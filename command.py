# -*- coding: utf-8 -*-

from typing import List, Literal

import discord
from py_fumen import decode

from draw_four import draw_fumens
from functions import get_fumen, is_colour_code, get_tinyurl
from tinyurl_api import make_tinyurl

class Commands():
    async def four(interaction: discord.Interaction | discord.Message, fumen_string: str, duration: float = 0.5, transparency: bool = True, background: str = None, theme: Literal["light", "dark"] = "dark", comment: bool = True): 
        if isinstance(interaction, discord.Interaction):
            send = interaction.response.send_message

        if isinstance(interaction, discord.Message):
            send = interaction.channel.send
        
        fumen = get_fumen(fumen_string)
        tinyurl = get_tinyurl(fumen_string)

        try:
            pages = decode(fumen)
        except:
            await send("Please input correct fumen / url / tinyurl! ")
            return

        if background is not None and not is_colour_code(background):
            await send("Please input correct background colour! ")
            return

        f = draw_fumens(pages, duration=duration*1000, transparent=transparency, theme=theme, background=background, is_comment=comment)

        image = discord.File(f)
        if len(pages) == 1:
            image.filename = "image.png"

        else:
            image.filename = "image.gif"

        if tinyurl is None or get_fumen(tinyurl) != fumen:
            base_url = "https://knewjade.github.io/fumen-for-mobile/#?d="
            tinyurl = make_tinyurl(base_url + fumen)

        await send(tinyurl, file=image)

        return
