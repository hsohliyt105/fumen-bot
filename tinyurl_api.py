# -*- coding: utf-8 -*-

from urllib.request import urlopen

def get_redirection(url) -> str:
    r = urlopen(url)
    status_code = r.getcode()

    if status_code == 200 or 300 <= status_code < 310:
        return r.url

    raise ValueError
