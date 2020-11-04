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
    out = 'http://www.youtube.com/watch_videos?video_ids='
    for entry in playlist:
        for key in entry:
            if key == 'videoId':
                out+=(entry['videoId'] + ',')
    out = out[:-1]
    await ctx.send(out)

    


client.run('NzczMzM5MzY0NDQ0MjA5MTc0.X6HyaA.whMtIsCYhj-fYDmCeDpHHKewzBU')

