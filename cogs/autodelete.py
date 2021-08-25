import json
import os
from datetime import datetime
from random import *

import discord
from discord.ext import commands
from discord.utils import get
import datetime
from datetime import datetime
import random
from random import randint
import time
import asyncio
import math
import configparser
import sqlite3
import sys
from discord.ext.commands import CommandNotFound
from discord import Message
import re


embedColor = 0xe51ddf



class autodelete(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='autodelete')
    async def autodelete(self, ctx):
        if ctx.subcommand_passed is None:
            pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        global autod_channels
        with open("autodelete.json", "r") as file:
            autod_channels = json.load(file)
        if str(message.channel.id) not in autod_channels:
            return
        for delay in autod_channels[str(message.channel.id)]:
            await asyncio.sleep(delay)
            if not message.pinned:
                try:
                    await message.delete()
                except:
                    pass

    @autodelete.command()
    @commands.has_permissions(administrator=True)
    async def start(self, ctx: commands.Context, channel: discord.TextChannel, since):
        global delay
        seconds = ("s", "sec", "secs", 'second', "seconds")
        minutes = ("m", "min", "mins", "minute", "minutes")
        hours = ("h", "hour", "hours")
        days = ("d", "day", "days")
        weeks = ("w", "week", "weeks")
        try:
            temp = re.compile("([0-9]+)([a-zA-Z]+)")
            if not temp.match(since):
                await ctx.send("Du hast keine Zeiteinheiten angegeben, bitte versuche es erneut.")
                return
            res = temp.match(since).groups()
            time2 = int(res[0])
            since = res[1]
        except ValueError:
            await ctx.send("Du hast keine Zeiteinheiten angegeben, bitte versuche es erneut.")
            return
        if since.lower() in seconds:
            delay = time2
        elif since.lower() in minutes:
            delay = time2 * 60
        elif since.lower() in hours:
            delay = time2 * 3600
        elif since.lower() in days:
            delay = time2 * 86400
        elif since.lower() in weeks:
            delay = time2 * 604800
        if str(channel.id) in autod_channels:
            del autod_channels[str(ctx.channel.id)]
        autod_channels[str(channel.id)] = []
        autod_channels[str(channel.id)].append(delay)
        with open("autodelete.json", "w") as file:
            json.dump(autod_channels, file)
        embed = discord.Embed(title='AutoDelete',
                              description=f'**Der Kanal {channel.mention} wurde erfolgreich aktiviert**',
                              color=embedColor)
        await ctx.send(embed=embed)

    @autodelete.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx: commands.Context, channel: discord.TextChannel):
        global autod_channels
        with open("autodelete.json", "r") as file:
            autod_channels = json.load(file)
        if str(channel.id) not in autod_channels:
            embed = discord.Embed(title='AutoDelete',
                                  description=f'**{channel.mention} ist kein AutoDelete Kanal!**',
                                  color=embedColor)
            await ctx.send(embed=embed)
            return
        if str(channel.id) in autod_channels:
            del autod_channels[str(channel.id)]
        with open("autodelete.json", "w") as file:
            json.dump(autod_channels, file)
        embed = discord.Embed(title='AutoDelete',
                              description='**wurde erfolgreich deaktiviert!**',
                              color=embedColor)
        await ctx.send(embed=embed)

    @autodelete.command()
    @commands.has_permissions(administrator=True)
    async def delay(self, ctx: commands.Context, channel: discord.TextChannel):
        global autod_channels
        with open("autodelete.json", "r") as file:
            autod_channels = json.load(file)
        if str(channel.id) not in autod_channels:
            embed = discord.Embed(title='AutoDelete',
                                  description=f'**{channel.mention} ist kein AutoDelete Kanal!**',
                                  color=embedColor)
            await ctx.send(embed=embed)
            return
        if str(channel.id) in autod_channels:
            for delay in autod_channels[str(channel.id)]:
                embed = discord.Embed(title='AutoDelete',
                                      description=f'**Das Delay beträgt vom Channel {channel.mention} beträgt: `{delay} Sekunden`**',
                                      color=embedColor)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(autodelete(bot))
