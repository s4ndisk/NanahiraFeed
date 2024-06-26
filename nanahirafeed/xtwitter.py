import os
import asyncio
import time
import json
import requests
from dotenv import load_dotenv
from datetime import datetime
from twikit import Client, Tweet

load_dotenv()

USERNAME = os.getenv('XTWITTER_USERNAME')
EMAIL = os.getenv('XTWITTER_EMAIL')
PASSWORD = os.getenv('XTWITTER_PASSWORD')
USER_ID = os.getenv('USER_ID')
USER_ID1 = os.getenv('USER_ID1')

# Initialize client
client = Client()

def X_Formally_Twitter_Login():

    file_path = "cookies.json"

    if not os.path.exists(file_path):
         # Login to X (Formally Twitter) with provided user credentials
        client.login(
            auth_info_1=USERNAME,
            auth_info_2=EMAIL,
            password=PASSWORD
        )
         # Saving X (Formally Twitter) cookies to login with in the future 
        client.save_cookies(file_path)
        client.load_cookies(file_path)
            
    else:
         # Use previously saved cookies to login with
         client.load_cookies(file_path)


X_Formally_Twitter_Login()

# Time to poll X (Formally Twitter) for new tweets 
## Make this RNG so I dont get banned for botting by X (Formally Twitter)
POLLING_INTERVAL = 60 * 5

# Define user_tweet var
user_tweets = client.get_user_tweets(USER_ID, 'Tweets')

# Set var to None by default
latest_tweet_id = None

# Define latest tweet var as global and return its value
async def get_latest_tweet_id():
    global latest_tweet_id
    return latest_tweet_id

async def get_profile_picture():
    user = client.get_user_by_id(USER_ID)
    if user:
        return user.profile_image_url

async def get_tweet_text():
    tweet = client.get_tweet_by_id(latest_tweet_id)
    if tweet:
        return tweet.text

async def get_tweet_media_url(tweet_id):
    tweet = client.get_tweet_by_id(tweet_id)
    if tweet.media:
        for i, media in enumerate(tweet.media):
            media_url = media.get('media_url_https')
            if media_url:
                return media_url

# Format the polled data to be just the id and the datetime for the JSON database
def extract_tweet_ids_and_datetimes(user_tweets):
    tweet_ids = [tweet.id for tweet in user_tweets]
    tweet_datetimes = [tweet.created_at_datetime for tweet in user_tweets]
    return tweet_ids, tweet_datetimes

# Search JSON database for tweet id to determine if polled tweet is new or not
def search_tweet_data(tweet_ids_to_search):
    with open('ids.json', 'r') as file:
        data = json.load(file)
    
    for tweet_data in data['xtwitter']:
        tweet_id = tweet_data['tweet_id']
        if tweet_id in tweet_ids_to_search:
            return True
    return False

# Append polled tweet data to the JSON database 
def append_tweet_data(tweet_id, tweet_datetime):
    tweet_datetime_str = tweet_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    new_data = {"tweet_id": tweet_id, "tweet_date_time": tweet_datetime_str}
    with open('ids.json', 'r+') as file:
        data = json.load(file)
        data["xtwitter"].append(new_data)
        file.seek(0)
        json.dump(data, file, indent=4)

async def main():
    global latest_tweet_id
    while True:
        user_tweets = client.get_user_tweets(USER_ID, 'Tweets')
        if user_tweets:
            count = 5 # set initial value of count var to 5
            for tweet in user_tweets: # for loop for checking tweets
                first_tweet = user_tweets[count]  # get the tweet in order of count var
                tweet_id = first_tweet.id
                tweet_datetime = first_tweet.created_at_datetime
                if not search_tweet_data([tweet_id]): # search if tweet id is in the json database, if not add it to the database and set it equal to latest_tweet_id var
                    append_tweet_data(tweet_id, tweet_datetime)
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New tweet found: {tweet_id}")
                    latest_tweet_id = tweet_id
                    count -= 1 # decreas the value of count var on each loop
                    await asyncio.sleep(2)
                if count < 0: # break the loop once the count var goes less than 0
                    break
        if latest_tweet_id == None:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} No new tweets found")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
        await asyncio.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())


    