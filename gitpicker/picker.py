import os, time, httpx, traceback
import os.path as osp
from abc import ABC, abstractmethod

class Picker(ABC):
    def __init__(self, user, repo, branch, num_retry=10, time_interval=5, client_kwargs={},):
        self.user = user
        self.repo = repo
        self.branch = branch
        self.num_retry = num_retry
        self.time_interval = time_interval
        self.non_txt_suffixes = set([
            'png', 'jpg', 
        ])
        self.client = httpx.Client(**client_kwargs)
        self._files = []

    def makedirs(self):
        os.makedirs(self.repo, exist_ok=True)
        if 'file' in self.files:
            dirnames = set()
            for file in self.files['file']:
                filename = f'{self.repo}/{file}'
                dirnames.add(osp.dirname(filename))
            for dirname in dirnames:
                os.makedirs(dirname, exist_ok=True)

    @staticmethod
    def suffix(file):
        basename = osp.basename(file)
        i = basename.rfind('.')
        if i == -1: return ''
        return basename[i+1:]

    def skip(self, file):
        suffix = self.suffix(file)
        return suffix in self.non_txt_suffixes

    @staticmethod
    def check_arg(str_or_list):
        if isinstance(str_or_list, list):
            return str_or_list
        elif isinstance(str_or_list, str):
            return [str_or_list]
        else:
            raise RuntimeError('only support str or list!')

    def pick(self, files):
        self.files = files
        self.makedirs()

        if 'file' in self.files:
            files = self.check_arg(self.files['file'])
            for file in files:
                self._files.append(file)
        if 'dir' in self.files:
            dirs = self.check_arg(self.files['dir'])
            for dir in dirs:
                self.append_dir_files(dir)
                time.sleep(self.time_interval)

        for file in self._files:
            self.download_file(file)
            time.sleep(self.time_interval)

    def save_file(self, filename, lines):
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(len(lines)-1):
                f.write(lines[i] + '\n')
            f.write(lines[-1])

    @abstractmethod
    def get_file_lines(self, url):
        ...

    @abstractmethod
    def get_dir_items(self, url):
        ...

    def download_file(self, file):
        if not self.skip(file): 
            print(f'downloading {self.repo}/{file}')
        else:
            print(f'skip to download non text file: {self.repo}/{file}')
            return
        retry, lines = 0, None
        einfo = ''
        while retry < self.num_retry:
            try:
                lines = self.get_file_lines(file)
                break
            except Exception as e:
                einfo = e
                retry += 1
                print(f'retry[{retry}/{self.num_retry}] {self.repo}/{file} failed!')
                time.sleep(self.time_interval)

        if lines is None or retry == self.num_retry:
            info = f'num_retry[{retry}/{self.num_retry}] downloading {self.repo}/{file} failed!\n{einfo}'
            raise RuntimeError(info)

        filename = f'{self.repo}/{file}'
        self.save_file(filename, lines)

    def append_dir_files(self, dir):
        print(f'downloading {self.repo}/{dir}')
        os.makedirs(f'{self.repo}/{dir}', exist_ok=True)
        retry, items = 0, None
        einfo = ''
        while retry < self.num_retry:
            try:
                items = self.get_dir_items(dir)
                break
            except Exception as e:
                einfo = e
                retry += 1
                print(f'retry[{retry}/{self.num_retry}] {self.repo}/{dir} failed!')
                time.sleep(self.time_interval)

        if items is None or retry == self.num_retry:
            info = f'num_retry[{retry}/{self.num_retry}] downloading {self.repo}/{dir} failed!\n{einfo}'
            raise RuntimeError(info)

        _dirs, _files = items

        for file in _files:
            self._files.append(file)
        for dir in _dirs:
            self.append_dir_files(dir)
