# MK Analysis

## Overview

This workflow is designed to analyze phase-contrast, tiff time-lapses of **Megakaryocytes** &amp; **Pro-platelet** differentiation using **ilastik** & **CellProfiler**. These open-source tools have been tethered through the python package management system **Conda**.

## Requirements

1. Miniconda3
2. ilastik
3. CellProfiler [Requires Java SE 8 Runtime Environment]

### Image Requirements

* **Tif Stacks** - 
The stacks should be within a folder.

* **Single 8-bit Tifs** - 
These single images should be within a folder named **single_images**, ideally placed within a primary folder.

### 1. Miniconda3

* https://docs.conda.io/en/latest/miniconda.html

Install it to your home folder, ie: /home/Italiano (Macs); C:\\Users\\Italiano\\ (Windows).

### 2. ilastik

* https://www.ilastik.org/download.html

On Macs, unpack the tar.bz2 file, and move it to the Applications folder.

### 3. CellProfiler

* https://cellprofiler.org/releases/

On Macs, install the dmg file for both apps into the Applications folder.

## How to Use

1. Clone or download this Github repository into your home folder.

2. Edit the config.ini file (with any text editor), and change the file paths in the section that corresponds to your computer, to match the locations of the applications/ilp/pipelines. [Darwin/Macs, Win32/Any windows computer, Linux]

3. Open the anaconda prompt; i) type 'cd MK' to move into the MK folder, ii) type 'conda env create -f environment.yml'. This will create the 'bioimg' environment, that is required to be active, to run this workflow.

4. a) In anaconda prompt (**Terminal**), while the prompt is in the MK folder (step 3i), type 'conda activate bioimg'.
b) **Terminal** - To run the program, type 'conda activate bioimg', followed by 'python mk "your_folder_path"'.
c) **Jupyter** - Type 'jupyter notebook', and access the 'MK' notebook located in the jupyter folder. Edit the first cell in the notebook, next to the 'FOLDER' variable, to match the path to your folder containing your images. Click the '>>' under the Widgets tab at the top, to run the entire notebook.