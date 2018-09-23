import urllib.request
import urllib.error
import argparse
from abc import ABC
from abc import abstractmethod
from math import floor


class BaseProgressBar(ABC):
    @abstractmethod
    def display_progress(self):
        pass


class ConsoleProgressBar(BaseProgressBar):
    def __init__(self, file_name, downloaded_content, file_size):
        self.file_name = file_name
        self.downloaded_content = downloaded_content
        self.file_size = file_size

    def display_progress(self):
        progress = floor(self.downloaded_content/self.file_size*100)
        print('\rDownloading {} - {}% [{} of {}]'.format(
            self.file_name, progress, self.downloaded_content,
            self.file_size),
            end="")


class DisplayProgressBar:
    def __init__(self, progress_bar):
        self.progress_bar = progress_bar

    def display_progress(self):
        self.progress_bar.display_progress()


class BaseDataProvider(ABC):
    @property
    def chunk_size(self):
        return 8192

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def get_file_name(self):
        pass

    @abstractmethod
    def get_file_size(self):
        pass


class ReadHttpResponseData(BaseDataProvider):
    def __init__(self, url):
        self.url = url

    def read_data(self):
        request = urllib.request.Request(url=self.url)
        response = urllib.request.urlopen(request)
        return response

    def get_file_name(self):
        return self.url.split('/')[-1]

    def get_file_size(self):
        return int(self.read_data().headers['Content-Length'])


class DataProvider:
    def __init__(self, source):
        self.source = source

    def read_data(self):
        return self.source.read_data()

    def get_file_name(self):
        return self.source.get_file_name()

    def get_file_size(self):
        return self.source.get_file_size()


class WriteDataToFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_data(self, data):
        with open(self.file_name, 'wb') as file:
            file.write(data)


def console_progress(file_name, downloaded_content, file_size):
    progress_bar = ConsoleProgressBar(file_name, downloaded_content, file_size)
    DisplayProgressBar(progress_bar).display_progress()


def download_processing(source, file_name, file_size, data, output_file, progress_callback):
    downloaded_content = 0
    while file_size > downloaded_content:
        chunk = data.read(source.chunk_size)
        output_file.write_data(chunk)
        downloaded_content += len(chunk)
        progress_callback(file_name, downloaded_content, file_size)


def wget(url):
    try:
        source = ReadHttpResponseData(url)
        file_name = DataProvider(source).get_file_name()
        file_size = DataProvider(source).get_file_size()
        data = DataProvider(source).read_data()
        output_file = WriteDataToFile(file_name)
        download_processing(source, file_name, file_size, data, output_file, console_progress)
        print('\n{} has been downloaded successfully'.format(file_name))
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


def cmd_args_parser():
    """
    Function passes path as a parameter to the program
    :return: Path argument
    """
    parser = argparse.ArgumentParser(description='Download files (wget)')
    parser.add_argument('path', help='URL to the file', type=str)
    args = parser.parse_args()
    return args.path


def main():
    url = cmd_args_parser()
    wget(url)


if __name__ == '__main__':
    main()
