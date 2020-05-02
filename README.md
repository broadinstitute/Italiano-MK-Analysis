# MK Analysis

### Getting Started

This image processing workflow is designed to analyze phase-contrast, tif time-lapses of **Megakaryocytes** &amp; **Pro-platelet** differentiation using **ilastik** & **CellProfiler**.

## Prerequisites

### Image Format(s)

* **Multi-Image {Stack} (.tif)** - 
The stack(s) should be within a folder, with all images following this naming convention: *Date_ExperimentName_Well_Site* (ie: 190101_MK_A1_1).

* **{Single} 8-bit Image (.tif)** - 
These individual images should be within a folder named *single_images*.

### Software

* **Italiano_MK_Analysis Repo**

* **Python 3**

* **ilastik**

* **CellProfiler & CellProfiler Analyst - [Java Runtime Environment required]** 

## Installation

### Italiano_MK_Analysis Repo

```
1. Clone/download this Github repository.
```

```
2. Move/unzip the repo into your home folder (ie: /home/Italiano [Mac]; C:\\Users\\Italiano\\ [Windows]).
```

### Python 3

* https://www.python.org/downloads/

```
1. Install Python 3 for your OS.
```

```
2. Open up a terminal/command prompt.
```

```
3. Enter 'pip3 install pipenv' (pipenv is used to setup the workflow environment).
```

### ilastik

* https://www.ilastik.org/download.html

```
Mac: Unpack the tar.bz2 file, and move the ilastik icon into the Applications folder.
```

```
Windows: Run the default installation.
```

### CellProfiler

* https://cellprofiler.org/releases/

```
Mac: Unzip the zip file, and move the CellProfiler icon into the Applications folder.
```

```
Windows: Run the default installation.
```

## Setup

### ilastik Training

```
1. Create a new ilastik project file (ilp), for the AutoContext (2-stage) workflow.
```

```
2. Convert your single tif training images to 8-bit in FIJI/ImageJ.
```

```
3. a) Import the images in the 'Input Data' section under 'raw data', select all of the images, right click, then click edit properties. 

   b) In the section called 'Storage', change it from 'Relative Link' to 'Copied to Project File'.
```

```
4. a) In Stage 1, be sure when you label the images, all classifiers are labeled equally (equal number of dots/labels), otherwise it will bias them. 

   b) Target irregular shapes, regions of high uncertainty, and areas between cells.
```

```
5. a) In Stage 2, you can be more free-form with your labeling. 

   b) Lower uncertainty in Stage 1 leads to improved learning/probability maps for Stage 2.
```

### Workflow Setup

```
1. a) Open up a terminal/command prompt. 

   b) Navigate to the Italiano_MK_Analysis folder, using the cd command (ie: cd /Users/Italiano/Desktop/Italiano_MK_Analysis).
```

```
2. Enter 'pipenv install -r requirements.txt' to install the workflow environment.
```

```
3. a) Edit the config.ini file in the repo folder (using any text editor). 

   b) Change the file paths for the section that matches your operating system (Darwin - Mac, Win32 - Windows, Linux). 

   c) These path variables should correspond to the locations of the applications/ilp/pipelines/text files on your computer.
```

### Running the workflow

```
1) a) Open a Terminal/command prompt.

   b) Navigate to the Italiano_MK_Analysis folder using the cd command.

   c) Enter 'pipenv shell' to activate the workflow environment.
```

* via Terminal

```
- Enter 'python mk "your_image_folder_path"' (ie: python mk /Users/Italiano/Desktop/MK_Images).
```

* via Jupyter Notebook

```
- Enter 'jupyter notebook'.

- Access the 'MK' notebook located in the jupyter folder (inside the repo). 

- Type in the path to your image folder, next to the 'FOLDER = ' variable, in the first cell. 

- Click the '>>' under the Widgets tab at the top, to run the entire notebook. 

- Alternatively, progress through the notebook step by step by using 'Shift + Enter'.
```

## Workflow Overview

### I. MK

```
1. Tif stacks (RGB/8-bit) get unpacked into a folder called *single_images* (converted to 8-bit).
```

```
2. a) A folder named *ilastik* is created, and ilastik is started headlessly (no GUI), running the ilp defined within config.ini. 

   b) Each single tif image is processed, by first creating an h5 file within the *single_images* folder.

   c) The code then unpacks each h5 file into the ilastik folder (4 .png probability maps per 1 single .tif image).
```

```
3. a) After ilastik has finished, a text file, 'mk.txt' is created in the project folder.

	- It contains folder paths of all single images & ilastik probability maps intended for processing. 

   b) The machine learning rules text file (already created via CellProfiler Analyst), called *mouse_rules.txt* or *human_rules.txt* is copied into the project folder as well. 
   
	- The mk & machine learning text files are required to be in the main folder, for mk.cppipe to recognize them and initiate the analysis.
```

```
4. a) A folder called *output* is created, and CellProfiler runs headlessly. 

   b) Upon completion, results files (results_) are generated, alongside 3 new folders, located in the 'output' folder: 
	  1) overlay
	  2) mk_labels
	  3) pplt_labels results files

   c) The '_labels' folders contain 16-bit tif images masking the locations of identified cellular objects. These are used downstream in the skel & fluo pipelines.
```

```
5. Excel files are created by CellProfiler and formatted by the code: 

	a) ImageResults - contains general data for all of the analyzed tif images. 
	b) MKArea 
	c) MKCount 
	d) PPLTArea 
	e) PPLTCount 
	f) PctPPLTProd  
	g) MKResults 
	h) PPLTResults 
	   - The MK & PPLT Results csvs, contain shape metrics for each identified cell/object. 
```

```
6. New folders are created within the *output* folder, containing graphs of:

	a) MKArea 
	b) MKCount 
	c) PPLTArea 
	d) PPLTCount 
	e) PctPPLTProd
```

```
7) All raw files with the prefix 'results_' are moved into a folder called 'raw_files'.
```

**FYI**

* The MK pipeline has to be run prior to executing the skel/fluo pipelines.


* Formatting of excel data is custom for the raw output files, from the mouse & human.cppipe.

### II. Skel

```
1. The 'skeleton' folder will be created in the main folder.
```

```
2. A text file called 'skel.txt' will be created.
   
   - It contains the file paths to the single tif images and proplatelet label images (located in output - created by mk.cppipe) intended for processing.
```

```
3. CellProfiler runs, and will generate 2 folders:

   a) overlay - QC of skeletonized protrusions, which have been overlayed onto the original single phase tif image. 

   b) branchpoints - skeletonized proplatelets marked with nodes for length identification.
```

```
4. Excel results: 

   a) ImageResults 

   b) PpltObjResults - correspond to the proplatelet objects within the 16-bit label images (proplatelet_labels). 

   c) ProtrusionMaskedResults - protrusions identified in the skel.cppipe, that have been masked by the proplatelet labels. 

   d) ProtrusionSeedResults - gives you total proplatelet object branch lengths.

   e) Edges

   f) Vertices

   - Edges & Vertices give you individual branch lengths & their node positions/locations. 
```

### III. Fluo

```
1. a) In the main folder, a folder called 'fluo' must exist, containing fluorescent tif stacks that correspond to the phase stacks in the primary folder. 

   b) The stacks will be unpacked into a folder within *fluo*, called *fluo_single*.
```

```
2. A text file called 'fluo.txt' will be created.

   - It contains the file paths to the single tif images, fluo single tif images, mk_labels & proplatelet_labels folders.
```

```
3. CellProfiler runs, and will generate 1 folder:
   
   a) overlay - QC of fluorescent images that have been corrected by the illumination function created within the pipeline. 
```

```
4. Excel results: 

   a) FluoImage - Image results for fluorescent images.

   b) FluoMK 

   c) FluoPPLT 
      
	- FluoMK & FluoPPLT give intensity values of puncta masked by the MK & PPLT labels.
```
