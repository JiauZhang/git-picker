import json, requests
from .picker import Picker

class Gitee(Picker):
    def __init__(self, user, repo, branch, files, **kwargs):
        super().__init__(user, repo, branch, files, **kwargs)
        self.base_url = f'https://gitee.com/{self.user}/{self.repo}/raw/{self.branch}'
        self.base_api_url = f'https://gitee.com/api/v5/repos/{self.user}/{self.repo}/git/trees'
        self.dir_tree = {}

    def make_url(self, path, file_type):
        if file_type == 'file':
            return f'{self.base_url}/{path}'
        elif file_type == 'dir':
            return path
        else:
            raise RuntimeError(f'Unsupported file_type: {file_type}')

    def get_file_lines(self, url):
        r = requests.get(url)
        return [r.text]

    def get_tree(self, api_url):
        r = requests.get(api_url)
        js = json.loads(r.text)
        return js['tree']

    def parse_dir_tree(self, dir):
        if not self.dir_tree:
            api_url = f'{self.base_api_url}/{self.branch}'
            for node in self.get_tree(api_url):
                if node['type'] == 'tree':
                    node['tree'] = {}
                self.dir_tree[node['path']] = node
            self.dir_tree = {'tree': self.dir_tree}

        nodes = dir.split('/')
        dir_tree = self.dir_tree['tree']
        sha = self.branch
        for node in nodes:
            if node in dir_tree:
                sha = dir_tree['sha']
                dir_tree = dir_tree[node]['tree']
            else:
                api_url = f'{self.base_api_url}/{sha}'

    def get_dir_items(self, url):
        dir = url
        api_url = f'{self.base_api_url}/{url}'
        items = self.parse_dir_tree(dir)
        return items

    def parse_items(self, items):
        _dirs, _files = [], []
        ...
        return _dirs, _files
