# -*- coding: utf-8 -*-

import aiohttp

async def get_redirection(url: str) -> str:
    async with aiohttp.ClientSession() as session, session.get(url) as response:
        if response.status==200 or 300<=response.status<310:
            return str(response.real_url)
        raise Exception(response.reason)


async def make_tinyurl(url: str) -> str:
    tinyurl = "http://tinyurl.com/api-create.php?"
    params = {'url': url}
    async with aiohttp.ClientSession() as session, session.post(tinyurl, data=params) as response:
        if response.status==200:
            return await response.text()
        raise Exception(response.reason)
