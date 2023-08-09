### Install
```shell
pip install git-picker
```

### Usage
```python
import gitpicker as gp

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

picker = gp.Picker(user, repo, branch, files)
picker.pick()
```
