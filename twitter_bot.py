import tweepy
import os
from dotenv import load_dotenv

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

# Verify credentials
try:
    response = client.get_me()
    if response.data:
        print("Authentication OK")
    else:
        print("Error during authentication")
except tweepy.TweepError as e:
    print(f"Error during authentication: {e}")

# Post a tweet
try:
    client.create_tweet(text="dom")
    client.create_tweet(text="is")
    client.create_tweet(text="cool")
    print("Tweet sent successfully")
except tweepy.TweepError as e:
    print(f"Error during tweet: {e}")
