import os, time
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
        self.non_txt_suffixes = set([
            'png', 'jpg', 
        ])

        if not osp.exists(self.repo):
           os.makedirs(self.repo)

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
        dirname = osp.dirname(filename)
        if not osp.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(len(lines)-1):
                f.write(lines[i] + '\n')
            f.write(lines[-1])

    def download_thread(self):
        while (self.running or not self.tasks.empty()):
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
        retry = 0
        while retry < self.retry:
            try:
                lines = self.get_file_lines(file)
                break
            except:
                retry += 1
                print(f'retry[{retry}/{self.retry}] failed!')
                time.sleep(1)

        if retry == self.retry:
            raise RuntimeError('retry failed!')

        filename = f'{self.repo}/{file}'
        self.save_file(filename, lines)

    @abstractmethod
    def parse_items(self, items):
        ...

    def download_dir(self, dir):
        print(f'downloading {self.repo}/{dir}')
        retry = 0
        while retry < self.retry:
            try:
                items = self.get_dir_items(dir)
                break
            except:
                retry += 1
                print(f'retry[{retry}/{self.retry}] failed!')
                time.sleep(1)

        if retry == self.retry:
            raise RuntimeError('retry failed!')

        _dirs, _files = self.parse_items(items)

        self.lock.acquire()
        for file in _files:
            self.tasks.put(file)
        self.lock.release()
        for dir in _dirs:
            self.download_dir(dir)
