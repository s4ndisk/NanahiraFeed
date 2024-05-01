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

latest_album = spotipy.artist_albums(SPOTIFY_ARTIST_URI, album_type='album', limit=1)
latest_single = spotipy.artist_albums(SPOTIFY_ARTIST_URI, album_type='single', limit=1)
latest_album_appeared_in = spotipy.artist_albumes(SPOTIFY_ARTIST_URI, album_type='appears_on', limit=1)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()

