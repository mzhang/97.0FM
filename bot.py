import discord
from discord.ext import commands
from ytmusicapi import YTMusic

ytmusic = YTMusic()
client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    print('aye aye captain')

@client.command()
async def beep(ctx):
    await ctx.send(f'boop {client.latency * 1000}')

@client.command()
async def search(ctx, *, query):
    search = ytmusic.search(query, 'songs')[0]['videoId']
    

    await ctx.send(f'https://www.youtube.com/watch?v={search}')

    


client.run('NzczMzM5MzY0NDQ0MjA5MTc0.X6HyaA.whMtIsCYhj-fYDmCeDpHHKewzBU')

