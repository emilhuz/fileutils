import argparse
import sys
from fileutils.split.splitter import split, join, default_shard_formatter

def main_split():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_op", help="whether to split file or join")
    
    parser.add_argument("filename", help="name of file to split")
    parser.add_argument("destination", help="folder in which to store resulting shards")
    parser.add_argument("--piece-size", required=True, type=int, help="desired shard size in bytes (smaller means more shards)")
    parser.add_argument("--metadata-file", required=False, default=None, help="where to store metadata about shards")

    args=parser.parse_args()
    
    try:
        split(args.filename, args.destination, args.piece_size, default_shard_formatter, args.metadata_file, True)
    except Exception as e:
        print("Error splitting file:", e)

def main_join():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_op", help="whether to split file or join")

    parser.add_argument("metadata_file", help="from where to load metadata about shards")
    parser.add_argument("destination", help="file in which to join shards")

    args=parser.parse_args()

    try:
        join([], args.metadata_file, args.destination)
    except Exception as e:
        print("Error joining file shards:", e)
    pass

def main():
    usage = f"""Usage:
              For splitting: {__name__} split <other-args>
              For joining: {__name__} join <other-args>"""
              
    if len(sys.argv) < 2:
        print(usage)
        return
    file_op = sys.argv[1]
    
    if file_op == "split":
        main_split()
    elif file_op == "join":
        main_join()
    else:
        print(usage)
