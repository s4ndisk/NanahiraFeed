import asyncio
import spotipy 
import os
import json
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_ARTIST_URI = os.getenv("SPOTIFY_ARTIST_URI")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

spotipy = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

album = spotipy.artist_albums(SPOTIFY_ARTIST_URI, album_type='album', limit=1)
single = spotipy.artist_albums(SPOTIFY_ARTIST_URI, album_type='single', limit=1)
album_appeared_on = spotipy.artist_albums(SPOTIFY_ARTIST_URI, album_type='appears_on', limit=1)

POLLING_INTERVAL = 60 * 5

def search_spotify_data(s_id):
    with open('ids.json', 'r') as file:
        data = json.load(file)
    
    for spotify_data in data['spotify']:
        spotify_id = spotify_data['spotify_id']
        if spotify_id in s_id:
            return True
    return False

def append_spotify_data(s_id, url):
    new_data = {"spotify_ids": s_id, "spotify_urls": url}
    with open('ids.json', 'r+') as file:
        data = json.load(file)
        data["spotify"].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)

async def latest_album():
    while True:
        album_id = album['id']
        album_url = album['external_urls']['spotify']
        if album_id:
            for s_id in album_id:
                if not search_spotify_data([album_id]):
                    append_spotify_data(album_id, album_url)
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New album found: {album_id}")
                    latest_album_url = album_url
                    return latest_album_url
        if latest_album_id == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No new albums found")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
        await asyncio.sleep(POLLING_INTERVAL)
        

async def latest_single():
    single_id = single['id']
    single_url = single['external_urls']['spotify']
    return single_url

async def latest_album_appeared_on():
    album_appeared_on_id = album_appeared_on['id']
    album_appeared_on_url = album_appeared_on['external_urls']['spotify']
    return album_appeared_on_url   
          
async def main():
    while True:
        await asyncio.gather(latest_album(), latest_single(), latest_album_appeared_on())
        asyncio.sleep(300)

if __name__ == "__main__":
    asyncio.run(main())
