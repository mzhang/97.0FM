from ytmusicapi import YTMusic
import json
import discord

ytmusic = YTMusic()
search = ytmusic.search('aaaa', 'songs')

playlist = ytmusic.get_watch_playlist(search[0]['videoId'])
out = 'https://www.youtube.com/watch?v='

print(search[0]['thumbnails'][2]['url'])


for entry in playlist:
    for key in entry:
        if key == 'videoId':
            out+=(entry['videoId'] + ',')

print(f"```{out}```")