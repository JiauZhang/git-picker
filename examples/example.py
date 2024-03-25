import gitpicker as gp
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

picker = gp.GitHub(user, repo, branch, files, proxy=args.proxy)
picker.pick()
