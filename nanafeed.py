import xtwitter 
import spotify
import asyncio
from datetime import datetime
from discord_webhook import DiscordWebhook

webhook_url = "https://discord.com/api/webhooks/1232155727229882491/BEQfpfu57WQZEahpppK6Af4JKxlm4XWFXImBoWTZWjOdqwY4YbUleR2Gbo9SyuSIMHRE"

async def xtwitter_webhook():
  latest_tweet_id = None
  while True:
    tweet_id = await xtwitter.get_latest_tweet_id()
    if tweet_id and tweet_id != latest_tweet_id:
      webhook = DiscordWebhook(url=webhook_url, content=f"ななひら just tweeted!\n\nhttps://twitter.com/nanafeed_/status/{tweet_id}")
      webhook.execute()
      latest_tweet_id = tweet_id
    await asyncio.sleep(0)

## needs testing
async def spotify_webhook():
   latest_album_url = None
   latest_single_url = None
   latest_album_appeared_on_url = None
   while True:
      album_url = await spotify.latest_album()
      if album_url and album_url != latest_album_url:
        webhook = DiscordWebhook(url=webhook_url, content=f"ななひら just released an album on Spotify!\n\n{album_url}")
        webhook.execute()
        latest_album_url = album_url
      await asyncio.sleep(5)
      single_url = await spotify.latest_single()
      if single_url and single_url != latest_single_url:
        webhook = DiscordWebhook(url=webhook_url, content=f"ななひら just released a single on Spotify!\n\n{single_url}")
        webhook.execute()
        latest_single_url = single_url
      await asyncio.sleep(5)
      album_appeared_on_url = await spotify.latest_album_appeared_on()
      if album_appeared_on_url and album_appeared_on_url != latest_album_appeared_on_url:
        webhook = DiscordWebhook(url=webhook_url, content=f"ななひら just appeared on an album on Spotify!\n\n{album_appeared_on_url}")
        webhook.execute()
        latest_album_appeared_on_url = album_appeared_on_url
      await asyncio.sleep(0)
      

async def main():
    await asyncio.gather(xtwitter.main(), xtwitter_webhook())

if __name__ == "__main__":
   asyncio.run(main())
