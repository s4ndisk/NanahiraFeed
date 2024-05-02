import urllib.request
import re
import os
import json
from dotenv import load_dotenv
from datetime import datetime
import asyncio

load_dotenv()

YT_CHANNEL_AT = os.getenv('YT_CHANNEL_AT')

POLLING_INTERVAL = 60 * 5

latest_video_url = None
latest_stream_url = None

async def get_latest_video():
    global latest_video_url
    return latest_video_url

async def get_latest_stream():
    global latest_stream_url
    return latest_stream_url

def search_youtube_data(url):
    with open('ids.json', 'r') as file:
        data = json.load(file)
    
    for youtube_data in data['youtube']:
        youtube_url = youtube_data['youtube_url']
        if youtube_url in url:
            return True
    return False

def append_youtube_data(url):
    new_data = {"youtube_url": url}
    with open('ids.json', 'r+') as file:
        data = json.load(file)
        data["youtube"].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)

async def latest_stream():
    global latest_stream_url
    while True:
        streams = f"https://www.youtube.com/{YT_CHANNEL_AT}/live"
        html = urllib.request.urlopen(f"{streams}")
        stream_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        stream_url = "https://www.youtube.com/watch?v=" + stream_id[1]
        if stream_url:
            for url in stream_url:
                if not search_youtube_data([stream_url]):
                    append_youtube_data(stream_url)
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New stream found: {stream_url}")
                    latest_stream_url = stream_url
        if latest_stream_url == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No new streams found")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
        await asyncio.sleep(POLLING_INTERVAL)

async def latest_video():
    global latest_video_url
    videos = f"https://www.youtube.com/{YT_CHANNEL_AT}/videos"
    html = urllib.request.urlopen(f"{videos}")
    video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video_url = "https://www.youtube.com/watch?v=" + video_id[0]
    if video_url:
        for url in video_url:
            if not search_youtube_data([video_url]):
                append_youtube_data(video_url)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New video found: {video_url}")
                latest_video_url = video_url
    if latest_video_url == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No new videos found")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
    await asyncio.sleep(POLLING_INTERVAL)


async def main():
    while True:
        await asyncio.gather(latest_stream(), latest_video())

if __name__ == "__main__":
    asyncio.run(main())