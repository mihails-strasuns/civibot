#!/bin/env python3
# pip3 install discord.py aiohttp

import os, discord
from discord.ext import commands
import aiohttp, aiodns, asyncio

################ Google Doc access & parsing ###################################

URL = 'BASE/gviz/tq?tqx=out:csv&sheet=Civ'

async def fetch_save_games (session):
    async with session.get(URL) as response:
        csv = await response.text()
        return parse_saves_csv(csv)

def parse_saves_csv (csv):
    result = {}
    lines = csv.splitlines()
    games = [game.strip('"') for game in lines[1].split(",") if game != '""']
    player_lines = [line.split(",") for line in lines[2:]]
    for i in range(0,len(games)):
        result[games[i]] = [line[0].strip('"') for line in player_lines
                            if line[i + 1] != '""']
        result[games[i]].sort()
    return result

################################################################################

client = commands.Bot(command_prefix='!')
session = None

@client.event
async def on_ready():
    global session
    session = aiohttp.ClientSession()
    print(f'{client.user} is ready')

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
    saves = await fetch_save_games(session)
    message = "\n".join(["- %s (%s)" % (name, " ".join(players))
                         for name,players in saves.items()])
    await ctx.send(message)


@saves.command(name='find', help='Lists all currently stored saved game record')
async def saves_find(ctx, *names):
    arr = [i for i in names]
    arr.sort()
    saves = await fetch_save_games(session)
    matching_saves = [name for name, players in saves.items() if players == arr]
    if len(matching_saves) > 0:
        message = "\n".join(["- %s" % name for name in matching_saves])
        await ctx.send(message)
    else:
        await ctx.send("No matching saves found")

TOKEN = os.getenv('DISCORD_CIVIBOT_TOKEN')
client.run(TOKEN)
