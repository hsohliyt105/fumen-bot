# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Literal
from traceback import format_exc

import discord
from py_fumen import decode, VersionException

from draw_four import draw_fumens
from functions import get_fumens, is_colour_code, urls_to_fumens
from tinyurl_api import make_tinyurl
import sql

class Commands(): 
    def __init__(self):
        return
    
    async def four(self, 
                   interaction: discord.Interaction | discord.Message, 
                   fumen_string: str, 
                   duration: float = 0.5, 
                   transparency: bool = True, 
                   background: str = None, 
                   theme: Literal["light", "dark"] = "dark", 
                   comment: bool = True):
        
        if isinstance(interaction, discord.Interaction):
            await interaction.response.defer()
            send = interaction.followup.send
        else:
            send = interaction.channel.send
        
        tinyurl_fumens = await urls_to_fumens(fumen_string)
        fumens = get_fumens(fumen_string)
        for fumen in tinyurl_fumens:
            fumens.append(fumen)
        fumens = list(set(fumens))

        images = []
        text = ""

        if not fumens:
            await send("Please input correct fumen / url / tinyurl! ")
            return

        for fumen in fumens:
            try:
                pages = decode(fumen)
            except (IndexError, VersionException):
                await send("Please input correct fumen / url / tinyurl! ")
                return

            if background and not is_colour_code(background):
                await send("Please input correct background colour! ")
                return

            if duration <= 0:
                await send("Please input correct duration! (duration > 0) ")
                return

            try:
                f = draw_fumens(pages, duration=int(duration*1000), transparency=transparency, theme=theme, background=background, is_comment=comment)

                image = discord.File(f)
                if len(pages) == 1:
                    image.filename = "image.png"
                else:
                    image.filename = "image.gif"

                tinyurl = ""
                if fumen not in tinyurl_fumens:
                    base_url = "https://knewjade.github.io/fumen-for-mobile/#?d="
                    print(base_url + fumen)
                    tinyurl = await make_tinyurl(base_url + fumen)
                else:
                    tinyurl = tinyurl_fumens[fumen]

                text += tinyurl + "\n"
                images.append(image)

            except Exception as e:
                await send("Error occured when creating and sending the image! *This error is automatically logged* ")
                with open("error.log", "a", encoding="utf-8") as error_log_f:
                    error_log_f.write(f"{datetime.now()} {format_exc()}")
                
        await send(text[:-1], files=images)
        return

    async def help(self, interaction: discord.Interaction | discord.Message):
        is_interaction = isinstance(interaction, discord.Interaction)

        if is_interaction:
            await interaction.response.defer()
            send = interaction.followup.send

        else:
            send = interaction.channel.send

        return

    async def sync(self, interaction: discord.Interaction, client: discord.Client, tree: discord.app_commands.CommandTree):
        if interaction.user == client.application.owner:
            await tree.sync(guild=interaction.guild)
            await interaction.response.send_message("Sync complete!", ephemeral=True)
        else:
            await interaction.response.send_message("This is only allowed for the owner of this bot!", ephemeral=True)

        return

    async def sync_all(self, interaction: discord.Interaction, client: discord.Client, tree: discord.app_commands.CommandTree):
        if interaction.user == client.application.owner:
            await tree.sync()
            await interaction.response.send_message("Sync complete!", ephemeral=True)
        else:
            await interaction.response.send_message("This is only allowed for the owner of this bot!", ephemeral=True)

        return

    async def set(self, interaction: discord.Interaction, auto: bool = None, duration: float = None, transparency: bool = None, background: str = None, theme: Literal["light", "dark"] = None, comment: bool = None):
        if background and not is_colour_code(background):
            await interaction.response.send("Please input correct background colour! ", ephemeral=True)
            return

        if duration and duration <= 0:
            await interaction.response.send("Please input correct duration! (duration > 0) ", ephemeral=True)
            return

        options = {
            'auto': auto,
            'duration': duration,
            'transparency': transparency,
            'background': background,
            'theme': theme,
            'comment': comment
        }

        sql.save_user(interaction.user, options)
        return