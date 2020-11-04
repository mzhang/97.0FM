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
    search = ytmusic.search(query, 'songs')
    playlist = ytmusic.get_watch_playlist(search[0]['videoId'])
    await ctx.send(playlist[0])

    


client.run('NzczMzM5MzY0NDQ0MjA5MTc0.X6HyaA.whMtIsCYhj-fYDmCeDpHHKewzBU')

