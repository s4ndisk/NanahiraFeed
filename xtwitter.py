from dotenv import load_dotenv
import os
import asyncio
import time
import json
from datetime import datetime
from twikit import Client, Tweet

load_dotenv()

USERNAME = os.getenv('X-TWITTER_USERNAME')
EMAIL = os.getenv('X-TWITTER_EMAIL')
PASSWORD = os.getenv('X-TWITTER_PASSWORD')
USER_ID = os.getenv('USER_ID')
USER_ID1 = os.getenv('USER_ID1')

# Initialize client
client = Client()

def X_Formally_Twitter_Login():
    # Login to X (Formally Twitter) with provided user credentials
    client.login(
        auth_info_1=USERNAME ,
        auth_info_2=EMAIL,
        password=PASSWORD
    )
    # Saving X (Formally Twitter) cookies to login with in the future 
    client.load_cookies('cookies.json')

# To be safe, you should only need to run this function once to store cookies, then comment it out so you login with cached cookies. 
# Less likely for your account to get banned this way
## X_Formally_Twitter_Login()

# Use previously saved cookies to login with
client.load_cookies('cookies.json')

# Time to poll X (Formally Twitter) for new tweets 
## Make this RNG so I dont get banned for botting by X (Formally Twitter)
POLLING_INTERVAL = 60 * 5

# Define user_tweet var
user_tweets = client.get_user_tweets(USER_ID1, 'Tweets')

# Set var to None by default
latest_tweet_id = None

# Define latest tweet var as global and return its value
async def get_latest_tweet_id():
    global latest_tweet_id
    return latest_tweet_id

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
        user_tweets = client.get_user_tweets(USER_ID, 'Replies')
        if user_tweets:  # Check if tweets were fetched
            first_tweet = user_tweets[0]  # Get the first tweet
            tweet_id = first_tweet.id
            tweet_datetime = first_tweet.created_at_datetime
            if not search_tweet_data([tweet_id]):
                append_tweet_data(tweet_id, tweet_datetime)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} New tweet found: {tweet_id}")
                latest_tweet_id = tweet_id
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Sleeping for {POLLING_INTERVAL}s")
        await asyncio.sleep(POLLING_INTERVAL)




if __name__ == "__main__":
    asyncio.run(main())

# Implement way for script to prevent missing tweets if a tweet was made during the sleep period
# even though count is set to 5 it is polling tweets till the end, only want it to poll the top 5 before sleeping
