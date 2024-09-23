import unittest
from os import makedirs, mkdir, listdir
from os.path import isdir, join as pathjoin
from shutil import rmtree
import json
from math import ceil
from random import choices

from fileutils.split.splitter import join, default_shard_formatter, split, DEFAULT_INFO_FILE

def dir_maker_and_destroyer(dirpath):
    if not isdir(dirpath):
        try:
            makedirs(dirpath, mode=777)
        except Exception as e:
            return None, e
        return lambda: rmtree(dirpath), None
        
    else:
        if len(listdir(dirpath)) == 0:
            return lambda: rmtree(dirpath), None
        else:
            return lambda: None, Exception("desired directory is not empty")

class TestSplit(unittest.TestCase):
    home_path = "test/tmp/split/sampletext"
    chars = tuple(chr(i) for i in range(ord("a"), ord("z")+1))
    
    def make_run_clean(self, testfunc, subdir):
        dirpath = pathjoin(self.home_path, subdir)
        cleaner, exc = dir_maker_and_destroyer(dirpath)
        self.assertIsNone(exc, f"trouble making test directory: {exc}")
        err_msg = ""
        try:
            testfunc()
        except Exception as test_exc:
            err_msg += str(test_exc)

        try:
            cleaner()
        except Exception as cleaner_exc:
            err_msg += "\ntrouble cleaning up test files: " + str(cleaner_exc)
            
        if err_msg != "":
            self.fail(err_msg)
    
    def write_split_join_check(self, dir_path, size, shard_size):
        shards_path = pathjoin(dir_path, "shards")
        filepath = pathjoin(dir_path, "file.txt")
        join_path = pathjoin(dir_path, "joined.txt")
        mkdir(shards_path, mode=777)
        
        contents = "".join(choices(self.chars, k=size))
        
        try:
            with open(filepath, "w") as f:
                f.write(contents)
        except Exception as e:
            raise Exception(f"cannot make original file: {e}")
        
        try:
            split(filepath, shards_path,
            shard_size, default_shard_formatter, "", True)
        except Exception as e:
            raise Exception(f"error splitting file: {e}")
    
        err = None
        try:
            with open(pathjoin(shards_path, DEFAULT_INFO_FILE), "r") as f:
                try:
                    info = json.loads(f.read())
                except json.JSONDecodeError as e:
                    err = f"error decoding shard info: {e}"
                if len(info["shards"]) != ceil(size/shard_size):
                    err = "shard list is larger than expected"
        except Exception as e:
            raise Exception(f"error reading shard info: {e}")
        if err:
            raise Exception(err)
        
        try:
            join([], pathjoin(shards_path, DEFAULT_INFO_FILE), join_path)
        except Exception as e:
            raise Exception(f"error joining shards: {e}")

        err = None
        try:
            with open(join_path, "r") as f:
                if contents != f.read():
                    err = "joined file different from start"
        except Exception as e:
            raise Exception(f"error reading joined file: {e}")
        if err:
            raise Exception(err)

    def complete_run(self, size, shard_size, subdir):
        dirpath = pathjoin(self.home_path, subdir)
        checker = lambda: self.write_split_join_check(dirpath, size, shard_size)
        self.make_run_clean(checker, subdir)

    def test_text_split_exact(self):
        self.complete_run(500_000, 100_000, "exact_multiple")

    def test_text_split_incomplete(self):
        self.complete_run(550_000, 100_000, "remainder_half")

    def test_text_split_exact_one(self):
        self.complete_run(100_000, 100_000, "exact_single")

    def test_text_split_half_one(self):
        self.complete_run(50_000, 100_000, "half_single")

    def test_text_split_small(self):
        self.complete_run(1, 100_000, "small")

    def test_text_split_almost_2(self):
        self.complete_run(199_999, 100_000, "almost_2")

    def test_text_split_byteshards(self):
        self.complete_run(10, 1, "10x1")

    def test_text_split_singlebyte(self):
        self.complete_run(10, 1, "1x1")

if __name__ == "__main__":
    unittest.main()