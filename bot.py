import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from ytmusicapi import YTMusic
 
ytmusic = YTMusic()
client = commands.Bot(command_prefix = ".")

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print('aye aye captain')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='the same 3 songs over and over'))

@client.command()
async def beep(ctx):
    await ctx.send(f'boop {client.latency * 1000}')

@client.command(aliases=['s', 'S'])
async def search(ctx, *, query):
    search = ytmusic.search(query, 'songs')
    playlist = ytmusic.get_watch_playlist(search[0]['videoId'])
    
    embed=discord.Embed(title="Here's a playlist based on your last song:", description="These are the songs that our Google overlords thinks is best for you! ", color=0xae00ff)
    embed.set_thumbnail(url=search[0]['thumbnails'][2]['url'])
    
    out = 'http://www.youtube.com/watch_videos?video_ids='
    recommendedSongs = ''
    for entry in playlist:
        for key in entry:
            if key == 'videoId':
                out+=(entry['videoId'] + ',')
                recommendedSongs += '[%s](%s)\n' % (entry['title'],"https://www.youtube.com/watch?v="+entry['videoId']) 
    out = '```' + out[:-1] + '```'
    embed.add_field(name="Triple-click and copy the following link!", value=out)
    await ctx.send(embed=embed)

client.run(token)