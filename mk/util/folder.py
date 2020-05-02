import os, re, sys

import pandas as pd
import skimage, skimage.io

from util import tools

class Folder:
    def __init__(self, path, regex_obj):
        self.path = path
        self.regex_obj = regex_obj
        self._df = pd.DataFrame()
        self._count = None
        self._list = None

    # Create a new folder within the folder.
    def folder(self, name):
        return tools.create_folder(self.path, name)

    # Dataframe of images. Recognizes filenames matching regex_obj.
    @property
    def df(self):
        image_files_dict = [self.make_dict(f, self.path, self.regex_obj) for f in os.listdir(self.path) if 
                            self.is_image(f, self.regex_obj)]
        self._df = self.sort_df(image_files_dict)
        return self._df

    # Number of images recognized by the dataframe.
    @property
    def count(self):
        self._count = len(self._df)
        return self._count

    # List of image filepaths from the dataframe.
    @property
    def list(self):
        frame = pd.DataFrame()
        try:
            frame["filepath"] = self._df["path"].map(str) + os.sep + self._df["filename"]
        except KeyError:
            print('Check your dataframe(s).')
        file_path_dict = {r'{}'.format(k):v for k, v in frame['filepath'].items()}
        self._list = tools.alphanumeric_sort(list(set(file_path_dict.values())))
        return self._list

    # Create dictionary of images by *filename* & *path*.
    @staticmethod
    def make_dict(filename, path, re_obj):
        my_dict = re_obj.match(filename).groupdict()
        my_dict["filename"] = filename
        my_dict["path"] = path
        return my_dict

    # Checks if filename matches regex_obj.     
    @staticmethod
    def is_image(filename, re_obj):
        mybool = False
        if re_obj.match(filename) != None:
            mybool = True
        return mybool
    
    # Sort dataframe alphanumerically by *filename*.
    @staticmethod
    def sort_df(image_files_dict):
        df = pd.DataFrame(image_files_dict)
        if df.empty:
            pass
        else:
            df = tools.sort_dataframe(df, 'filename')
        return df

class Stack(Folder):
    def __init__(self, path, regex_obj):
        super(Stack, self).__init__(path, regex_obj)       
        self.done = None
        self._slices = None

    # Check if tiff stacks are unpacked by seeing if [# of stacks * slices per stack  = num unpacked images]
    def check(self, count_unpacked):
        try:    
            if (self._count * self._slices) is count_unpacked:
                self.done = True
            elif (self._count * self._slices) < count_unpacked:
                print(f'Expected {self._count * self._slices} unpacked images. Got {count_unpacked}. Proceeding anyways..')
                self.done = True
            else:
                self.done = False
        except TypeError:
            print("Run stack.count first.")
            
    # Use skimage to unpack stacks. If stacks are RGB, convert to 8-bit, then unpack.
    def unpack(self, destination, bit):
        if self.done:
            print("Stacks unpacked.")
        else:
            for n in self._df.index: 
                image = skimage.io.imread(os.path.join(self._df["path"][n], self._df["filename"][n]))
                timepoints = image.shape[0]
                               
                for i in range(timepoints):
                    if len(image.shape) is 4:
                        retest = self.regex_obj.match(self._df["filename"][n])
                        retest.group(1)
                        new_filename = "{0}-{1:04d}.tif".format(retest.group(1), i)
                        image2 = skimage.color.rgb2gray(image)

                        if bit is 16:
                            image2 = skimage.img_as_uint(image2)
                        elif bit is 8:
                            image2 = skimage.img_as_ubyte(image2)

                        skimage.io.imsave(os.path.join(self._df["path"][n], destination, new_filename), image2[i]) 
                    else:
                        retest = self.regex_obj.match(self._df["filename"][n])
                        retest.group(1)
                        new_filename = "{0}-{1:04d}.tif".format(retest.group(1), i)
                        skimage.io.imsave(os.path.join(self._df["path"][n], destination, new_filename), image[i])
            
            self.done = True

    # Dataframe set to recognize if filename matches RE_STACK AND NOT RE_SINGLE.
    @property
    def df(self):
        regex_single = re.compile(".*\-\d{4}\.tif")
        image_files_dict = [self.make_dict(f, self.path, self.regex_obj) for f in os.listdir(self.path) if 
                            self.is_stack(f, self.regex_obj, regex_single)] 
        self._df = self.sort_df(image_files_dict)
        return self._df

    # Checks if stack image's filename matches REGEX_STACK, and not REGEX_SINGLE.
    @staticmethod
    def is_stack(filename, RE_STACK, RE_SINGLE):
        mybool = False
        if (RE_STACK.match(filename) != None 
            and RE_SINGLE.match(filename) == None
        ):
            mybool = True
        return mybool

    # Use skimage to read every stack & get the slices (timepoints). If all slices are the same, return number of slices in a stack. Else, None.
    @property
    def slices(self):
        df = self._df
        stack_timepoints = []
        for n in df.index:
            stack = skimage.io.imread(os.path.join(df["path"][n], df["filename"][n]))
            time = stack.shape[0]
            stack_timepoints.append(time)

        srs = pd.Series(t for t in stack_timepoints)
        df['timepoints'] = srs.values
        time_srs = df['timepoints'].value_counts()

        if len(time_srs) is 1:
            # print(int(time_srs.index.values))
            self._slices = int(time_srs.index.values)
        else:
            self._slices = None
        return self._slices

class Ilastik(Folder):
    def __init__(self, path, regex_obj):
        super(Ilastik, self).__init__(path, regex_obj)
        self.incomplete = pd.DataFrame()

    # Acquire dataframe of incomplete single tif images, by identifying missing probability maps. Used for running ilastik.
    def check(self, prbstg_dict, single_df):
        if self._df.empty is False and self._count is len(single_df)*4:
            self.incomplete = pd.DataFrame()
            print("All probability maps created.")
        elif self._df.empty:
            self.incomplete = single_df  
            print("No probability maps found.")     
        else:
            self.incomplete = self.check_incomplete(self.df, prbstg_dict, self.regex_obj, single_df)
        return self.incomplete

    # Check for missing ilastik probabilities by referencing single_df. Return list of unprocessed single images.
    @staticmethod
    def check_incomplete(df, prbstg_dict, RE_PNG, single_df):
        ilastik_dict = {r'{}'.format(k):v for k, v in df['filename'].items()}
        missing_ilastik = []
        for n in ilastik_dict:
            for i in prbstg_dict:
                drop_ext = re.sub(prbstg_dict[i], '', ilastik_dict[n])
                if re.match(RE_PNG, drop_ext):
                    pass
                else:                            
                    missing_ilastik.append(drop_ext)
                    
        missing_ilastik = tools.alphanumeric_sort(list(set(missing_ilastik)))
        unprocessed_single = [s + '.tif' for s in missing_ilastik]
        unprocessed_srs = single_df['filename'][~single_df['filename'].isin(unprocessed_single)]
        incomplete_df = single_df.loc[unprocessed_srs.index.values].reset_index(drop=True)
        return incomplete_df
