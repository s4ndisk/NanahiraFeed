import xtwitter 
import os
import spotify
import youtube
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from discord_webhook import DiscordWebhook

load_dotenv()

webhook_url = os.getenv('DISCORD_WEBHOOK')

def send_webhook(content):
  webhook = DiscordWebhook(url=webhook_url, content=content)
  webhook.execute()

async def xtwitter_webhook():
  latest_tweet_id = None
  while True:
    try:
      tweet_id = await xtwitter.get_latest_tweet_id()
      if tweet_id and tweet_id != latest_tweet_id:
        send_webhook(f"ななひら tweeted!\n\nhttps://twitter.com/nanafeed_/status/{tweet_id}")
        latest_tweet_id = tweet_id
    
    except Exception as e:
      print(f"An error occurred in the XTwitter webhook: {e}")

    await asyncio.sleep(0)

async def spotify_webhook():
  latest_album_url = None
  latest_single_url = None
  latest_album_appeared_on_url = None
  while True:
    try:
      album_url = await spotify.get_latest_album()
      if album_url and album_url != latest_album_url:
        send_webhook(f"ななひら released an album on Spotify!\n\n{album_url}")
        latest_album_url = album_url

      single_url = await spotify.get_latest_single()
      if single_url and single_url != latest_single_url:
        send_webhook(f"ななひら released a single on Spotify!\n\n{single_url}")
        latest_single_url = single_url
      
      album_appeared_on_url = await spotify.get_latest_album_appeared_on()
      if album_appeared_on_url and album_appeared_on_url != latest_album_appeared_on_url:
        send_webhook(f"ななひら appeared on an album on Spotify!\n\n{album_appeared_on_url}")
        latest_album_appeared_on_url = album_appeared_on_url
    
    except Exception as f:
      print(f"An error occurred in Spotify webhook: {f}")

    await asyncio.sleep(0)

async def youtube_webhook():
  latest_video_url = None
  latest_stream_url = None
  while True:
    try:
      video_url = await youtube.get_latest_video()
      if video_url and video_url != latest_video_url:
        send_webhook(f"ななひら posted a video on Youtube!\n\n{video_url}")
        latest_video_url = video_url
      
      stream_url = await youtube.get_latest_stream()
      if stream_url and stream_url != latest_stream_url:
        send_webhook(f"ななひら went/is/was live on Youtube!\n\n{stream_url}")
        latest_stream_url = stream_url
    
    except Exception as g:
      print(f"An error occurred in Youtube webhook: {g}")
    
    await asyncio.sleep(0)
      

async def main():
    await asyncio.gather(xtwitter.main(), xtwitter_webhook(), spotify.main(), spotify_webhook(), youtube.main(), youtube_webhook())

if __name__ == "__main__":
   asyncio.run(main())
