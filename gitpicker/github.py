import json, requests
from .picker import Picker

class GitHub(Picker):
    def __init__(self, user, repo, branch, files, **kwargs):
        super().__init__(user, repo, branch, files, **kwargs)
        self.base_url = f'https://github.com/{self.user}/{self.repo}/blob/{self.branch}'

    def get_file_lines(self, file):
        url = f'{self.base_url}/{file}?plain=1'
        r = requests.get(url)
        js = json.loads(r.text)
        lines = js['payload']['blob']['rawLines']
        return lines

    def get_dir_items(self, dir):
        url = f'{self.base_url}/{dir}'
        r = requests.get(url)
        js = json.loads(r.text)
        items = js['payload']['tree']['items']
        return items

    def parse_items(self, items):
        _dirs, _files = [], []
        for item in items:
            ctype = item['contentType']
            path = item['path']
            if ctype == 'directory':
                _dirs.append(path)
            elif ctype == 'file':
                _files.append(path)
            else:
                raise RuntimeError(f'unsupport contentType: {ctype}')
        return _dirs, _files
