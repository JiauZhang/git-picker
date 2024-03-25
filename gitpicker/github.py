from .picker import Picker
from conippets import git

class GitHub(Picker):
    def __init__(self, user, repo, branch, files, **kwargs):
        super().__init__(user, repo, branch, files, **kwargs)
        self.base_url = f'https://github.com/{self.user}/{self.repo}/blob/{self.branch}'

    def get_file_lines(self, file):
        url = f'{self.base_url}/{file}'
        lines = git.rawLines(url)
        return lines

    def get_dir_items(self, dir):
        url = f'{self.base_url}/{dir}'
        items = git.list_dir(url)
        return self.parse_items(items)

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
