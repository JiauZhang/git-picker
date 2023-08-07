import gtipicker as gp

repo = 'https://github.com/JiauZhang/git-picker'
files = {
    'dir': [
        'examples',
        'gitpicker',
    ],
    'file': [
        'LICENSE',
        "README.md",
    ],
}

gp.pick(repo, files)
