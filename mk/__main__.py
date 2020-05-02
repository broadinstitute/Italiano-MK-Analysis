import re
from util import docs, tools

# Check if main folder exists from terminal
FOLDER = docs.main()

from util.folder import Folder, Stack, Ilastik
from util.il import RunIL
from util.cp import RunCP
from util.results import ResultsImage, ResultsObject

# Regular expressions to identify images in folders
RE_TIF = re.compile("(.*)\.tif")
RE_PNG = re.compile("(.*)\.png")

# Dictionary of probability extensions generated in ilastik. Used for checking created maps.
PRBSTG_DICT = {0:'_background_prbstg2_0.png', 1:'_cell_boundary_prbstg2_1.png', 2:'_mk_prbstg2_2.png', 3:'_pplt_prbstg2_3.png'}

# Get pipeline & rules from config.ini
PIPELINE = tools.read_config('mk')
RULES = tools.read_config('rules')

def main():
    # Initialize main folder of tiff stacks, derive timepoints by checking slices
    stack = Stack(FOLDER, RE_TIF)
    stack.df, stack.count
    time = stack.slices

    # Check & unpack single images
    single = Folder(stack.folder('single_images'), RE_TIF)
    single.df
    stack.check(single.count)
    stack.unpack(single.path, 8)
    single.df

    # Ilastik
    ilastik = Ilastik(stack.folder('ilastik'), RE_PNG)
    ilastik.df, ilastik.count
    ilastik.check(PRBSTG_DICT, single.df)
    RunIL(ilastik.incomplete)
    ilastik.df
    
    # CellProfiler
    out = stack.folder('output')
    RunCP(PIPELINE, stack.path, 'mk.txt', single.list + ilastik.list, out, rules=RULES)
    
    # Results
    res = ResultsImage(out, 'results_Image.csv', time)
    res.df
    x = res.analyze()

    res2 = ResultsObject(out, 'results_mk_filter.csv', time, 'MK')
    res2.df
    y = res2.analyze()

    res3 = ResultsObject(out, 'results_pplt_filter.csv', time, 'PPLT')
    res3.df
    z = res3.analyze()

    tools.move_results(out)

if __name__ == "__main__":
    main()