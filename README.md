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

picker = gp.GitHub(user, repo, branch, files)
picker.pick()
```

### Sponsor
<table align="center">
    <thead>
        <tr>
            <th colspan="2">公众号</th>
        </tr>
    </thead>
    <tbody align="center" valign="center">
        <tr>
            <td colspan="2"><img src="https://www.chatqkv.com/ghstatic/images/ofa_m.png" style="height: 196px" alt="AliPay.png"></td>
        </tr>
    </tbody>
    <thead>
        <tr>
            <th>AliPay</th>
            <th>WeChatPay</th>
        </tr>
    </thead>
    <tbody align="center" valign="center">
        <tr>
            <td><img src="https://www.chatqkv.com/AliPay.png" style="width: 196px; height: 196px" alt="AliPay.png"></td>
            <td><img src="https://www.chatqkv.com/WeChatPay.png" style="width: 196px; height: 196px" alt="WeChatPay.png"></td>
        </tr>
    </tbody>
</table>