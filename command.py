# -*- coding: utf-8 -*-

from typing import List

from discord import Message, Embed, File
from py_fumen import decode

from helper import command_list, command_help, command_option
from draw_four import draw_fumens
from functions import get_fumen, get_options, is_colour_code, get_tinyurl
from tinyurl_api import make_tinyurl

async def help(message: Message, strings: List[str]):
    if len(strings) < 2:
        embed = Embed(title="List of commands")

        desc = ""
        
        for command in command_list:
            desc += f"`{command}`, "

        desc = desc[:-2]

        desc += f"\n`!help [command]` for more information. "

        embed.description = desc

    else:
        command = strings[1]
        
        if command in command_list:
            embed = Embed(title=command, description=command_help[command])
            embed.add_field(name="options", value=command_option[command])

        else:
            await message.channel.send("There is no such command! ")
            return

    await message.channel.send(embed=embed)
    return
    
async def four(message: Message, strings: List[str]): 
    duration = 500
    transparent = True
    theme = "dark"
    background = None

    fumen = get_fumen(strings)
    tinyurl = get_tinyurl(strings)
    options = get_options(strings)

    if fumen is None:
        await message.channel.send("Please include a fumen string! `!help four` for more information.")
        return

    if 'duration' in options or 'd' in options:
        key = 'd' if 'd' in options else 'duration'
        value = options[key]

        try:
            duration = float(value) * 1000
        
        except ValueError:
            await message.channel.send("Duration option must be in decimal! ")
            return

    if 'transparent' in options or 't' in options:
        key = 't' if 't' in options else 'transparent'
        value = options[key]
        
        transparent = True if value in [ "y", "yes" ] else False if value in [ "n", "no" ] else None

        if transparent is None:
            await message.channel.send("Transparent option must be yes (y) or no (n)! ")
            return

    if 'theme' in options:
        key = 'theme'
        value = options[key]

        if value in [ "dark", "light" ]:
            theme = value

        else:
            await message.channel.send("Theme option must be dark or light! ")
            return

    if 'background' in options or 'b' in options:
        key = 'b' if 'b' in options else 'background'
        value = options[key]

        if is_colour_code(value):
            background = value

        else:
            await message.channel.send("Wrong colour code! ")
            return

    if 'comment' in options or 'c' in options:
        key = 'c' if 'c' in options else 'comment'
        value = options[key]

        display_comment = True if value in [ "y", "yes" ] else False if value in [ "n", "no" ] else None

        if display_comment is None:
            await message.channel.send("Comment option must be yes (y) or no (n)! ")
            return

    try:
        pages = decode(fumen)

    except:
        await message.channel.send("Unsupported fumen string! ")
        return

    try:
        f = draw_fumens(pages, duration=duration, transparent=transparent, theme=theme, background=background, is_comment=display_comment)

    except ValueError:
        await message.channel.send("Some input is wrong! Please try again. If you think this is a bug, report to 적절한사람#2009. ")
        return

    image = File(f)
    if len(pages) == 1:
        image.filename = "image.png"
    else:
        image.filename = "image.gif"

    if tinyurl is None or get_fumen([tinyurl]) != fumen:
        base_url = "https://knewjade.github.io/fumen-for-mobile/#?d="
        tinyurl = make_tinyurl(base_url + fumen)

    await message.channel.send(tinyurl ,file=image)

    return
