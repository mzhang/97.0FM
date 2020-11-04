from ytmusicapi import YTMusic
import json

ytmusic = YTMusic()
search = ytmusic.search('aaaa', 'songs')
# playlist = ytmusic.create_playlist('a','a')
# ytmusic.add_playlist_items(playlist, [search])

playlist = ytmusic.get_watch_playlist(search[0]['videoId'])


print(playlist)


