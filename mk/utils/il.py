import os, subprocess, sys

import h5py
import pandas as pd
import skimage
import skimage.io
from tqdm._tqdm_notebook import tqdm_notebook

from utils import tools

# Change strings within ('') to match config.ini
ILASTIK_PATH = tools.read_config('il')
ILP = tools.read_config('ilp')

# Ilastik classifiers for hdf5 unpacking (corresponds to ilp's stage-2 export order.) [ilastik.check()]
LABEL_LIST = ["background", "cell_boundary", "mk", "pplt"]

class RunIL:
    def __init__(self, df):
        self.df = df
        self.run()

    def run(self):
        if tools.isnotebook():
            tqdm_notebook.pandas(desc="run ilastik")
            _ = self.df.progress_apply(self.process, axis=1)
        else:
            try: 
                _ = self.df.apply(self.process, axis=1)
            except OSError:
                sys.exit(">>> Check ilastik path and config.ini.")
    
    @staticmethod
    def process(df):
        filename = os.path.join(df["path"], df["filename"])
        filename_noext = os.path.splitext(df["filename"])[0]
        filename_h5 = "{}_Probabilities Stage 2.h5".format(filename_noext)

        # Run ilastik using subprocess -> output hdf5 file
        process = subprocess.Popen([ILASTIK_PATH, 
                    "--headless",
                    "--export_source=probabilities stage 2",
                    "--output_format=hdf5",
                    r"--project={}".format(ILP),
                    filename
                    ], stdout=subprocess.PIPE)
        out, err = process.communicate()
        
        path_h5 = os.path.join(df["path"], filename_h5)
        with h5py.File(path_h5, "r") as ilastik_hdf5:
            ilastik_probabilities = ilastik_hdf5["exported_data"].value

        for i in range(ilastik_probabilities.shape[2]):
            im = skimage.img_as_uint(ilastik_probabilities[:, :, i])
            filename_slice = "{}_{}_prbstg2_{}.png".format(filename_noext, LABEL_LIST[i], i)
            skimage.io.imsave(os.path.join(df["path"], "..", "ilastik", filename_slice), im)

        os.remove(path_h5)