# -*- coding: utf-8 -*-

from typing import Optional, List, Dict
from re import findall
from datetime import datetime

import discord

from tinyurl_api import get_redirection
import sql

def get_my_colour(user, channel):
    if isinstance(channel, discord.channel.DMChannel) or isinstance(channel, discord.channel.PartialMessageable):
        colour = discord.colour.Colour(0)
        return colour

    for member in channel.members:
        if user == member:
            colour = member.colour
            return colour



async def urls_to_fumens(string: str) -> Dict:
    found = findall("(\(?https?://(tinyurl\.com|tiny\.one|rotf\.lol)/[;,/?:@&=+$\-_.!~*'()#A-z0-9]*)", string)
    urls = [result[0].strip().strip("(").strip(")") for result in found]
    
    fumens = {}
    for url in urls:
        try:
            redir = await get_redirection(url)
            found = findall('([vmdVMD](110|115)@[\w+/?]+)', redir)
            fumens[found[0][0]] = url
        except ValueError:
            pass
    return fumens

def get_fumens(string: str) -> List[str]:
    found = findall('([vmdVMD](110|115)@[\w+/?]+)', string)
    result = list(set([found[i][0] for i in range(len(found))]))
    return result

def is_colour_code(string: str) -> bool:
    if string == "default":
        return True

    if string[0] != "#" or (len(string) != 7 and len(string) != 9):
        return False

    try:
        red = int(string[1:2], 16)
        green = int(string[3:4], 16)
        blue = int(string[5:6], 16)
        alpha = 255
        if len(string) == 9:
            alpha = int(string[7:8], 16)
        return True if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255 and 0 <= alpha <= 255 else False

    except ValueError:
       return False

def write_log(message: discord.Message | discord.Interaction):
    time = datetime.now()
    guild = message.guild
    channel = message.channel
    embed = ""

    if isinstance(message, discord.Interaction):
        author = message.user
        content = message.data

    else:
        author = message.author
        content = message.content
        if len(message.embeds) > 0:
            for i, em in enumerate(message.embeds):
                embed += "\n    Embed {i} - title: {em.title} description: {em.description} fields: {em.fields} footer: {em.footer}"

    with open("general.log", "a", encoding="utf-8") as general_log_f:
        general_log_f.write(f"{time} {guild} {channel} {author} {content} {embed}\n")

    return