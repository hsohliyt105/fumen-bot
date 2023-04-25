# -*- coding: utf-8 -*-

from typing import Literal

import discord
from py_fumen import decode

from draw_four import draw_fumens
from functions import get_fumens, is_colour_code, get_tinyurls, write_error
from tinyurl_api import make_tinyurl
import sql

class Commands():
    async def four(interaction: discord.Interaction | discord.Message, fumen_string: str, duration: float = 0.5, transparency: bool = True, background: str = None, theme: Literal["light", "dark"] = "dark", comment: bool = True):
        is_interaction = isinstance(interaction, discord.Interaction)
        
        if is_interaction:
            await interaction.response.defer()
            send = interaction.followup.send

        else:
            send = interaction.channel.send
        
        fumens = get_fumens(fumen_string)
        tinyurls = get_tinyurls(fumen_string)
        tinyurl_fumens = None
        if tinyurls is not None:
            tinyurl_fumens = get_fumens(tinyurls)

        images = []
        text = ""

        if fumens is None:
            await send("Please input correct fumen / url / tinyurl! ", ephemeral=True)
            return

        for fumen in fumens:
            try:
                pages = decode(fumen)
            
            except:
                await send("Please input correct fumen / url / tinyurl! ", ephemeral=True)
                return

            if background is not None and not is_colour_code(background):
                await send("Please input correct background colour! ", ephemeral=True)
                return

            if duration <= 0:
                await send("Please input correct duration! (duration > 0) ", ephemeral=True)
                return

            try:
                f = draw_fumens(pages, duration=duration*1000, transparency=transparency, theme=theme, background=background, is_comment=comment)

                image = discord.File(f)
                if len(pages) == 1:
                    image.filename = "image.png"

                else:
                    image.filename = "image.gif"

                if tinyurls is None or not fumen in tinyurl_fumens:
                    base_url = "https://knewjade.github.io/fumen-for-mobile/#?d="
                    tinyurl = make_tinyurl(base_url + fumen)

                else:
                    for i in range(len(tinyurl_fumens)):
                        if tinyurl_fumens[i] == fumen:
                            tinyurl = tinyurls[i]

                text += tinyurl + "\n"

                images.append(image)

            except Exception as e:
                await send("Error occured when creating and sending the image! *This error is automatically logged* ")
                write_error(e)

        try:
            await send(text[:-1], files=images)

        except Exception as e:
            await send("Error occured when creating and sending the image! *This error is automatically logged* ")
            write_error(e)

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
