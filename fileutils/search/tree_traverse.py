from os import listdir
from os.path import join, isdir
from typing import Callable

def eval_tree(dirpath: str,
              path_processor: Callable[[str, bool], None],
              dir_path_filter: Callable[[str], bool] = None,
              max_depth:int = None):

    path_processor(dirpath, True)
    
    files = listdir(dirpath)
    next_depth = None if max_depth is None else max_depth-1

    for f in files:
        subpath = join(dirpath, f)
        is_subpath_dir = isdir(subpath)
        path_processor(subpath, is_subpath_dir)
        
        # traverse subtrees
        # max_depth=0 means that no subdirectories of the current path need to be traversed
        if is_subpath_dir and (max_depth is None or max_depth>0):
            # enter subdirectory unless path filter returns False for it
            if not dir_path_filter or dir_path_filter(subpath):
                eval_tree(subpath, path_processor, dir_path_filter, next_depth)

def process_file_contents(dirpath: str, file_query: Callable[[str, str], None],
                                 dir_path_filter: Callable[[str], bool] = None, max_depth:int = None,
                                 file_path_filter: Callable[[str], bool] = None, print_err:bool = True):

    def path_processor(path:str, is_dir:bool):
        if is_dir or (file_path_filter and not file_path_filter(path)):
            return
        try:
            with open(path, "r") as f:
                contents = f.read()
        except UnicodeDecodeError as e:
            if print_err:
                print("Decoding error:", e)
            return
        except OSError as e:
            if print_err:
                print("Error reading file:", e)
            return
        
        try:
            file_query(path, contents)
        except Exception as e:
            if print_err:
                print("Error processing file contents:", e)
            return

    eval_tree(dirpath, path_processor, dir_path_filter, max_depth)
