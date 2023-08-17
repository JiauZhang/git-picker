import os, time
import threading as td
from queue import Queue
from abc import ABC, abstractmethod

class Picker(ABC):
    def __init__(self, retry=10, threads=os.cpu_count()):
        self.retry = retry
        self.tasks = Queue()
        self.lock = td.Lock()
        self.threads = threads
        self.running = False

    def pick(self):
        self.running = True
        threads = [td.Thread(target=self.download_thread) for _ in range(self.threads)]
        _ = [thread.start() for thread in threads]

        if 'file' in self.files:
            files = self.files['file']
            self.lock.acquire()
            for file in files:
                self.tasks.put(file)
            self.lock.release()
        if 'dir' in self.files:
            dirs = self.files['dir']
            for dir in dirs:
                self.download_dir(dir)

        self.running = False
        _ = [thread.join() for thread in threads]

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
    def download_file(self, file):
        ...

    @abstractmethod
    def download_dir(self, dir):
        ...
