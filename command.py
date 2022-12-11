# -*- coding: utf-8 -*-

from typing import List

from discord import Message, Embed, File
from py_fumen import decode

from helper import command_list, command_help
from draw_four import draw_fumens
from functions import get_fumen, get_options

async def help(message: Message, string: List[str]):
    if len(string) < 2:
        embed = Embed(title="List of commands")

        desc = ""
        
        for command in command_list:
            desc += f"`{command}`, "

        desc = desc[:-2]

        embed.description = desc

    else:
        command = string[1]
        
        if command in command_list:
            embed = Embed(title=command, description=command_help[command])

        else:
            await message.channel.send("There is no such command! ")
            return

    await message.channel.send(embed=embed)
    return
    
async def four(message: Message, string: List[str]): 
    duration = 500
    transparent = True
    theme = "dark"

    fumen = get_fumen(string)
    options = get_options(string)

    if fumen is None:
        await message.channel.send("Please include a fumen string! command format: `!image <fumen string> [delay per page in seconds, default=0.5]`")
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

    try:
        pages = decode(fumen)

    except:
        await message.channel.send("Unsupported fumen string! ")
        return

    try:
        f = draw_fumens(pages, duration=duration, transparent=transparent, theme=theme)

    except ValueError:
        await message.channel.send("Some input is wrong! Please try again. If you think this is a bug, report to 적절한사람#2009. ")
        return

    image = File(f)
    if len(pages) == 1:
        image.filename = "image.png"
    else:
        image.filename = "image.gif"

    await message.channel.send(file=image)

    return
