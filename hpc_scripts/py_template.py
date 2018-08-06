import glob
import h5py
import numpy
import os
import os.path
import pandas
import re
import skimage
import skimage.exposure
import skimage.io
import subprocess

# Change the following line to your folder directory
image_directory = r"/n/data2/bwh/medicine/italiano/180731_PV"
# Change the following line to the path of your ilastik project file
path_to_project = r"/n/data2/bwh/medicine/italiano/Incucyte_Analysis/180805_FLMK.ilp"

path_to_ilastik = r"/n/data2/bwh/medicine/italiano/ilastik-1.3.0-Linux/run_ilastik.sh"
regex_image = "(.*)\.tif" #stack
regex_single = ".*\-\d{4}\.tif" #slice
re_image = re.compile(regex_image)
re_single = re.compile(regex_single)

os.makedirs(os.path.join(image_directory, "single_images"), exist_ok=True)
imdir_single = os.path.join(image_directory,"single_images")
os.makedirs(os.path.join(image_directory, "ilastik"), exist_ok=True)
imdir_ilastik = os.path.join(image_directory,"ilastik")
# os.makedirs(os.path.join(image_directory, "output"), exist_ok=True)
# output_directory = os.path.join(image_directory,"output")

def is_my_file(filename, re_image, re_single):
    
    mybool = False
    
    if (    re_image.match(filename) != None 
        and re_single.match(filename) == None
       ):
        
        mybool = True
        
    return mybool


def make_dict(filename, path, re_obj):
    
    my_dict = re_obj.match(filename).groupdict()
    
    my_dict["filename"] = filename
    
    my_dict["path"] = path
    
    return my_dict

image_files_dict = [make_dict(f, image_directory, re_image) for f in os.listdir(image_directory) if is_my_file(f, re_image, re_single)]
image_df = pandas.DataFrame(image_files_dict)

def df_stack_image(p):
    
    im = skimage.io.imread(os.path.join(p["path"], p["filename"]))
    
    if len(im.shape) < 4:
        
        retest = re_image.match(p["filename"])

        retest.group(1)

        fname = "{0}-{1:04d}.tif".format(retest.group(1), 0)
        
        im2 = skimage.color.rgb2gray(im)
        
        im2 = skimage.img_as_ubyte(im2)

        skimage.io.imsave(os.path.join(p["path"], fname), im2)
        
    else:
    
        number_of_timepoints = im.shape[0]

        for i in range(number_of_timepoints):

            retest = re_image.match(p["filename"])

            retest.group(1)

            fname = "{0}-{1:04d}.tif".format(retest.group(1), i)
            
            im2 = skimage.color.rgb2gray(im[i,:,:,:])
        
            im2 = skimage.img_as_ubyte(im2)

            skimage.io.imsave(os.path.join(p["path"], "single_images", fname), im2)

if image_df.empty is False:
    
    _ = image_df.apply(df_stack_image, axis=1)

else:
    
    print("no images to unpack")          
    
def is_my_file(filename, re_obj):
    
    mybool = False
    
    if re_obj.match(filename) != None:
        
        mybool = True
        
    return mybool


def make_dict(filename, path, re_obj):
    
    my_dict = re_obj.match(filename).groupdict()
    
    my_dict["filename"] = filename
    
    my_dict["path"] = path
    
    return my_dict

image_files_dict = [make_dict(f, imdir_single, re_single) for f in os.listdir(imdir_single) if is_my_file(f, re_single)]
image_df = pandas.DataFrame(image_files_dict)

def df_ilastik(p):
    
    filename = os.path.join(p["path"], p["filename"])
    
    filename_noext = os.path.splitext(p["filename"])[0]
    
    filename_h5 = "{}_Probabilities Stage 2.h5".format(filename_noext)
    
    # Run ilastik using subprocess
    
    command = (path_to_ilastik,"--headless","--export_source=probabilities stage 2","--output_format=hdf5",
               r"--project={}".format(path_to_project),filename)
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    
    out, err = process.communicate()
    
    # unpack the HDF5 file
    
    label_list = ["background", "protrusion", "cell_boundary", "cell"]
    
    path_h5 = os.path.join(p["path"], filename_h5)
    
    with h5py.File(path_h5, "r") as ilastik_hdf5:
    
        ilastik_probabilities = ilastik_hdf5["exported_data"].value
    
        for i in range(ilastik_probabilities.shape[2]):
            im = skimage.img_as_uint(ilastik_probabilities[:, :, i])
        
            filename_slice = "{}_{}_prbstg2_{}.png".format(filename_noext, label_list[i], i)
        
            skimage.io.imsave(os.path.join(p["path"], "..", "ilastik", filename_slice), im)
    
    os.remove(path_h5)

_ = image_df.apply(df_ilastik, axis=1)
