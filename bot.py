import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from ytmusicapi import YTMusic
from pprint import pprint
import random
ytmusic = YTMusic()
client = commands.Bot(command_prefix = ".", help_command=None)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

splashQuotes = ["These are the songs that our Google overlords thinks are best for you!",
                "You have interesting taste!",
                "You might like these! I don't know. I'm just a robot.",
                "Weird album art, but great music!",
                "Don't blame me for your taste in music. I'm just a robot.",
                "I operate on a 99% Rickroll-free guarantee.",
                "If I had ears, this is what I'd listen to.",
                "Do not worry. Judging you is not yet an implemented feature.",
                "Groovy. Or something. I am not yet capable of measuring groovitude.",
                "I'm doing my best. Music is hard for robots!"
            ]

@client.event
async def on_ready():
    print('aye aye captain')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='the same 3 songs over and over'))

@client.command()
async def beep(ctx):
    await ctx.send(f'boop {client.latency * 1000}')

@client.command()
async def help(ctx):
    embed=discord.Embed(title="Give me a song and I'll give you a playlist.")
    embed.add_field(name="Feeling lucky? ", value="Give me some inspiration with `.search [song title]`. Or just `.s [title]`", inline=False)
    embed.add_field(name="Don't trust me?", value="Try `.fullSearch [song title]`. `.S [title]` or `.fs [title]` also work.", inline=False)
    embed.set_footer(text="Beep boop beep boop. Stop listening on loop.")
    await ctx.send(embed=embed)

@client.command(aliases=['s'])
async def search(ctx, *, query):
    try:
        search = ytmusic.search(query, 'songs')
    
        playlist = ytmusic.get_watch_playlist(search[0]['videoId'])
        embed=discord.Embed(title=f"Here's a playlist with songs similar to `{search[0]['title']}` by `{search[0]['artists'][0]['name']}`:", description=random.choice(splashQuotes), color=0xae00ff)
        embed.set_thumbnail(url=search[0]['thumbnails'][0]['url'])

        out = 'http://www.youtube.com/watch_videos?video_ids='
        for entry in playlist['tracks']:
            for key in entry:
                if key == 'videoId':
                    out+=(entry['videoId'] + ',')
        out = '```' + out[:-1] + '```'
        embed.add_field(name="Triple-click and copy the following link!", value=out)
        await ctx.send(embed=embed)

    except Exception as e:
        print(e)
        await ctx.send('A search for'+ """ `"""+query+"""` """ + 'yielded no results! Maybe try rephrasing the query?')
@client.command(aliases=['S','fs'])
async def fullSearch(ctx, *, query):
    try:
        search = ytmusic.search(query, 'songs')
        playlist = ytmusic.get_watch_playlist(search[0]['videoId'])

        embed=discord.Embed(title=f"Here's a playlist with songs similar to `{search[0]['title']}` by `{search[0]['artists'][0]['name']}`:", description=random.choice(splashQuotes), color=0xae00ff)
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
    except Exception as e:
        print(e)
        await ctx.send('A search for'+ """ `"""+query+"""` """ + 'yielded no results! Maybe try rephrasing the query?')

from youtube_dl import YoutubeDL
from requests import get

#Get videos from links or from youtube search
def search(query):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
        try: requests.get(query)
        except: info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        else: info = ydl.extract_info(query, download=False)
    return (info, info['formats'][0]['url'])

async def join(ctx, voice):
    channel = ctx.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect() 
        return voice

from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    await voice.disconnect()

@client.command()
async def play(ctx, *, query):
    FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    video, source = search(query)
    voice = get(client.voice_clients, guild=ctx.guild)

    voice = await join(ctx, voice)
    await ctx.send(f'Now live! {random.choice(splashQuotes)}')

    voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
    voice.is_playing()

client.run(token)
