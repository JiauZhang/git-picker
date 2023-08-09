import os, json, requests
import os.path as osp

class Picker():
    def __init__(self, user, repo, branch, files):
        self.user = user
        self.repo = repo
        self.branch = branch
        self.files = files
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
        r = requests.get(url)
        js = json.loads(r.text)
        lines = js['payload']['blob']['rawLines']
        return lines

    def save_file(self, filename, lines):
        with open(filename, 'w') as f:
            for i in range(len(lines)-1):
                f.write(lines[i] + '\n')
            f.write(lines[-1])
