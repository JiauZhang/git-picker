from .picker import Picker
from lxml.etree import HTML as parse_html

class Gitee(Picker):
    def __init__(self, user, repo, branch, client_kwargs={}):
        client_kwargs.update({
            'base_url': f'https://gitee.com/{user}/{repo}',
            'follow_redirects': True,
        })
        super().__init__(user, repo, branch, client_kwargs=client_kwargs)

    def get_file_lines(self, file):
        url = f'/raw/{self.branch}/{file}'
        r = self.client.get(url)
        return [r.text]

    def get_dir_items(self, dir):
        url = f'/tree/{self.branch}/{dir}'
        r = self.client.get(url)
        html = parse_html(r.text.encode('utf-8'))
        dir_tree = html.xpath('//div[@id="tree-slider"]')[0]
        _dirs = dir_tree.xpath('./div[@data-type="folder"]')
        for i in range(len(_dirs)):
            _dirs[i] = _dirs[i].xpath('./div[@data-type="folder"]')[0].attrib['data-path']
        _files = dir_tree.xpath('./div[@data-type="file"]')
        for i in range(len(_files)):
            _files[i] = _files[i].xpath('./div[@data-type="file"]')[0].attrib['data-path']
        return _dirs, _files
