import os
import asyncio
import spotipy 
import json
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_ARTIST_URI = os.getenv("SPOTIFY_ARTIST_URI")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

album = sp.artist_albums(SPOTIFY_ARTIST_URI, album_type='album', limit=1)
single = sp.artist_albums(SPOTIFY_ARTIST_URI, album_type='single', limit=1)
album_appeared_on = sp.artist_albums(SPOTIFY_ARTIST_URI, album_type='appears_on', limit=1)

POLLING_INTERVAL = 60 * 5

latest_album_url = None
latest_single_url = None
latest_album_appeared_on_url = None

async def get_latest_album():
    global latest_album_url
    return latest_album_url

async def get_latest_single():
    global latest_single_url
    return latest_single_url

async def get_latest_album_appeared_on():
    global latest_album_appeared_on_url
    return latest_album_appeared_on_url
    

def search_spotify_data(url):
    with open('ids.json', 'r') as file:
        data = json.load(file)
    
    for spotify_data in data['spotify']:
        spotify_url = spotify_data['spotify_url']
        if spotify_url in url:
            return True
    return False

def append_spotify_data(url, date):
    new_data = {"spotify_url": url, "spotify_date": date}
    with open('ids.json', 'r+') as file:
        data = json.load(file)
        data["spotify"].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)

async def latest_album():
    global latest_album_url
    while True:
        album_url = album['items'][0]['external_urls']['spotify']
        album_date = album['items'][0]['release_date']
        if album_url:
            for url in album_url:
                if not search_spotify_data([album_url]):
                    append_spotify_data(album_url, album_date)
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New album found: {album_url}")
                    latest_album_url = album_url
        if latest_album_url == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No new albums found")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
        await asyncio.sleep(POLLING_INTERVAL)
        

async def latest_single():
    global latest_single_url
    while True:
        single_url = single['items'][0]['external_urls']['spotify']
        single_date = single['items'][0]['release_date']
        if single_url:
            for url in single_url:
                if not search_spotify_data([single_url]):
                    append_spotify_data(single_url, single_date)
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New single found: {single_url}")
                    latest_single_url = single_url
        if latest_single_url == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No new singles found")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
        await asyncio.sleep(POLLING_INTERVAL)
   

async def latest_album_appeared_on():
    global latest_album_appeared_on_url
    while True:
        album_appeared_on_url = album_appeared_on['items'][0]['external_urls']['spotify']
        album_appeared_on_date = album_appeared_on['items'][0]['release_date']
        if album_appeared_on_url:
            for url in album_appeared_on_url:
                if not search_spotify_data([album_appeared_on_url]):
                    append_spotify_data(album_appeared_on_url, album_appeared_on_date)
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New album appeared on found: {album_appeared_on_url}")
                    latest_album_appeared_on_url = album_appeared_on_url
        if latest_album_appeared_on_url == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No new albums appeared on found")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
        await asyncio.sleep(POLLING_INTERVAL)
    
          
async def main():
    while True:
        await asyncio.gather(latest_album(), latest_single(), latest_album_appeared_on())

if __name__ == "__main__":
    asyncio.run(main())
