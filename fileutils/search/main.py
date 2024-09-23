import argparse
import sys
from typing import Callable
from fileutils.search.search import search_path_substr, search_file_contents
from fileutils.search.file_processors import count_lines

def checker_path_contains_none(strs: list):
    strs = [x for x in strs if x!=""]
    def check(path: str) -> bool:
        return all(x not in path for x in strs)
    return check

def combined_filter(f1, f2: Callable[[str], bool]) -> Callable[[str], bool]:
    def comb_filter(input_str):
        return f1(input_str) and f2(input_str)
    return comb_filter

def main_names():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_kind")
    
    parser.add_argument("dir", help="directory to search")
    parser.add_argument("str", help="what to search for")
    parser.add_argument("--ignore-case", required=False, type=str, default="", help="whether to ignore case (y to set)")
    parser.add_argument("--not-in-path", required=False, type=str, default=None, help="exclude paths that contain at least one of these")

    args=parser.parse_args()

    path_filter = None
    if args.not_in_path != "":
        path_filter = checker_path_contains_none(args.not_in_path.split(","))

    found_paths = search_path_substr(args.dir, args.str, args.ignore_case.lower()=="y", dir_path_filter=path_filter)
    print("\n".join(found_paths))

def make_file_ext_filter(exts, noexts):
    if len(exts) > 0 and len(noexts) > 0:
        print("Flag exts is set. Ignoring no_exts")
    
    def file_ext_filter(filepath:str):
        if len(exts) == 0 and len(noexts) == 0:
            # no conditions on extensions, all files pass
            return True
        ext = filepath.split(".")
        if len(ext) == 1:
            return len(exts) > 0
        ext = ext[-1]
        if len(exts) > 0:
            return ext in exts
        else:
            return ext not in noexts
    return file_ext_filter

def main_contents():
    parser = argparse.ArgumentParser()
    parser.add_argument("search_kind")
    
    parser.add_argument("dir", help="directory to search")
    parser.add_argument("str", help="what to search for")
    parser.add_argument("--ignore-case", required=False, type=str, default="", help="whether to ignore case (y to set)")
    parser.add_argument("--exts", required=False, type=str, default="", help="extensions to consider")
    parser.add_argument("--no-exts", required=False, type=str, default="", help="extensions to ignore")
    parser.add_argument("--not-in-path", required=False, type=str, default=None, help="exclude paths that contain at least one of these")

    args=parser.parse_args()
    
    exts = [ext.strip() for ext in args.exts.split(",") if ext != ""]
    noexts = [ext.strip() for ext in args.no_exts.split(",") if ext != ""]

    path_filter = make_file_ext_filter(exts, noexts)
    
    if args.not_in_path != "":
        path_filter = combined_filter(path_filter,
                                      checker_path_contains_none(args.not_in_path.split(","))
                                      )
    
    found_paths = search_file_contents(args.dir, args.str, args.ignore_case.lower()=="y", file_path_filter=path_filter)
    print("\n".join(found_paths))


def main_count_lines():
    parser = argparse.ArgumentParser()
    parser.add_argument("lines_kind")
    
    parser.add_argument("dir", help="directory to search")
    parser.add_argument("--ignore-empty-lines", required=False, type=str, default="", help="count empty lines (y to set)")
    parser.add_argument("--exts", required=False, type=str, default="", help="extensions to consider")
    parser.add_argument("--no-exts", required=False, type=str, default="", help="extensions to ignore")
    parser.add_argument("--sort-count", required=False, type=str, default="", help="sort by line count (y to set)")
    parser.add_argument("--not-in-path", required=False, type=str, default="", help="exclude paths that contain at least one of these")
    parser.add_argument("--group-dir", required=False, type=str, default="", help="show line count in each directory (y to set)")
    
    args=parser.parse_args()
    
    exts = [ext.strip() for ext in args.exts.split(",") if ext != ""]
    noexts = [ext.strip() for ext in args.no_exts.split(",") if ext != ""]

    path_filter = make_file_ext_filter(exts, noexts)
    
    if args.not_in_path != "":
        path_filter = combined_filter(path_filter,
                                      checker_path_contains_none(args.not_in_path.split(","))
                                      )
    
    counts, total = count_lines(args.dir, ignore_empty_lines=args.ignore_empty_lines.lower()=="y", file_path_filter=path_filter)
    if args.sort_count.lower()=="y":
        counts.sort(key=lambda x: x[1], reverse=True)
    print(total)
    print("\n".join(map(str, counts)))


def main():
    usage = f"""Usage:
              For searching names: {__name__} names <other-args>
              For searching inside files: {__name__} contents <other-args>"""
    if len(sys.argv) < 2:
        print(usage)
        return
    file_op = sys.argv[1]
    
    if file_op == "names":
        main_names()
    elif file_op == "contents":
        main_contents()
    elif file_op == "countlines":
        main_count_lines()
    else:
        print(usage)