import os, subprocess, sys
from shutil import copy2

import h5py
import pandas as pd
from tqdm._tqdm_notebook import tqdm_notebook

from utils import tools

# Change string to match config.ini
CP_PATH = tools.read_config('cp')

class RunCP:    
    ''' Run CellProfiler, with the option to copy the Analyst Rules file used to process your pipeline.'''
    def __init__(self, pipeline, path, list_name, image_list, output, rules=None):
        self.pipeline = pipeline
        self.path = path
        self.list_name = list_name
        self.image_list = image_list
        self.output = output
        self.rules = rules
        self.run()

    def run(self):
        if self.rules is not None:
            copy2(self.rules, self.path)
        else:
            pass
        
        if not os.path.exists(self.output + os.sep + 'overlay'):
            self.create_cp_list(self.path, self.list_name, self.image_list)
            self.process(self.pipeline, self.path, self.list_name, self.output) 
        else:
            print(f'>> Results are in {self.output}.')
            pass

    @staticmethod
    def create_cp_list(path, list_name, list):
        with open(os.path.join(path, list_name), 'w') as f:
            for item in list:
                f.write("{}\n".format(item))

    @staticmethod
    def process(pipeline, path, filelist, output):
        if sys.platform == 'win32':
            command = [CP_PATH,
                    "--run-headless",
                    "--pipeline={}".format(pipeline),
                    "--file-list={}".format(os.path.join(path,filelist)),
                    "--image-directory={}".format(path),
                    "--output-directory={}".format(output)
                    ]

            cmd_str = ' '.join(str(n) for n in command)
            print(">> Running command:" + cmd_str)
        else:
            command = CP_PATH + " -p {}".format(pipeline) + " --file-list {}".format(os.path.join(path, filelist)) + " -i {}".format(path) + " -o {}".format(output)
            print(">> Running command:" + command)

        process = subprocess.Popen(command, shell=True)
        out, err = process.communicate()