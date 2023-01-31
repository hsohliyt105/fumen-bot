# -*- coding: utf-8 -*-

from typing import Literal

import discord
from py_fumen import decode

from draw_four import draw_fumens
from functions import get_fumen, is_colour_code, get_tinyurl
from tinyurl_api import make_tinyurl

class Commands():
    async def four(interaction: discord.Interaction | discord.Message, fumen_string: str, duration: float = 0.5, transparency: bool = True, background: str = None, theme: Literal["light", "dark"] = "dark", comment: bool = True):
        is_interaction = isinstance(interaction, discord.Interaction)
    
        if is_interaction:
            send = interaction.followup.send

        else:
            send = interaction.channel.send
        
        fumen = get_fumen(fumen_string)
        tinyurl = get_tinyurl(fumen_string)

        try:
            pages = decode(fumen)
            
        except:
            await send("Please input correct fumen / url / tinyurl! ", ephemeral=True)
            return

        if background is not None and not is_colour_code(background):
            await send("Please input correct background colour! ", ephemeral=True)
            return
            
        if is_interaction:
            await interaction.response.defer()

        f = draw_fumens(pages, duration=duration*1000, transparency=transparency, theme=theme, background=background, is_comment=comment)

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

    async def sync(interaction: discord.Interaction, client: discord.Client, tree: discord.app_commands.CommandTree):
        if interaction.user == client.application.owner:
            await tree.sync(guild=interaction.guild)
            await interaction.response.send_message("Sync complete!", ephemeral=True)
        else:
            await interaction.response.send_message("This is only allowed for the owner of this bot!", ephemeral=True)

        return

    async def sync_all(interaction: discord.Interaction, client: discord.Client, tree: discord.app_commands.CommandTree):
        if interaction.user == client.application.owner:
            await tree.sync()
            await interaction.response.send_message("Sync complete!", ephemeral=True)
        else:
            await interaction.response.send_message("This is only allowed for the owner of this bot!", ephemeral=True)

        return
