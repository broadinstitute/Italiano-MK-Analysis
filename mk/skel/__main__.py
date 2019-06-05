import os, re, sys

sys.path.append(os.path.split(os.getcwd())[0] + os.sep + 'MK/mk')
from util import docs, tools

FOLDER = docs.main()

from util.folder import Folder, Stack
from util.cp import RunCP
from results import SkelImage, ProtrusionMask, ProtrusionSeed, PpltObj, Edges, Vertices

RE_TIF = re.compile("(.*)\.tif")
RE_TIFF = re.compile("(.*)\.tiff")
RE_PNG = re.compile("(.*)\.png")

PIPELINE = tools.read_config('skel')

def main():
    stack = Stack(FOLDER, RE_TIF)
    stack.df, stack.count
    time = stack.slices

    single = Folder(stack.folder('single_images'), RE_TIF)
    single.df
 
    # CellProfiler
    out = Folder(stack.folder('output'), RE_TIF)
    pplt_labels = Folder(out.folder('pplt_labels'), RE_TIFF)
    pplt_labels.df

    skel = Folder(stack.folder('skeleton'), RE_TIFF)
    RunCP(PIPELINE, stack.path, 'skel.txt', single.list + pplt_labels.list, skel.path)

    # Results
    res = SkelImage(skel.path, 'results_Image.csv', time)
    res.df
    res.analyze()

    res2 = ProtrusionMask(skel.path, 'results_protrusion_mask.csv', time, 'ProtrusionMasked')    
    res2.df
    res2.analyze()

    res3 = ProtrusionSeed(skel.path, 'results_protrusion_seed.csv', time, 'ProtrusionSeed')
    res3.df
    res3.analyze()

    res4 = PpltObj(skel.path, 'results_pplt_obj.csv', time, 'PpltObj')    
    res4.df
    res4.analyze()

    res5 = Edges(skel.path, 'results_edges.csv', time, 'Edges')    
    res5.df
    res5.analyze()

    res6 = Vertices(skel.path, 'results_vertices.csv', time, 'Vertices')    
    res6.df
    res6.analyze()

    tools.move_results(skel.path)

if __name__ == "__main__":
    main()
