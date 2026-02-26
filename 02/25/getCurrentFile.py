import os
from os import path

filename="pathpy_output.txt"

# Get the current working directory
def current_directory():
    cwd=os.getcwd()
    print(cwd)

# Get the absolute path of the file if it exists in this directory
def file_path(filename):
    if path.exists(filename):
        print(path=os.path.abspath((filename)))
    else:
        print("file does not exist in " + os.getcwd())
    
current_directory()
file_path(filename)