import os, json, requests, time
import os.path as osp

class Picker():
    def __init__(self, user, repo, branch, files, retry=10):
        self.user = user
        self.repo = repo
        self.branch = branch
        self.files = files
        self.retry = retry
        self.base_url = f'https://github.com/{self.user}/{self.repo}/blob/{self.branch}'

        if not osp.exists(self.repo):
           os.makedirs(self.repo)

    def pick(self):
        files = self.files['file']
        for file in files:
            self.download_file(file)
        dirs = self.files['dir']
        for dir in dirs:
            self.download_dir(dir)

    def download_file(self, file):
        url = f'{self.base_url}/{file}'
        print(f'downloading {url}')
        retry = 0
        while retry < self.retry:
            try:
                r = requests.get(url)
                js = json.loads(r.text)
                lines = js['payload']['blob']['rawLines']
                break
            except:
                retry += 1
                print(f'retry[{retry}/{self.retry}] failed!')
                time.sleep(1)

        if retry == self.retry:
            raise RuntimeError('retry failed!')

        filename = f'{self.repo}/{file}'
        self.save_file(filename, lines)

    def save_file(self, filename, lines):
        dirname = osp.dirname(filename)
        if not osp.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'w') as f:
            for i in range(len(lines)-1):
                f.write(lines[i] + '\n')
            f.write(lines[-1])

    def download_dir(self, dir):
        url = f'{self.base_url}/{dir}'
        print(f'downloading {url}')
        retry = 0
        while retry < self.retry:
            try:
                r = requests.get(url)
                js = json.loads(r.text)
                items = js['payload']['tree']['items']
                break
            except:
                retry += 1
                print(f'retry[{retry}/{self.retry}] failed!')
                time.sleep(1)

        if retry == self.retry:
            raise RuntimeError('retry failed!')

        _dirs, _files = [], []
        for item in items:
            ctype = item['contentType']
            if ctype == 'directory':
                _dirs.append(item['path'])
            elif ctype == 'file':
                _files.append(item['path'])
            else:
                raise RuntimeError(f'unsupport contentType: {ctype}')

        for file in _files:
            self.download_file(file)
        for dir in _dirs:
            self.download_dir(dir)