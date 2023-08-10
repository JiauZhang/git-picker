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
            url = f'{self.base_url}/{file}'
            lines = self.download_file(url)
            filename = f'{self.repo}/{file}'
            self.save_file(filename, lines)

    def download_file(self, url):
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

        return lines

    def save_file(self, filename, lines):
        dirname = osp.dirname(filename)
        if not osp.exists(dirname):
            os.makedirs(dirname)
        with open(filename, 'w') as f:
            for i in range(len(lines)-1):
                f.write(lines[i] + '\n')
            f.write(lines[-1])
