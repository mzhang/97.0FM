from ytmusicapi import YTMusic
import json

ytmusic = YTMusic()
search = ytmusic.search('aaaa', 'songs')
playlist = ytmusic.create_playlist('a','a')
ytmusic.add_playlist_items(playlist, [search])
print(playlist)


