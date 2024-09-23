from fileutils.search.tree_traverse import eval_tree, process_file_contents

def search_path_substr(dirpath, substr, ignore_case=False, print_running=False,
                       dir_path_filter=None, max_depth=None) -> list:
    matching = []
    if ignore_case:
        substr = substr.lower()
    def comparator(fpath, isfile):
        if ignore_case:
            fpath = fpath.lower()
        
        if substr in fpath:
            matching.append(fpath)
            if print_running:
                print(fpath)
    
    eval_tree(dirpath, comparator, dir_path_filter, max_depth)
    return matching


def search_file_contents(dirpath, substr, ignore_case=False, print_running=False,
                         dir_path_filter=None, file_path_filter=None, max_depth=None,
                         print_err=True) -> list:
    matching = []
    if ignore_case:
        substr = substr.lower()
    def comparator(fpath, contents):
        if ignore_case:
            contents = contents.lower()
        
        if substr in contents:
            matching.append(fpath)
            if print_running:
                print(fpath)
    
    process_file_contents(dirpath, comparator,
                                 dir_path_filter, max_depth, file_path_filter,
                                 print_err)
    return matching