import requests
from .picker import Picker

class Gitee(Picker):
    def __init__(self, user, repo, branch, files, **kwargs):
        super().__init__(user, repo, branch, files, **kwargs)
        self.base_url = f'https://gitee.com/{self.user}/{self.repo}/raw/{self.branch}'
        self.web_url = f'https://gitee.com//{self.user}/{self.repo}/tree/{self.branch}'
        self.dir_tree = {'tree': {}, 'sha': self.branch}
        from lxml import etree
        self.to_html = etree.HTML

    def make_url(self, path, file_type):
        if file_type == 'file':
            return f'{self.base_url}/{path}'
        elif file_type == 'dir':
            return f'{self.web_url}/{path}'
        else:
            raise RuntimeError(f'Unsupported file_type: {file_type}')

    def get_file_lines(self, url):
        r = requests.get(url)
        return [r.text]

    def get_dir_items(self, url):
        r = requests.get(url)
        html = self.to_html(r.text.encode('utf-8'))
        dir_tree = html.xpath('//div[@id="tree-slider"]')[0]
        _dirs = dir_tree.xpath('./div[@data-type="folder"]')
        for i in range(len(_dirs)):
            _dirs[i] = _dirs[i].xpath('./div[@data-type="folder"]')[0].attrib['data-path']
        _files = dir_tree.xpath('./div[@data-type="file"]')
        for i in range(len(_files)):
            _files[i] = _files[i].xpath('./div[@data-type="file"]')[0].attrib['data-path']
        return _dirs, _files

    def parse_items(self, items):
        _dirs, _files = items
        return _dirs, _files
