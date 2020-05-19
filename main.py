#!/bin/env python3
# pip3 install discord.py aiosqlite

import os, discord, aiosqlite
from discord.ext import commands

client = commands.Bot(command_prefix='!')
db = None

@client.event
async def on_ready():
    print(f'{client.user} has connected, waiting for the DB..')
    global db
    db = await aiosqlite.connect('civibot.db')
    print(f'DB connection ready')

@client.command(help='Arranges mentioned players into two teams')
async def teams(ctx, *names):
    arr = [i for i in names]
    import random
    random.shuffle(arr)
    m = int(len(arr) / 2)
    team1 = ", ".join(arr[:m])
    team2 = ", ".join(arr[m:])
    await ctx.send("Team 1: %s\nTeam 2: %s" % (team1, team2))

@client.group(help='Savegame management utils')
async def saves(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send_help(saves)

@saves.command(name='list', help='Lists all currently stored saved game record')
async def saves_list(ctx):
    cursor = await db.execute('SELECT host, description FROM saved_games')
    rows = await cursor.fetchall()
    await cursor.close()
    message = "\n".join(["- %s (hosted by @%s)" % (row[1], row[0])
                         for row in rows])
    await ctx.send(message)

TOKEN = os.getenv('DISCORD_CIVIBOT_TOKEN')
client.run(TOKEN)
