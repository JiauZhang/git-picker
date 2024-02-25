import os, time, httpx, traceback
import os.path as osp
import threading as td
from queue import Queue
from abc import ABC, abstractmethod

class Picker(ABC):
    def __init__(self, user, repo, branch, files, retry=10, threads=os.cpu_count()):
        self.user = user
        self.repo = repo
        self.branch = branch
        self.files = files
        self.retry = retry
        self.tasks = Queue()
        self.lock = td.Lock()
        self.threads = threads
        self.running = False
        self.failed = False
        self.non_txt_suffixes = set([
            'png', 'jpg', 
        ])
        self.client = httpx.Client()

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

    def pick(self):
        self.running = True
        threads = [td.Thread(target=self.download_thread) for _ in range(self.threads)]
        _ = [thread.start() for thread in threads]

        if 'file' in self.files:
            files = self.check_arg(self.files['file'])
            self.lock.acquire()
            for file in files:
                self.tasks.put(file)
            self.lock.release()
        if 'dir' in self.files:
            dirs = self.check_arg(self.files['dir'])
            for dir in dirs:
                self.download_dir(dir)

        self.running = False
        _ = [thread.join() for thread in threads]

    def save_file(self, filename, lines):
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(len(lines)-1):
                f.write(lines[i] + '\n')
            f.write(lines[-1])

    def download_thread(self):
        while self.running or not self.tasks.empty():
            if self.failed:
                return
            if not self.tasks.empty():
                self.lock.acquire()
                task = None
                if not self.tasks.empty():
                    task = self.tasks.get()
                self.lock.release()
                if task: self.download_file(task)
            else:
                time.sleep(1)

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
        while not self.failed and retry < self.retry:
            try:
                lines = self.get_file_lines(file)
                break
            except:
                retry += 1
                print(f'retry[{retry}/{self.retry}] {self.repo}/{file} failed!')
                time.sleep(1)

        if lines is None or retry == self.retry:
            self.failed = True
            raise RuntimeError(f'retry[{retry}/{self.retry}] downloading {self.repo}/{file} failed!')

        filename = f'{self.repo}/{file}'
        self.save_file(filename, lines)

    def download_dir(self, dir):
        print(f'downloading {self.repo}/{dir}')
        os.makedirs(f'{self.repo}/{dir}', exist_ok=True)
        retry, items = 0, None
        while not self.failed and retry < self.retry:
            try:
                items = self.get_dir_items(dir)
                break
            except:
                retry += 1
                print(f'retry[{retry}/{self.retry}] {self.repo}/{dir} failed!')
                traceback.print_exc()
                time.sleep(1)

        if items is None or retry == self.retry:
            self.failed = True
            raise RuntimeError(f'retry[{retry}/{self.retry}] downloading {self.repo}/{dir} failed!')

        _dirs, _files = items

        self.lock.acquire()
        for file in _files:
            self.tasks.put(file)
        self.lock.release()
        for dir in _dirs:
            self.download_dir(dir)
