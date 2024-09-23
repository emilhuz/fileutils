from fileutils.search.tree_traverse import process_file_contents

def count_lines(dirpath, ignore_empty_lines=True,
                dir_path_filter=None, file_path_filter=None, max_depth=None,
                print_err=True):
    counts = []
    def counter(fpath, contents:str):
        numlines = sum(1 for l in contents.split("\n")
                       if (not ignore_empty_lines or l.strip() != ""))
        counts.append([fpath, numlines])

    process_file_contents(dirpath, counter, dir_path_filter, max_depth, file_path_filter, print_err)
    
    return counts, sum(item[1] for item in counts)
