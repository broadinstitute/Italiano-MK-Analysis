import configparser, os, re, sys
from shutil import move
def alphanumeric_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

def create_folder(folder, new_folder_name):
    os.makedirs(os.path.join(folder, new_folder_name), exist_ok=True)
    new_folder = os.path.join(folder, new_folder_name)
    return new_folder

def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True 
        else:
            return False
    except NameError:
        return False 

def read_config(object):
    # Get path to app.py, replace with config.ini to allow reading of config.
    UTIL_PATH = os.path.dirname(os.path.abspath(__file__))
    UTIL_NAME = os.sep + 'mk' + os.sep + 'util'
    CONFIG_FILE = UTIL_PATH.replace(UTIL_NAME, os.sep + 'config.ini')
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    try:
        object_path = config.get(sys.platform, object)
        return object_path
    except configparser.NoSectionError:
        sys.exit(">>> Error! Check config.ini.")

def rename(folder, name1, name2):
    for fileName in os.listdir(folder):
        os.rename(fileName, fileName.replace(name1, name2))

def sort_dataframe(dataframe, alphanumeric_index):
    df = dataframe.set_index(alphanumeric_index)
    df2 = df.reindex(index=alphanumeric_sort(df.index))
    new_df = df2.reset_index()
    return new_df

# move the 'results_' files created by CP into a new directory
def move_results(output_folder):
    # create a new folder in the output folder called raw_results
    raw_folder = create_folder(output_folder,"raw_results")
    for filename in os.listdir(output_folder):
        if filename.startswith('results'):
            # move the 'results_' files from the output folder to a new folder
            src = output_folder + os.sep + filename
            new_folder = raw_folder + os.sep + filename
            move(src, new_folder)
    return raw_folder