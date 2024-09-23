from setuptools import setup

setup(name="fileutils",
      packages=["fileutils", "fileutils.search", "fileutils.split"],
      version="1.0.0",
      requires=["json", "argparse"])