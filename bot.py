import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from ytmusicapi import YTMusic
from pprint import pprint

ytmusic = YTMusic()
client = commands.Bot(command_prefix = ".", help_command=None)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

splashQuotes = {"These are the songs that our Google overlords thinks are best for you!",
                "You have interesting taste!",
                "You might like these! I don't know. I'm just a robot.",
                "Weird album art, but great music!",
                "Don't blame me for your taste in music. I'm just a robot.",
                "99% Rickroll-free guaranteed. ",
                "If I had ears, this is what I'd listen to.",
                "Do not worry. Judging you is not yet an implemented feature.",
                "Groovy. Or something. I am not yet capable of measuring groovitude.",
                "I'm doing my best."
                }

@client.event
async def on_ready():
    print('aye aye captain')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='the same 3 songs over and over'))

@client.command()
async def beep(ctx):
    await ctx.send(f'boop {client.latency * 1000}')

@client.command()
async def help(ctx):
    await ctx.send("Give me some inspiration with `.s [song title]`!")

@client.command(aliases=['s'])
async def shortSearch(ctx, *, query):
    try:
        search = ytmusic.search(query, 'songs')
    
        playlist = ytmusic.get_watch_playlist(search[0]['videoId'])
        embed=discord.Embed(title=f"Here's a playlist with songs similar to {search[0]['title']} by {search[0]['artists'][0]['name']}:", description=random.choice(splashQuotes), color=0xae00ff)
        embed.set_thumbnail(url=search[0]['thumbnails'][0]['url'])

        out = 'http://www.youtube.com/watch_videos?video_ids='
        for entry in playlist['tracks']:
            for key in entry:
                if key == 'videoId':
                    out+=(entry['videoId'] + ',')
        out = '```' + out[:-1] + '```'
        embed.add_field(name="Triple-click and copy the following link!", value=out)
        await ctx.send(embed=embed)

    except:
        await ctx.send('A search for'+ """ `"""+query+"""` """ + 'yielded no results! Maybe try rephrasing the query?')
@client.command(aliases=['S'])
async def search(ctx, *, query):
    try:
        search = ytmusic.search(query, 'songs')
        playlist = ytmusic.get_watch_playlist(search[0]['videoId'])

        embed=discord.Embed(title="Here's a playlist based on your last song:", description=random.choice(splashQuotes), color=0xae00ff)
        embed.set_thumbnail(url=search[0]['thumbnails'][0]['url'])

        out = 'http://www.youtube.com/watch_videos?video_ids='
        index = 0

        for entry in playlist['tracks']:
            for key in entry:
                if key == 'videoId':
                    out+=(entry['videoId'] + ',')
                    index += 1
                    if index <= 24:
                        embed.add_field(name=entry['title'], value=f"[{entry['byline']} - {entry['length']}](https://www.youtube.com/watch?v={entry['videoId']})",inline=True)
        out = '```' + out[:-1] + '```'
        embed.add_field(name="Triple-click and copy the following link!", value=out, inline=False)

        await ctx.send(embed=embed)
    except:
        await ctx.send('A search for'+ """ `"""+query+"""` """ + 'yielded no results! Maybe try rephrasing the query?')
client.run(token)
