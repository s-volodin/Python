import argparse
import os
import time
from hashlib import md5


def md5_hash_of_file(path):
    """
    Function generates MD5 hash of file
    :param path: Absolute path to the file on filesystem
    :return: MD5 hash of file
    """
    buffer = md5()
    with open(path, 'rb') as f:
        [buffer.update(line) for line in iter(f.readline, b'')]
    return buffer.hexdigest()


def indexing_files(path):
    """
    Function links the value of MD5 hash and absolute path to the file
    :param path: Absolute path to the folder where files shall be indexed
    :return: Dictionary which contains all pairs of 'path':'hash' values in specified folder and its sub-folders
    """
    dict_of_hashes = {}
    for f in os.scandir(path):
        if f.is_file():
            file_hash = md5_hash_of_file(f.path)
            dict_of_hashes[f.path] = file_hash
        elif f.is_dir():
            sub_folder_hashes = indexing_files(f.path)
            dict_of_hashes.update(sub_folder_hashes)
        else:
            print('It is neither a file or a directory: {}'.format(f.path))
    return dict_of_hashes


def group_files_by_hash(index):
    """
    Function groups files by hash in specified index
    :param index: Dictionary which contains pairs of 'path':'hash' values
    :return: Dictionary of files grouped by hash. Key is a hash, value is a list of files
    """
    grouped_files = {}
    for key, value in index.items():
        if value not in grouped_files.keys():
            grouped_files[value] = [key]
        else:
            grouped_files[value].append(key)
    return grouped_files


def filter_duplicates(sorted_dict):
    """
    Function generates dictionary with duplicates
    :param sorted_dict: Dictionary of files grouped by hash. Key is a hash, value is a list of files
    :return: Dictionary of duplicates grouped by hash. Key is a hash, value is a list of duplicates
    """
    duplicates = {key:value for key, value in sorted_dict.items() if len(value) > 1}
    return duplicates


def storage_scanner(path):
    """
    Function runs process of duplicates searching and outputs results to console
    :param path: Absolute path to the folder where duplicates shall be found
    """
    index = indexing_files(path)
    grouped_files = group_files_by_hash(index)
    duplicates = filter_duplicates(grouped_files)
    output_beautifier(duplicates)


def cmd_args_parser():
    """
    Function passes path as a parameter to the program
    :return: Path argument
    """
    parser = argparse.ArgumentParser(description='Find duplicates in specified folder')
    parser.add_argument('path', help='Absolute path to the folder where duplicates shall be found', type=str)
    args = parser.parse_args()
    return args.path


def output_beautifier(dictionary):
    """
    Function prints hash, list of duplicates and number of duplicates
    :param dictionary: Dictionary of duplicates
    """
    for key, value in dictionary.items():
        print('Hash: {} '.format(key))
        print('Files: {}'.format(value))
        print('Number of duplicates: {}\n'.format(len(value)))


def execution_time_calc(func):
    """
    Decorator function which calculates execution time of function
    :param func: Function which execution time should be calculated
    :return: Wrapped function
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print('Execution time is {} seconds'.format(round(end_time - start_time, 2)))
    return wrapper


@execution_time_calc
def main():
    path = cmd_args_parser()
    storage_scanner(path)


if __name__ == '__main__':
    main()
