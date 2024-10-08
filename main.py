# -*- coding: utf-8 -*-

"""
To do 

help command

turn on/off commands

  - setting to not respond automatically 

  - make my sql functions

work around to fix gif graphical errors

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
from helper import FourDefault, FourSettings
from functions import get_fumens, write_log_inter, write_log_message
from sql import load_user

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
                               background="Background colour in hex colour code (#xxxxxx)",
                               theme="Theme colour of background (if not specified,) annd minos",
                               comment="Whether to show the comment section")
async def four(interaction: discord.Interaction, fumen_string: str, duration: float = None, transparency: bool = None, background: str = None, theme: Literal["light", "dark"] = None, comment: bool = None):
    settings = FourSettings(duration=duration, transparency=transparency, background=background, theme=theme, comment=comment)
    await Commands.four(interaction, fumen_string, settings)
    return

@tree.command(name="set", description="Sets default options for the user")
@discord.app_commands.describe(auto="Whether to automatically respond to the user's fumen link. ", 
                               duration="Druration of each frame in seconds",
                               transparency="Transparency of the background, only available in png", 
                               background="Background colour in hex colour code (#xxxxxx). To default to the theme colour, type default. ",
                               theme="Theme colour of background (if not specified,) annd minos",
                               comment="Whether to show the comment section")
async def set(interaction: discord.Interaction, auto: bool = None, duration: float = None, transparency: bool = None, background: str = None, theme: Literal["light", "dark"] = None, comment: bool = None):
    settings = FourSettings(auto=auto, duration=duration, transparency=transparency, background=background, theme=theme, comment=comment)
    await Commands.set(interaction, settings)
    return

@tree.command(name="set_default", description="Restores options to default for the user")
async def set_default(interaction: discord.Interaction):
    await Commands.set(interaction, FourDefault())
    return

@tree.command(name="set_delete", description="Deletes the user settings in the database. for test.")
async def set_delete(interaction: discord.Interaction):
    await Commands.set_delete(interaction)
    return

@tree.command(name="set_check", description="Check the current settings")
async def set_delete(interaction: discord.Interaction):
    await Commands.set_check(interaction)
    return

@tree.command(name="sync", description="Syncs the commands in this guild, only for the owner of the bot")
async def sync(interaction: discord.Interaction):
    await Commands.sync(interaction, client, tree)
    return

@tree.command(name="sync_all", description="Syncs the commands globally, only for the owner of the bot")
async def sync_all(interaction: discord.Interaction):
    await Commands.sync_all(interaction, client, tree)
    return

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
            write_log_message(message)

        f = open("blacklist.txt", "r", encoding="utf-8")
        blacklist = f.read().split("\n")
        f.close()
        f = open("whitelist.txt", "r", encoding="utf-8")
        whitelist = f.read().split("\n")
        f.close()

        if str(message.author) not in whitelist and (message.author == client.user or message.author.bot or str(message.author) in blacklist):
            return

        if message.content.startswith("!four") or message.content.startswith("!help"):
            await message.channel.send("The commands with actual messages are depricated now. Please use the newer slash commands! ")
            write_log_message(message)

        else:
            fumens = get_fumens(message.content)

            if fumens is not None and (load_user(message.author) is None or load_user(message.author)['auto']):
                await Commands.four(message, message.content, FourSettings())

                write_log_message(message)

            return

    except discord.Forbidden:
        with open("error.log", "a", encoding="utf-8") as f:
            err_log = f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n{format_exc()}\n"
            f.write(err_log)
            f.close()
        await message.channel.send(f"A permission error occurred! Reinvite this bot via this link: https://discord.com/oauth2/authorize?client_id={client.application_id} *This error has been automatically logged.*")

    except:
        with open("error.log", "a", encoding="utf-8") as f:
            err_log = f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n{format_exc()}\n"
            f.write(err_log)
            f.close()
        await message.channel.send("An error occurred! *This error has been automatically logged.*")

    return

# Interaction events
@client.event
async def on_interaction(interaction: discord.Interaction):
    write_log_inter(interaction)
    return

client.run(DISCORD_TOKEN)
