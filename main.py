# -*- coding: utf-8 -*-

"""
To do 

make my sql functions

opener library 

perfect clear library
"""

from os import chdir, getenv
from os.path import abspath, dirname
from datetime import datetime
from asyncio import sleep
from traceback import format_exc
from typing import Literal

import discord
from discord.ext import tasks
from dotenv import load_dotenv

from command import Commands
import helper
from functions import get_fumen, get_tinyurl

abs_path = abspath(__file__)
dir_name = dirname(abs_path)
chdir(dir_name)

with open("general.log", "a", encoding="utf-8") as general_log_f:
    general_log_f.write(f"{datetime.now()} Started.\n")

load_dotenv(encoding="UTF-8")
DISCORD_TOKEN = getenv("DISCORD_TOKEN") # TEST_TOKEN or DISCORD_TOKEN

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guild_messages = True
intents.dm_messages = True

client = discord.Client(intents=intents)

tree = discord.app_commands.CommandTree(client)

# Presence change 
@tasks.loop(seconds=(2*helper.presence_time))
async def change_presence():
    client.activity = discord.Game(helper.version)
    await sleep(helper.presence_time)
    client.activity = discord.Game(f"working in {len(client.guilds)}")
    await sleep(helper.presence_time)

@tree.command(name="four", description="Sends an four formatted image containing the fumen")
@discord.app_commands.describe(fumen_string="The fumen / url / tinyurl to display", 
                               duration="Druration of each frame in seconds",
                               transparency="Transparency of the background, only available in png", 
                               background="Background colour in hex colour code",
                               theme="Theme colour of background (if not specified,) annd minos",
                               comment="Whether to show the comment section")
async def four(interaction: discord.Interaction, fumen_string: str, duration: float = 0.5, transparency: bool = True, background: str = None, theme: Literal["light", "dark"] = "dark", comment: bool = True):
    await Commands.four(interaction, fumen_string, duration, transparency, background, theme, comment)

    return

@tree.command(name="sync", description="Syncs the commands in this guild")
async def sync(interaction: discord.Interaction):
    if interaction.user == client.application.owner:
        await tree.sync(guild=interaction.guild)
        await interaction.response.send_message("Sync complete!", ephemeral=True)
    else:
        await interaction.response.send_message("This is only allowed for the owner of this bot!", ephemeral=True)

@tree.command(name="sync_all", description="Syncs the commands globally")
async def sync_all(interaction: discord.Interaction):
    if interaction.user == client.application.owner:
        await tree.sync()
        await interaction.response.send_message("Sync complete!", ephemeral=True)
    else:
        await interaction.response.send_message("This is only allowed for the owner of this bot!", ephemeral=True)

# Start up
@client.event
async def on_ready():
    print(f"{client.user} has been connected. ")

    for guild in client.guilds:
        print(guild.name)

    print(len(client.guilds))

    try:
        await change_presence.start()
        return
    except:
        return

# Message events
@client.event
async def on_message(message: discord.Message):
    try:
        if message.author == client.user:
            if len(message.embeds) > 0:
                with open("general.log", "a", encoding="utf-8") as general_log_f:
                    general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} title: {message.embeds[0].title} description: {message.embeds[0].description} fields: {message.embeds[0].fields} footer: {message.embeds[0].footer}\n")
            else: 
                with open("general.log", "a", encoding="utf-8") as general_log_f:
                    general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n")
        
        if message.author == client.user or message.author.bot:
            return

        if message.content.startswith("!four") or message.content.startswith("!help"):
            await message.channel.send("The commands with actual messages are depricated now. Please use the newer slash commands! ")

        else:
            fumen_found = get_fumen(message.content)
            tinyurl = get_tinyurl(message.content)

            if fumen_found is not None:
                if fumen_found == get_fumen(tinyurl):
                    fumen_found = tinyurl

                await Commands.four(message, fumen_found)

            if len(message.embeds) > 0:
                with open("general.log", "a", encoding="utf-8") as general_log_f:
                    general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} title: {message.embeds[0].title} description: {message.embeds[0].description} fields: {message.embeds[0].fields} footer: {message.embeds[0].footer}\n")
            else: 
                with open("general.log", "a", encoding="utf-8") as general_log_f:
                    general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n")

            return

    except discord.Forbidden:
        with open("error.log", "a", encoding="utf-8") as f:
            err_log = f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n{format_exc()}\n"
            f.write(err_log)
            f.close()
        await message.channel.send(f"A permission error occurred! Reinvite this bot via this link: (https://discord.com/oauth2/authorize?client_id={client.application_id} *This error has been automatically logged.*")

    except:
        with open("error.log", "a", encoding="utf-8") as f:
            err_log = f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n{format_exc()}\n"
            f.write(err_log)
            f.close()
        await message.channel.send("An error occurred! *This error has been automatically logged.*")

    return

client.run(DISCORD_TOKEN)
