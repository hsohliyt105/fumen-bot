# -*- coding: utf-8 -*-

from __future__ import annotations
from telnetlib import SE

from typing import Optional, List
from re import findall
from datetime import datetime
from helper import FourDefault

from tinyurl_api import get_redirection
import discord

import sql
from helper import FourSettings

def get_my_colour(user, channel):
    if isinstance(channel, discord.channel.DMChannel) or isinstance(channel, discord.channel.PartialMessageable):
        colour = discord.colour.Colour(0)
        return colour

    for member in channel.members:
        if user == member:
            colour = member.colour
            return colour

def get_tinyurls(string: str) -> List[str]:
    found = findall("(\(?https?://(tinyurl\.com|tiny\.one|rotf\.lol)/[;,/?:@&=+$\-_.!~*'()#A-z0-9]*)", string)
    result = []
    for i in range(len(found)):
        current = found[i][0].strip().strip("(").strip(")")
        if not current in result:
            result.append(current)
    return result

def get_fumens(string: str) -> List[str]:
    tinyurls = get_tinyurls(string)
    for tinyurl in tinyurls:
        try:
            string += " " + get_redirection(tinyurl)
        except ValueError:
            pass
        
    found = findall('([vmdVMD](110|115)@[\w+/?]+)', string)
    result = list(dict.fromkeys([found[i][0] for i in range(len(found))]))
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

#work on here

def load_four_settings(user: discord.User, settings: FourSettings) -> FourSettings:
    loaded_dict = sql.load_user(user)
        
    settings.auto = settings.auto if settings.auto is not None else (loaded_dict['auto'] if loaded_dict is not None and loaded_dict['auto'] is not None else FourDefault.auto)
    settings.duration = settings.duration if settings.duration is not None else (loaded_dict['duration'] if loaded_dict is not None and loaded_dict['duration'] is not None else FourDefault.duration)
    settings.transparency = settings.transparency if settings.transparency is not None else (loaded_dict['transparency'] if loaded_dict is not None and loaded_dict['transparency'] is not None else FourDefault.transparency)
    settings.background = settings.background.lower() if settings.background is not None else (loaded_dict['background'] if loaded_dict is not None and loaded_dict['background'] is not None else FourDefault.background)
    settings.theme = settings.theme.lower() if settings.theme is not None else (loaded_dict['theme'] if loaded_dict is not None and loaded_dict['theme'] is not None else FourDefault.theme)
    settings.comment = settings.comment if settings.comment is not None else (loaded_dict['comment'] if loaded_dict is not None and loaded_dict['comment'] is not None else FourDefault.comment)

    return settings

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