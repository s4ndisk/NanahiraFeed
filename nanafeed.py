import xtwitter 
import os
import spotify
import youtube
import asyncio
import json
from dotenv import load_dotenv
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

load_dotenv()

webhook_url = os.getenv('DISCORD_WEBHOOK')
USER_ID = os.getenv('USER_ID')

def create_ids_db():
  data = {
    "xtwitter": [],
    "spotify": [],
    "youtube": []
  }

  file_path = "ids.json"

  if not os.path.exists(file_path):
    with open(file_path, "w") as json_file:
      json.dump(data, json_file)
    print("Creating database file for IDs at:", file_path)
  else:
    print("Database file for IDs already exists. Continuing")

async def xtwitter_webhook():
  latest_tweet_id = None
  while True:
    try:
      tweet_id = await xtwitter.get_latest_tweet_id()
      if tweet_id and tweet_id != latest_tweet_id:
        tweet_user_pfp = await xtwitter.get_profile_picture()
        tweet_text = await xtwitter.get_tweet_text()
        tweet_media_url = await xtwitter.get_tweet_media_url(tweet_id)
        tweet_url = f"https://twitter.com/{USER_ID}/status/{tweet_id}"
        embed = DiscordEmbed(
          description=f"ななひら tweeted on X/Twitter\n\n{tweet_text}"
        )
        embed.set_author(name='ななひら - X/Twitter', url=tweet_url)
        embed.set_thumbnail(url=tweet_user_pfp)
        embed.set_image(tweet_media_url)
        embedhook = DiscordWebhook(url=webhook_url)
        embedhook.add_embed(embed)
        embedhook.execute()
        latest_tweet_id = tweet_id
    
    except Exception as e:
      print(f"An error occurred in the XTwitter webhook: {e}")
      await asyncio.sleep(400)

    await asyncio.sleep(0)

async def album_spotify():
  global latest_album
  album = await spotify.get_latest_album()
  if album:
    album_url = album['items'][0]['external_urls']['spotify']
    album_name = album['items'][0]['name']
    album_cover_url = album['items'][0]['images'][0]['url']
    embed = DiscordEmbed(
      description=f"ななひら uploaded an album on Spotify\n\n**{album_name}**"
    )
    embed.set_author(name="ななひら - Spotify", url=album_url)
    embed.set_image(url=album_cover_url)
    embedhook = DiscordWebhook(url=webhook_url)
    embedhook.add_embed(embed)
    if album and album != latest_album:
      embedhook.execute()
      latest_album = album
    
async def single_spotify():
  global latest_single
  single = await spotify.get_latest_single()
  if single:
    single_url = single['items'][0]['external_urls']['spotify']
    single_name = single['items'][0]['name']
    single_cover_url = single['items'][0]['images'][0]['url']
    embed = DiscordEmbed(
      description=f"ななひら uploaded a single on Spotify\n\n**{single_name}**"
    )
    embed.set_author(name="ななひら - Spotify", url=single_url)
    embed.set_image(url=single_cover_url)
    embedhook = DiscordWebhook(url=webhook_url)
    embedhook.add_embed(embed)
    if single and single != latest_single:
      embedhook.execute()
      latest_single = single

async def album_appeared_on_spotify():
  global latest_album_appeared_on
  album_appeared_on = await spotify.get_latest_album_appeared_on()
  if album_appeared_on:
    album_appeared_on_url = album_appeared_on['items'][0]['external_urls']['spotify']
    album_appeared_on_name = album_appeared_on['items'][0]['name']
    album_appeared_on_cover_url = album_appeared_on['items'][0]['images'][0]['url']
    embed = DiscordEmbed(
      description=f"ななひら appeared on an album on Spotify\n\n**{album_appeared_on_name}**"
    )
    embed.set_author(name="ななひら - Spotify", url=album_appeared_on_url)
    embed.set_image(url=album_appeared_on_cover_url)
    embedhook = DiscordWebhook(url=webhook_url)
    embedhook.add_embed(embed)
    if album_appeared_on and album_appeared_on != latest_album_appeared_on:
      embedhook.execute()
      latest_album_appeared_on = album_appeared_on

async def spotify_webhook():
  global latest_album, latest_single, latest_album_appeared_on
  latest_album = None
  latest_single = None
  latest_album_appeared_on = None
  while True:
    try:
      await album_spotify()

      await single_spotify()
      
      await album_appeared_on_spotify()
    
    except Exception as f:
      print(f"An error occurred in Spotify webhook: {f}")
      await asyncio.sleep(400)

    await asyncio.sleep(0)

async def youtube_webhook():
  latest_video_url = None
  latest_stream_url = None
  while True:
    try:
      video_url = await youtube.get_latest_video()
      if video_url and video_url != latest_video_url:
        video_thumbnail = await youtube.get_video_thumbnail()
        video_title = await youtube.get_video_title()
        embed = DiscordEmbed(
        description=f"ななひら uploaded a video on Youtube\n\n**{video_title}**"
        )
        embed.set_author(name="ななひら - Youtube", url=video_url)
        embed.set_image(url=video_thumbnail)
        embedhook = DiscordWebhook(url=webhook_url)
        embedhook.add_embed(embed)
        embedhook.execute()
        latest_video_url = video_url
      
      stream_url = await youtube.get_latest_stream()
      if stream_url and stream_url != latest_stream_url:
        stream_thumbnail = await youtube.get_stream_thumbnail()
        stream_title = await youtube.get_stream_title()
        embed = DiscordEmbed(
        description=f"ななひら is/was live on Youtube\n\n**{stream_title}**"
        )
        embed.set_author(name="ななひら - Youtube", url=stream_url)
        embed.set_image(url=stream_thumbnail)
        embedhook = DiscordWebhook(url=webhook_url)
        embedhook.add_embed(embed)
        embedhook.execute()
        latest_stream_url = stream_url
    
    except Exception as g:
      print(f"An error occurred in Youtube webhook: {g}")
      await asyncio.sleep(400)
    
    await asyncio.sleep(0)
      

async def main():
    create_ids_db()

    await asyncio.gather(xtwitter.main(), xtwitter_webhook(), spotify.main(), spotify_webhook(), youtube.main(), youtube_webhook())

if __name__ == "__main__":
   asyncio.run(main())
