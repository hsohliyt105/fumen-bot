# -*- coding: utf-8 -*-

from os import chdir, getenv
from os.path import abspath, dirname
from datetime import datetime
from asyncio import sleep
from traceback import format_exc

from discord import Intents, Client, Game, Forbidden, Message
from discord.ext import tasks
from dotenv import load_dotenv

import command
import helper
from functions import get_fumen

abs_path = abspath(__file__)
dir_name = dirname(abs_path)
chdir(dir_name)

with open("general.log", "a", encoding="utf-8") as general_log_f:
    general_log_f.write(f"{datetime.now()} Started.\n")

load_dotenv(encoding="UTF-8")
DISCORD_TOKEN = getenv("DISCORD_TOKEN") # TEST_TOKEN or DISCORD_TOKEN
CLIENT_ID = getenv("DISCORD_ID") #TEST_ID or DISCORD_ID

intents = Intents.default()
intents.messages = True
intents.message_content = True
intents.guild_messages = True
intents.dm_messages = True

client = Client(activity=Game("!help"), intents=intents)

# Presence change
@tasks.loop(seconds=(len(helper.command_list)+2)*helper.presence_time)
async def change_presence():
    for command in helper.command_list:
        client.activity = Game(f"!{command}")
        await sleep(helper.presence_time)
    client.activity = Game(helper.version)
    await sleep(helper.presence_time)
    client.activity = Game(f"working in {len(client.guilds)}")
    await sleep(helper.presence_time)

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
async def on_message(message: Message):
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

        if message.content.startswith("!"):
            string = message.content.split()

            if len(string[0]) > 1:
                string[0] = string[0][1:]
            else:
                return

            if string[0] in helper.command_list:
                if len(message.embeds) > 0:
                    with open("general.log", "a", encoding="utf-8") as general_log_f:
                        general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} title: {message.embeds[0].title} description: {message.embeds[0].description} fields: {message.embeds[0].fields} footer: {message.embeds[0].footer}\n")
                else: 
                    with open("general.log", "a", encoding="utf-8") as general_log_f:
                        general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n")

            if string[0] == "help":
                await command.help(message, string)
                return

            if string[0] == "four":
                await command.four(message, string)
                return

        else:
            fumen_found = get_fumen([message.content])

            if fumen_found is not None:
                await command.four(message, [message.content])

            if len(message.embeds) > 0:
                with open("general.log", "a", encoding="utf-8") as general_log_f:
                    general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} title: {message.embeds[0].title} description: {message.embeds[0].description} fields: {message.embeds[0].fields} footer: {message.embeds[0].footer}\n")
            else: 
                with open("general.log", "a", encoding="utf-8") as general_log_f:
                    general_log_f.write(f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n")

            return

    except Forbidden:
        with open("error.log", "a", encoding="utf-8") as f:
            err_log = f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n{format_exc()}\n"
            f.write(err_log)
            f.close()
        await message.channel.send(f"A permission error occurred! Reinvite this bot via this link: (https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&permissions=277025441856&scope=bot). *This error has been automatically logged.*")

    except:
        with open("error.log", "a", encoding="utf-8") as f:
            err_log = f"{datetime.now()} {message.guild} {message.channel} {message.author} {message.content}\n{format_exc()}\n"
            f.write(err_log)
            f.close()
        await message.channel.send("An error occurred! *This error has been automatically logged.*")

    return

client.run(DISCORD_TOKEN)
