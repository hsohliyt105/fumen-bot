# -*- coding: utf-8 -*-

from urllib.request import urlopen

import requests

def get_redirection(url: str) -> str:
    r = urlopen(url)
    status_code = r.getcode()

    if status_code == 200 or 300 <= status_code < 310:
        return r.url

    raise ValueError

def make_tinyurl(url) -> str:
    params = {'url': url}

    r = requests.post("http://tinyurl.com/api-create.php?", params=params)

    if r.status_code == 200:
        return r.text

    raise Exception(r.reason)