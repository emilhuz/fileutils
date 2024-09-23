import unittest
from os.path import join, split, normpath
from fileutils.search.file_processors import count_lines
from fileutils.search.search import search_file_contents

class TestCountLines(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCountLines, self).__init__(*args, **kwargs)
        self.loc = "test/data/search/lines"
        self.all_counts = {
            "text1.txt":5,
            "text2.txt":1,
            "empty.txt":1,
            "code.py":3,
            "subdir/hello.txt":1,
            "subdir/data.json":3
        }
        self.all_counts = {normpath(join(self.loc, path)):count for path, count in self.all_counts.items()}
    
    
    def test_all_lines(self):
        line_counts, total_count = count_lines(self.loc, ignore_empty_lines=False)
        
        line_counts = {normpath(item[0]):item[1] for item in line_counts}
        expected_total = sum(self.all_counts.values())
        
        self.assertEqual(self.all_counts, line_counts)
        self.assertEqual(expected_total, total_count)
    
    def test_non_empty_lines(self):
        line_counts, total_count = count_lines(self.loc, ignore_empty_lines=True)
        
        line_counts = {normpath(item[0]):item[1] for item in line_counts}
        expected_counts = self.all_counts.copy()
        expected_counts[normpath(join(self.loc, "code.py"))] = 2
        expected_counts[normpath(join(self.loc, "empty.txt"))] = 0
        expected_total = sum(expected_counts.values())
        
        self.assertEqual(expected_counts, line_counts)
        self.assertEqual(expected_total, total_count)
    
    def test_max_depth(self):
        line_counts, total_count = count_lines(self.loc, ignore_empty_lines=False, max_depth=0)
        
        line_counts = {normpath(item[0]):item[1] for item in line_counts}
        expected_counts = self.all_counts.copy()
        del expected_counts[normpath(join(self.loc, "subdir/data.json"))]
        del expected_counts[normpath(join(self.loc, "subdir/hello.txt"))]

        expected_total = sum(expected_counts.values())
        
        self.assertEqual(expected_counts, line_counts)
        self.assertEqual(expected_total, total_count)
    
    def test_filename_filter(self):
        line_counts, total_count = count_lines(self.loc, ignore_empty_lines=False, file_path_filter=lambda fpath: fpath.split(".")[-1] == "txt")
        
        line_counts = {normpath(item[0]):item[1] for item in line_counts}
        expected_counts = self.all_counts.copy()
        del expected_counts[normpath(join(self.loc, "subdir/data.json"))]
        del expected_counts[normpath(join(self.loc, "code.py"))]

        expected_total = sum(expected_counts.values())
        
        self.assertEqual(expected_counts, line_counts)
        self.assertEqual(expected_total, total_count)


class TestSearch(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSearch, self).__init__(*args, **kwargs)
        self.loc = "test/data/search/lines"
    
    def test_simple_contents(self):
        where_found = search_file_contents(self.loc, "1")
        expected_found = ["text1.txt", "text2.txt", "subdir/data.json"]
        self.assertEqual(set(map(normpath, where_found)), {normpath(join(self.loc, x)) for x in expected_found})
    
    def test_simple_contents_maxdepth(self):
        where_found = search_file_contents(self.loc, "1", max_depth=0)
        expected_found = ["text1.txt", "text2.txt"]

        self.assertEqual(set(map(normpath, where_found)), {normpath(join(self.loc, x)) for x in expected_found})
    
    def test_simple_contents_ignorecase(self):
        where_found = search_file_contents(self.loc, "HeLlO", ignore_case=True)
        expected_found = ["subdir/hello.txt"]

        self.assertEqual(set(map(normpath, where_found)), {normpath(join(self.loc, x)) for x in expected_found})