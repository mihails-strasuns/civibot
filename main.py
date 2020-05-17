#!/bin/env python3
# pip3 install discord.py

import os, discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'{client.user} has connected')

@client.command(name='teams', help='Arranges mentioned players into two teams')
async def teams(ctx, *names):
    arr = [i for i in names]
    import random
    random.shuffle(arr)
    m = int(len(arr) / 2)
    team1 = ", ".join(arr[:m])
    team2 = ", ".join(arr[m:])
    await ctx.send("Team 1: %s\nTeam 2: %s" % (team1, team2))

TOKEN = os.getenv('DISCORD_CIVIBOT_TOKEN')
client.run(TOKEN)
