from datetime import datetime
import tweepy
import os
import time
import tweepy.errors
from dotenv import load_dotenv
from requests_scraper import req_scrape, upload_to_google_sheets

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
bearer_token = os.getenv("BEARER_TOKEN")
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Create a client object
client = tweepy.Client(bearer_token=bearer_token,
                       consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# run two other functions
req_scrape()
upload_to_google_sheets()
time.sleep(5)
# Verify credentials
try:
    response = client.get_me()
    if response.data:
        print("Authentication OK")
    else:
        print("Error during authentication")
except tweepy.errors.TweepyException as e:
    print(f"Error during authentication: {e}")

time.sleep(5)


def create_unique_tweet(base_text, url):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{base_text} (Updated: {timestamp}) {url}"


# When tweeting:
base_tweet = "Check out the latest top airing anime!"
sheets_url = "https://docs.google.com/spreadsheets/d/1TBpLTpAsucY_aYz5qF4DN6bI90DQQ64v3AUzPA6zqeI/edit?gid=0#gid=0"
unique_tweet = create_unique_tweet(base_tweet, sheets_url)

# Post a tweet
try:
    client.create_tweet(text=unique_tweet)
    print("Tweet sent successfully")
except tweepy.errors.TweepyException as e:
    print(f"Error during tweet: {e}")
