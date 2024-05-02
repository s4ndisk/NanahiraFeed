import xtwitter 
import spotify
import asyncio
from datetime import datetime
from discord_webhook import DiscordWebhook

webhook_url = "https://discord.com/api/webhooks/1232155727229882491/BEQfpfu57WQZEahpppK6Af4JKxlm4XWFXImBoWTZWjOdqwY4YbUleR2Gbo9SyuSIMHRE"

def send_webhook(content):
  webhook = DiscordWebhook(url=webhook_url, content=content)
  webhook.execute()

async def xtwitter_webhook():
  latest_tweet_id = None
  while True:
    try:
      tweet_id = await xtwitter.get_latest_tweet_id()
      if tweet_id and tweet_id != latest_tweet_id:
        send_webhook(f"ななひら just tweeted!\n\nhttps://twitter.com/nanafeed_/status/{tweet_id}")
        latest_tweet_id = tweet_id
    
    except Exception as f:
      print(f"An error occurred in the XTwitter webhook: {f}")

    await asyncio.sleep(0)

async def spotify_webhook():
  latest_album_url = None
  latest_single_url = None
  latest_album_appeared_on_url = None
  while True:
    try:
      album_url = await spotify.get_latest_album()
      if album_url and album_url != latest_album_url:
        send_webhook(f"ななひら just released an album on Spotify!\n\n{album_url}")
        latest_album_url = album_url

      single_url = await spotify.get_latest_single()
      if single_url and single_url != latest_single_url:
        send_webhook(f"ななひら just released a single on Spotify!\n\n{single_url}")
        latest_single_url = single_url
      
      album_appeared_on_url = await spotify.get_latest_album_appeared_on()
      if album_appeared_on_url and album_appeared_on_url != latest_album_appeared_on_url:
        send_webhook(f"ななひら just appeared on an album on Spotify!\n\n{album_appeared_on_url}")
        latest_album_appeared_on_url = album_appeared_on_url
    
    except Exception as e:
      print(f"An error occurred in Spotify webhook: {e}")

    await asyncio.sleep(0)
      

async def main():
    await asyncio.gather(xtwitter.main(), xtwitter_webhook(), spotify.main(), spotify_webhook())

if __name__ == "__main__":
   asyncio.run(main())
