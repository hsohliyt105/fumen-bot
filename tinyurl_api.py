# -*- coding: utf-8 -*-

from os import chdir, getenv
from os.path import abspath, dirname

from dotenv import load_dotenv
from requests import get

abs_path = abspath(__file__)
dir_name = dirname(abs_path)
chdir(dir_name)

load_dotenv(encoding="UTF-8")

TINYURL_TOKEN = getenv("TINYURL_TOKEN")

base = "https://api.tinyurl.com"

def get_alias(alias: str) -> str:
    params = { 
        'api_token': TINYURL_TOKEN
        }

    r = get(f"{base}/alias/{alias}", params=params)

    if r.status_code == 200:
        return r.json()['data']['url']

    else:
        raise ValueError