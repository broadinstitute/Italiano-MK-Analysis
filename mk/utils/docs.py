import os, sys

try:
    from docopt import docopt
except ModuleNotFoundError:
    sys.exit(">>> Bioimg environment inactive - type 'source activate bioimg'.")

def main():
    args = docopt("""
    \b
     Italiano Megakaryocyte & Proplatelet Differentiation Analysis

        Usage:
            mk <folder>
            mk -h, --help
            
        Examples:
            mk C:\\Users\\italiano\\Desktop\\folder
            mk /Users/italiano/Desktop/folder

        Options:
            -h, --help            [help message]
    \b
""")
    folder = args['<folder>'][:]
    if os.path.exists(folder):
        return folder      
    else:
        sys.exit(f'>>> {folder} does not exist. Check path.')
