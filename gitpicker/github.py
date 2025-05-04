import httpx
from .picker import Picker
from lxml.etree import HTML as parse_html
from conippets import json

_repo_data_xpath_ = '//react-partial[@partial-name="repos-overview"]/script[@data-target="react-partial.embeddedData"]'
_code_data_xpath_ = '//react-app[@app-name="react-code-view"]/script[@data-target="react-app.embeddedData"]'

class GitHub(Picker):
    def __init__(self, user, repo, branch, client_kwargs={}):
        client_kwargs.update({
            'base_url': f'https://github.com/{user}/{repo}',
            'follow_redirects': True,
        })
        super().__init__(user, repo, branch, client_kwargs=client_kwargs)

    def get_repo_data(self):
        r = self.client.get('')
        html = parse_html(r.text)
        repo_data = html.xpath(_repo_data_xpath_)[0]
        repo_data = json.loads(repo_data.text)
        return repo_data

    def createAt(self):
        repo_data = self.get_repo_data()
        create_time = repo_data['props']['initialPayload']['repo']['createdAt']
        return create_time

    def currentOid(self):
        repo_data = self.get_repo_data()
        commit_id = repo_data['props']['initialPayload']['refInfo']['currentOid']
        return commit_id

    def get_code_data(self, url):
        r = self.client.get(url)
        html = parse_html(r.text)
        code_data = html.xpath(_code_data_xpath_)[0]
        code_data = json.loads(code_data.text)
        return code_data

    def rawLines(self, url):
        code_data = self.get_code_data(url)
        code = code_data['payload']['blob']['rawLines']
        return code

    def list_dir(self, url):
        dir_data = self.get_code_data(url)
        items = dir_data['payload']['tree']['items']
        return items

    def get_file_lines(self, file):
        url = f'/blob/{self.branch}/{file}'
        lines = self.rawLines(url)
        return lines

    def get_dir_items(self, dir):
        url = f'/blob/{self.branch}/{dir}'
        items = self.list_dir(url)
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
