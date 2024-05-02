import urllib.request
import re
import asyncio

YT_CHANNEL_ID = "UN_fYA9QRK-aJnFTgvR_4zug"
YT_CHANNEL_AT = "@Nanahira_Confetto"

def search_youtube_data(url):
    with open('ids.json', 'r') as file:
        data = json.load(file)
    
    for youtube_data in data['youtube']:
        youtube_url = youtube_data['youtube_url']
        if youtube_url in url:
            return True
    return False

def append_youtube_data(url, date):
    new_data = {"youtube_url": url, "youtube_date": date}
    with open('ids.json', 'r+') as file:
        data = json.load(file)
        data["youtube"].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)

async def latest_stream():
    streams = f"https://www.youtube.com/{YT_CHANNEL_AT}/streams"
    html = urlib.request.urlopen(f"{videos}")
    stream_id = re.findall(r"watch\?v=(\S{11})", html.read().decode)
    print("https://www.youtube.com/watch?v=" + stream_id[0])


async def latest_video():
    videos = f"https://www.youtube.com/{YT_CHANNEL_AT}/videos"
    html = urllib.request.urlopen(f"{videos}")
    video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    print("https://www.youtube.com/watch?v=" + video_id[0])

async def main():
    while True:
        await asyncio.gather(latest_stream(), latest_video())

if __name__ == "__main__":
    asyncio.run(main())