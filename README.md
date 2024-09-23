# File utils

Performant CLI tool for directory exploration and sharding files.

## Searching files

Search file contents or file names for keywords with fine grained filtering options.

```sh
python -m fileutils.search contents . "sneaky text"
    --ignore-case y
    --exts txt,pdf
    --not-in-path unimportantfolder
```

## General tomfoolery

Count lines in project files:

```sh
python -m fileutils.search countlines .
    --no-exts pyc
    --not-in-path test
    --ignore-empty-lines y
    --sort-count y
```

## File sharding

Use the sharding tool to split a file into multiple pieces and stitch it back up later. Useful when backing up data to multiple places or over a slow network.

```sh
python -m fileutils.split split
    bigfile.mp4
    dest_folder
    --piece-size 100000000
```

```sh
python -m fileutils.split join
    dest_folder/info.split
    bigfile.mp4
```