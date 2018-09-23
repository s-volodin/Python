import urllib.request
import urllib.error
import threading
import argparse
import time


CHUNK_SIZE = 32768


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


def cmd_args_parser():
    """
    Function passes path as a parameter to the program
    :return: Path argument
    """
    parser = argparse.ArgumentParser(description='Download files (wget) in multiple threads')
    parser.add_argument('path', help='URL to the file', type=str)
    args = parser.parse_args()
    return args.path


class DataManager:
    @staticmethod
    def get_file_size(url):
        """
        Function gets size of file based on Content-Length in HTTP response
        :param url: URL to the file
        :return: File size in bytes
        """
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            return int(response.headers['Content-Length'])
        except urllib.error.HTTPError as e:
            print('HTTP Error: ' + str(e.code) + ' ' + str(e.reason))
        except urllib.error.URLError as e:
            print('URL Error: ' + str(e.reason))

    @staticmethod
    def get_file_name(url):
        """
        Function gets name of the file based on last portion of data in a path
        :param url: URL to the file
        :return: File name
        """
        return url.split('/')[-1]

    @staticmethod
    def get_data_portion(begin, offset, url):
        """
        Function gets portion of file defined by Range header
        :param begin: Start byte
        :param offset: Offset in bytes
        :param url: URL to the file
        :return: Portion of data in defined range of bytes
        """
        try:
            headers = {'Range': 'bytes=' + str(begin) + '-' + str(begin + offset - 1)}
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request)
            data_portion = response.read()
            return data_portion
        except urllib.error.HTTPError as e:
            print('HTTP Error: ' + str(e.code) + ' ' + str(e.reason))
        except urllib.error.URLError as e:
            print('URL Error: ' + str(e.reason))
        except IOError as e:
            print('IOError: Disk is full. ' + str(e))
        except OSError as e:
            print('OSError: ' + str(e))
        except Exception as e:
            print('Exception: ' + str(e))

    @staticmethod
    def save_data_portion(file_name, begin, data):
        """
        Saving chunk of data in a file
        :param file_name: Name of file
        :param begin: Start byte where chunk has to be saved in a file
        :param data: Portion of data which has to be saved
        :return:
        """
        with open(file_name, 'r+b') as f:
            f.seek(begin)
            f.write(data)


    @staticmethod
    def create_empty_file(file_name):
        """
        Creates empty file
        :param file_name: Name of file
        """
        with open(file_name, 'wb') as f:
            f.write(b'')


class MyThread(threading.Thread):
    def __init__(self, begin, offset, url):
        threading.Thread.__init__(self)
        self.begin = begin
        self.offset = offset
        self.url = url

    def run(self):
        file_name = DataManager.get_file_name(self.url)
        data = DataManager.get_data_portion(self.begin, self.offset, self.url)
        DataManager.save_data_portion(file_name, self.begin, data)


def threads_runner(url):
    active_threads_list = []
    begin = 0
    offset = CHUNK_SIZE
    active_threads = 4
    file_size = DataManager.get_file_size(url)
    file_name = DataManager.get_file_name(url)
    DataManager.create_empty_file(file_name)
    pool_of_threads = int(file_size/offset) + 1

    if pool_of_threads <= active_threads:
        active_threads = pool_of_threads

    while(pool_of_threads > 0):
        for i in range(active_threads):
            t = MyThread(begin, offset, url)
            active_threads_list.append(t)
            t.start()
            begin += offset

        for t in active_threads_list:
            t.join()

        pool_of_threads -= active_threads


@execution_time_calc
def main():
    url = cmd_args_parser()
    threads_runner(url)


if __name__ == '__main__':
    main()

