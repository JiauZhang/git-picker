import gitpicker.github as git
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--proxy', type=str, default=None, required=False)
args = parser.parse_args()

user = 'JiauZhang'
repo = 'git-picker'
branch = 'main'
files = {
    'dir': [
        'examples',
        'gitpicker',
    ],
    'file': [
        'LICENSE',
        'setup.py',
    ],
}

picker = git.GitHub(user, repo, branch, client_kwargs={'proxy': args.proxy})
picker.pick(files)
