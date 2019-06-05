# MK Analysis

## Overview

This workflow is designed to analyze phase-contrast, tif time-lapses of **Megakaryocytes** &amp; **Pro-platelet** differentiation using **ilastik** & **CellProfiler**. These open-source tools have been tethered through the python package management system **Conda**.

## Requirements

1. Miniconda3
2. ilastik
3. CellProfiler [Requires installation of Java SE 8 Runtime Environment]

### Image Requirements

* **Tif Stacks** - 
The stacks should be within a folder. Stacks should follow this naming convention: ie: 190101_MK_A1_1. (Date_Experiment_Well_Site)

* **Single 8-bit Tifs** - 
These single images should be within a folder named **single_images**.

### 1. Miniconda3

* https://docs.conda.io/en/latest/miniconda.html

1. Install for all folders.

2. Add Anaconda to the system PATH variable environment.

3. (Optional) Register Anaconda as the system Python 3.*.

### 2. ilastik

* https://www.ilastik.org/download.html

- Mac: unpack the tar.bz2 file, and move it to the Applications folder.
- Windows: install to default location

### 3. CellProfiler

* https://cellprofiler.org/releases/

- Mac: install the dmg file into the Applications folder.
- Windows: install to default location

## Ilastik Training

1. Open your ilastik project file (ilp).

2. Convert your single tif training images to 8-bit in FIJI/ImageJ.

3. Import the images in the 'Input Data' section under 'raw data', select all of the images, right click, edit properties, and in the section called 'Storage', change them from 'Relative Link' to 'Copied to Project File'.

4. In Stage 1, be sure when you label the images, all classifiers are labeled equally (equal number of dots/labels), otherwise it will bias them. Target irregular shapes, regions of high uncertainty, and areas between cells.

5. In Stage 2, you can be more free-form with your labeling. Lower uncertainty in Stage 1 leads to improved learning/probability maps for Stage 2.

## Running the Analysis

1. Clone or download the **MK** Github repository into your home folder. ie: /home/Italiano (Mac); C:\\Users\\Italiano\\ (Windows).

2. Edit the config.ini file (use any text editor), and change the file paths for the section that matches your computer (Darwin - Mac, Win32 - Any windows computer, Linux). These path variables shouldd correspond to the locations of the applications/ilp/pipelines on your computer. 

3. i) Open the anaconda prompt (should open in your home folder). ii) enter 'cd MK' to move into the MK folder, iii) type 'conda env create -f environment.yml'. This will create the 'bioimg' environment which is required to be active to run this workflow.

4. a) In anaconda prompt (**Terminal**), when the prompt is located in the MK folder (step 3ii), type 'conda activate bioimg'.
b) **Terminal** - To run the program, enter 'python mk "your_folder_path"'.
c) **Jupyter** - Type 'jupyter notebook', and access the 'MK' notebook located in the jupyter folder. Edit the first cell in the notebook, next to the 'FOLDER' variable, to match the path to your folder containing your images. Click the '>>' under the Widgets tab at the top, to run the entire notebook.

## I. MK

1. Tif stacks (RGB/8-bit) get unpacked into a folder called *single_images* (converted to 8-bit).

2. A folder named *ilastik* is created, and Ilastik is started headlessly (no GUI), running the ilp defined within config.ini. Each single tif image is processed, by first creating an h5 file within the *single_images* folder; the code then unpacks each h5 file into the ilastik folder (4 png probability maps per 1 single tif image).

3. After ilastik has finished, a text file, *mk.txt* is created in the project folder, containing all the paths to the single images & ilastik probabilities intended for processing. The machine learning rules text file (already created via CellProfiler Analyst), called *mouse_rules.txt* or *human_rules.txt* is copied into the project folder as well. These text files are required to be in the main folder, for mk.cppipe to recognize them and initiate the analysis.

4. A folder called *output* is created, and CellProfiler runs headlessly. Upon completion, 3 folders are created in the *output* folder: 1) overlay, 2) mk_labels, & 3) pplt_labels; results files (results_) are also generated. The '_labels' folders contain 16-bit tif images masking the locations of identified cellular objects. These are used downstream in the skel & fluo pipelines.

5. Excel files are created by CellProfiler and formatted by the code: 1) ImageResults - contains general data for all of the analyzed tif images. 2) MKArea 3) MKCount 4) PPLTArea 5) PPLTCount 6) PctPPLTProd  7) MKResults 8) PPLTResults - The MK & PPLT Results csvs, contain shape metrics for each identified cell/object. 

6. New folders are created within the *output* folder, containing graphs of 1) MKArea 2) MKCount 3) PPLTArea 4) PPLTCount & 5) PctPPLTProd. The raw files with the prefix results_ are moved into a folder called *raw_files*.

**FYI**

- Formatting of the excel files is exclusive to the raw outputs of mouse & human.cppipe.

- The results_mk, results_pplt properties files & their respective .db (database) files (required for CellProfiler Analyst) are moved into the raw_files folder as well. You will need to move them back into the *output* folder to open them in CellProfiler Analyst to update/train the machine learning text rules.

- The MK pipeline has to be run prior to executing the skel/fluo pipelines.

## II. Skel

1. The *skeleton* folder will be created in the main folder.

2. A text file called *skel.txt* will be created, containing the file paths to the single tif images and proplatelet label images (located in output - created by mk.cppipe) intended for processing.

3. CellProfiler runs, and will generate 2 folders, 1) overlay - QC of skeletonized protrusions, which have been overlayed onto the original single phase tif image. 2) branchpoints - skeletonized proplatelets marked with nodes for length identification.

4. Excel results: 1) ImageResults, 2) PpltObjResults - correspond to the proplatelet objects within the 16-bit label images (proplatelet_labels). 3) ProtrusionMaskedResults - protrusions identified in the skel.cppipe, that have been masked by the proplatelet labels. 4) ProtrusionSeedResults - gives you total proplatelet object branch lengths., 5) Edges & 6) Vertices - Edges & Vertices give you individual branch lengths & their node positions/locations. 

## III. Fluo

1. In the main folder, a folder called *fluo* must exist, containing fluorescent tif stacks that correspond to the phase stacks in the primary folder. The stacks will be unpacked into a folder within *fluo*, called *fluo_single*.

2. A text file called *fluo.txt* will be created, containing the file paths to the single tif images, fluo single tif images, mk_labels & proplatelet_labels folders.

3. CellProfiler runs, and will generate 1 folder, 1) overlay - QC of fluorescent images that have been corrected by the illumination function created within the pipeline. 

4. Excel results: 1) FluoImage - Image results for fluorescent images. 2) FluoMK 3) FluoPPLT - FluoMK & FluoPPLT give intensity values of puncta masked by the MK & PPLT labels.
