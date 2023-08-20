# -*- coding: utf-8 -*-

import discord
from py_fumen import decode

from helper import FourDefault, FourSettings
from draw_four import draw_fumens
from functions import get_my_colour, is_colour_code, get_tinyurls, get_fumens, write_error, load_four_settings
from tinyurl_api import make_tinyurl
import sql

class Commands():
    async def four(interaction: discord.Interaction | discord.Message, fumen_string: str, settings: FourSettings = FourDefault()):
        user = interaction.user if isinstance(interaction, discord.Interaction) else interaction.author
        settings = load_four_settings(user, settings)
        
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
            await send("Please input correct fumen / url / tinyurl! ")
            return

        for fumen in fumens:
            try:
                pages = decode(fumen)
            
            except:
                await send("Please input correct fumen / url / tinyurl! ")
                return

            if not is_colour_code(settings.background):
                await send("Please input correct background colour! ")
                return

            if settings.duration <= 0:
                await send("Please input correct duration! (duration > 0) ")
                return

            try:
                f = draw_fumens(pages, duration=settings.duration*1000, transparency=settings.transparency, theme=settings.theme, background=settings.background, is_comment=settings.comment)

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

    async def set(interaction: discord.Interaction, settings: FourSettings = FourDefault()):
        await interaction.response.defer()
        settings = load_four_settings(interaction.user, settings)
        
        if not is_colour_code(settings.background):
            await interaction.followup.send("Please input correct background colour! ", ephemeral=True)
            return

        if settings.duration <= 0:
            await interaction.followup.send("Please input correct duration! (duration > 0) ", ephemeral=True)
            return

        sql.save_user(interaction.user, settings.auto, settings.duration, settings.transparency, settings.background, settings.theme, settings.comment)
        await interaction.followup.send("Setting complete! ", ephemeral=True)
        
        return

    async def set_delete(interaction: discord.Interaction):
        sql.delete_user(interaction.user)
        await interaction.response.send_message("Deleting complete! ", ephemeral=True)
        return

    async def set_check(interaction: discord.Interaction):
        settings_dict = sql.load_user(interaction.user)

        embed = discord.Embed(title=f"{interaction.user.display_name}'s Settings", colour=get_my_colour(interaction.client.user, interaction.channel))
        for key, value in settings_dict.items():
            embed.add_field(name=key, value=value)

        await interaction.response.send_message(embed=embed)
        return
