# -*- coding: utf-8 -*-

from typing import Optional
from re import findall
from datetime import datetime

from tinyurl_api import get_redirection
import discord

def get_fumen(string: str) -> Optional[str]:
    tinyurl = get_tinyurl(string)

    if tinyurl is not None:
        try:
            string += " " + get_redirection(tinyurl)

        except ValueError:
            pass
        
    found = findall('([vmd](110|115)@[\w+/?]+)', string)

    if len(found) > 0:
        return found[0][0]

    return None

def is_colour_code(string: str) -> bool:
    if string[0] != "#" or len(string) != 7:
        return False

    try:
        red = int(string[1:2], 16)
        green = int(string[3:4], 16)
        blue = int(string[5:6], 16)

        return True if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255 else False

    except:
       return False

def get_tinyurl(string: str) -> Optional[str]:
    found = findall('(https://(tinyurl\.com|tiny\.one|rotf\.lol)/[^ \n]*)', string)

    if len(found) > 0:
        return found[0][0]

    return None

def write_log_inter(interaction: discord.Interaction):
    with open("general.log", "a", encoding="utf-8") as general_log_f:
        general_log_f.write(f"{datetime.now()} {interaction.guild} {interaction.channel} {interaction.user} {interaction.data}\n")

def write_log_message(message: discord.Message):
    if len(message.embeds) > 0:
        with open("general.log", "a", encoding="utf-8") as general_log_f:
            general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content} title: {message.embeds[0].title} description: {message.embeds[0].description} fields: {message.embeds[0].fields} footer: {message.embeds[0].footer}\n")
    else: 
        with open("general.log", "a", encoding="utf-8") as general_log_f:
            general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n")