import tweepy
import pandas as pd
import json
import datetime as datetime
import boto3

# Load API keys and tokens from configuration file
with open('config.json') as config_file:
    config = json.load(config_file)

access_token = config["access_key"]
access_token_secret = config["access_secret"]
consumer_key = config["consumer_key"]
consumer_secret = config["consumer_secret"]
bearer_token = config["bearer_token"]  # Add bearer token for v2

# Authenticate Twitter requests using OAuth2 Bearer Token
client = tweepy.Client(bearer_token=bearer_token)

# Fetch tweets using API v2
try:
    user_id = client.get_user(username='JoanWanjiruN').data.id
    tweets = client.get_users_tweets(id=user_id, max_results=100, tweet_fields=['created_at', 'text', 'author_id'])

    if tweets.data:
        tweet_list = [tweet.data for tweet in tweets.data]
        df = pd.json_normalize(tweet_list)
        print(df)
    else:
        print("No tweets found for the user.")
except tweepy.TweepyException as e:
    print(f'Error: {e}')
except Exception as e:
    print(f"An unexpected error occurred: {e}")
