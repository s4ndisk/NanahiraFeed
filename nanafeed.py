import xtwitter 
import asyncio
from datetime import datetime
from discord_webhook import DiscordWebhook


POLLING_INTERVAL = 60 * 1

async def xtwitter_webhook():
  latest_tweet_id = None
  while True:
    tweet_id = await xtwitter.get_latest_tweet_id()
    if tweet_id and tweet_id != latest_tweet_id:
      webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1232155727229882491/BEQfpfu57WQZEahpppK6Af4JKxlm4XWFXImBoWTZWjOdqwY4YbUleR2Gbo9SyuSIMHRE", content=f"https://twitter.com/nanafeed_/status/{tweet_id}")
      webhook.execute()
      latest_tweet_id = tweet_id
    await asyncio.sleep(0)

async def main():
    await asyncio.gather(xtwitter.main(), xtwitter_webhook())

if __name__ == "__main__":
   asyncio.run(main())
