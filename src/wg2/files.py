import os
import shutil


def read(f):
    with open(f) as input_file:
        return input_file.read()


def empty_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    # os.mkdir(directory)