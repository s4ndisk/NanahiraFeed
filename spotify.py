import asyncio
import spotipy 
import os
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

async def latest_album():
    album_id = album['id']
    album_url = album['external_urls']['spotify']

async def latest_single():
    single_id = single['id']
    album_url = album['external_urls']['spotify']

async def latest_album_appeared_on():
   album_appeared_on_id = album_appeared_on['id']
   album_appeared_on_url = album_appeared_on['external_urls']['spotify']
                       
async def main():
    await asyncio.gather(latest_album(), latest_single(), latest_album_appeared_on())

if __name__ == "__main__":
    asyncio.run(main())
