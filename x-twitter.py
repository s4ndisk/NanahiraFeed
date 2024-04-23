# imports
from dotenv import load_dotenv
import os
import time
from typing import NoReturn
from twikit import Client, Tweet

load_dotenv()

USERNAME = os.getenv('X-TWITTER_USERNAME')
EMAIL = os.getenv('X-TWITTER_EMAIL')
PASSWORD = os.getenv('X-TWITTER_PASSWORD')

# Initialize client
client = Client('en-us')

# Login to X(Formally Twitter) with provided user credentials
# client.login(
#     auth_info_1=USERNAME ,
#     auth_info_2=EMAIL,
#     password=PASSWORD
# )

# Saving X(Formally Twitter) cookies to login with
# client.save_cookies('cookies.json')

# Use previously saved cookies to login with
client.load_cookies('cookies.json')

# Nanahira's Twitter ID 
# USER_ID = '231926590'

# Nanafeed's Twitter ID
USER_ID = '1782558668472324096'

CHECK_INTERVAL = 60 * 5


def callback(tweet: Tweet) -> None:
    print(f'New tweet posted : {tweet.text}')


def get_latest_tweet() -> Tweet:
    return client.get_user_tweets(USER_ID, 'Tweets')[0]


def main() -> NoReturn:
    before_tweet = get_latest_tweet()

    while True:
        time.sleep(CHECK_INTERVAL)
        latest_tweet = get_latest_tweet()
        if (
            before_tweet != latest_tweet and
            before_tweet.created_at_datetime < latest_tweet.created_at_datetime
        ):
            callable(latest_tweet)
        before_tweet = latest_tweet

main()