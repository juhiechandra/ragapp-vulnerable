# this is a file for extracting the tar file and getting the files inside it

import tarfile
import os

def extract_tar_file(tar_file_path, extract_path=None):

    if extract_path:
        os.makedirs(extract_path, exist_ok=True)
        with tarfile.open(tar_file_path, 'r') as tar:
            tar.extractall(path=extract_path, filter="data")   
    else:
        with tarfile.open(tar_file_path, 'r') as tar:
            tar.extractall(filter="data")   

def get_files_from_tar_file(tar_file_path):
    with tarfile.open(tar_file_path, 'r') as tar:
        return tar.getnames()

def extract_tarfile(tar_file_path, extract_path=None):
    if extract_path:
        os.makedirs(extract_path, exist_ok=True)
        with tarfile.open(tar_file_path, 'r') as tar:
            tar.extractall(path=extract_path, filter="tar")   
    else:
        with tarfile.open(tar_file_path, 'r') as tar:
            tar.extractall(filter="tar")   

if __name__ == "__main__":
    print(get_files_from_tar_file('test.tar'))