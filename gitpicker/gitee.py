from .picker import Picker

class Gitee(Picker):
    def __init__(self, user, repo, branch, files, **kwargs):
        super().__init__(user, repo, branch, files, **kwargs)
        self.base_url = f'https://gitee.com/{self.user}/{self.repo}/raw/{self.branch}'
        self.web_url = f'https://gitee.com//{self.user}/{self.repo}/tree/{self.branch}'
        from lxml import etree
        self.to_html = etree.HTML

    def get_file_lines(self, file):
        url = f'{self.base_url}/{file}'
        r = self.client.get(url, follow_redirects=True)
        return [r.text]

    def get_dir_items(self, dir):
        url = f'{self.web_url}/{dir}'
        r = self.client.get(url, follow_redirects=True)
        html = self.to_html(r.text.encode('utf-8'))
        dir_tree = html.xpath('//div[@id="tree-slider"]')[0]
        _dirs = dir_tree.xpath('./div[@data-type="folder"]')
        for i in range(len(_dirs)):
            _dirs[i] = _dirs[i].xpath('./div[@data-type="folder"]')[0].attrib['data-path']
        _files = dir_tree.xpath('./div[@data-type="file"]')
        for i in range(len(_files)):
            _files[i] = _files[i].xpath('./div[@data-type="file"]')[0].attrib['data-path']
        return _dirs, _files
