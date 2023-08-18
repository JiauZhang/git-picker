import json, requests
from .picker import Picker

class Gitee(Picker):
    def __init__(self, user, repo, branch, files, **kwargs):
        super().__init__(user, repo, branch, files, **kwargs)
        self.base_url = f'https://gitee.com/{self.user}/{self.repo}/raw/{self.branch}'

    def make_url(self, path):
        return f'{self.base_url}/{path}'

    def get_file_lines(self, url):
        r = requests.get(url)
        print(r.text)
        return [r.text]

    def get_dir_items(self, url):
        ...

    def parse_items(self, items):
        _dirs, _files = [], []
        ...
        return _dirs, _files
