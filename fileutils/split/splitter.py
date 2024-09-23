from os.path import split, getsize
from typing import Callable
import json

DEFAULT_SHARD_FILENAME_FORMAT = "%s.part%d.shard"
DEFAULT_INFO_FILE = "info.split"

def default_shard_formatter(fname:str, shard_num:int) -> str:
    return DEFAULT_SHARD_FILENAME_FORMAT % (fname, shard_num)

def split(filepath:str, destpath:str,
          size_pieces:int, shard_formatter:Callable[[str, int], str],
          info_file_name:str, write_info=True):
    if not filepath:
        raise ValueError("file path must be provided")
    fname = split(filepath)
    if fname[1] == "":
        raise ValueError(f"unexpected file name: empty after last slash ({filepath})")
    siz = getsize(filepath)
    if siz == 0:
        raise ValueError("File size is 0; nothing to split")
    
    if write_info and not info_file_name:
        info_file_name = f"{destpath}/{DEFAULT_INFO_FILE}"
    
    filenum = 0
    offset = 0
    shard_paths = []
    with open(filepath, "rb") as f:
        while offset < siz:
            
            f.seek(offset)
            piece_content = f.read(size_pieces)
            read_size = len(piece_content)
            offset += read_size

            filenum+=1
            shard_file_name = shard_formatter(fname[1], filenum)
            shard_path = f"{destpath}/{shard_file_name}"
            shard_paths.append(shard_path)
            with open(shard_path, "wb") as f_out:
                f_out.write(piece_content)
    if write_info:
        info = {"input_file":filepath, "size":siz, "shards":shard_paths}
        try:
            with open(info_file_name, "w") as f_info:
                f_info.write(json.dumps(info))
        except Exception as e:
            raise ValueError(f"cannot write shard info to file: {e}")



def join(shard_paths:list, info_file_path:str, dest_file_path:str):
    if not shard_paths:
        with open(info_file_path, "r") as f:
                info_str = f.read()
        try:
            info_dict = json.loads(info_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Cannot decode shard information: {e}")
        
        try:
            shard_paths = info_dict["shards"]
        except KeyError:
            raise ValueError("Cannot read shard paths from file")

    try:
        f = open(dest_file_path, "wb")
        for fpath in shard_paths:
            try:
                f1 = open(fpath, "rb")
                f.write(f1.read())
                f1.close()
            except Exception:
                print("Error writing piece")
                return
        f.close()
    except Exception:
        print("Error opening file for writing")
