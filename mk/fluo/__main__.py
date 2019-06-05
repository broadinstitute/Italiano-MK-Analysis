import os, re, sys

sys.path.append(os.path.split(os.getcwd())[0] + os.sep + 'MK/mk')
from util import docs, tools

FOLDER = docs.main()
FLUO_FOLDER = FOLDER + os.sep + 'fluo'

if os.path.exists(FLUO_FOLDER):
    from util.folder import Folder, Stack
    from util.cp import RunCP
    from results import FluoImage, FluoObject
else:
    sys.exit('>>> Unable to find folder named ''fluo''.')

RE_TIF = re.compile("(.*)\.tif")
RE_TIFF = re.compile("(.*)\.tiff")
RE_PNG = re.compile("(.*)\.png")

PIPELINE = tools.read_config('fluo')

def main():
    stack = Stack(FOLDER, RE_TIF)
    stack.df, stack.count

    single = Folder(stack.folder('single_images'), RE_TIF)
    single.df
        
    # Initialize fluo folder
    fluo = Stack(stack.path + os.sep + 'fluo', RE_TIF)
    fluo.df
    time = fluo.slices
    fluo_single = Folder(fluo.folder('fluo_single'), RE_TIF)
    fluo_single.df
    fluo.check(fluo_single.count)
    fluo.unpack(fluo_single.path, 8)
    fluo_single.df

    # CellProfiler
    out = Folder(stack.folder('output'), RE_TIF)
    mk_labels = Folder(out.folder('mk_labels'), RE_TIFF)
    pplt_labels = Folder(out.folder('proplatelet_labels'), RE_TIFF)
    mk_labels.df, pplt_labels.df

    fluo_out = Folder(fluo.folder('output'),RE_TIFF)
    RunCP(PIPELINE, stack.path, 'fluo.txt', single.list + fluo_single.list + mk_labels.list + pplt_labels.list, fluo_out.path)

    # Results
    res = FluoImage(fluo_out.path, 'results_Image.csv', time)
    res.df
    res.analyze()

    res2 = FluoObject(fluo_out.path, 'results_MaskedFluoMK.csv', time, 'FluoMK')
    res2.df
    res2.analyze()

    res3 = FluoObject(fluo_out.path, 'results_MaskedFluoPPLT.csv', time, 'FluoPPLT')
    res3.df
    res3.analyze()

    tools.move_results(fluo_out.path)

if __name__ == "__main__":
    main()
