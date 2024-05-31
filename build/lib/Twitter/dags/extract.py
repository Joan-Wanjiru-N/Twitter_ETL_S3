# import tweepy
# import pandas as pd
# import json
# import datetime as datetime
# import boto3
# from Twitter.config.access_tokens import access_key, access_secret, consumer_key, consumer_secret

# access_key = access_key.strip()
# access_secret = access_secret.strip()
# consumer_key = consumer_key.strip()
# consumer_secret = consumer_secret.strip()

# # Authenticate Twitter requests using OAuth Authentication and call the keys provided earlier
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_key, access_secret)

# # Setting an API object
# api = tweepy.API(auth)

# # Verify credentials to ensure authentication is successful
# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except tweepy.errors.Unauthorized as e: 
#     print(f"Error during authentication: {e}")
#     exit(1)  # Exit if authentication fails
# except Exception as e:
#     print(f"An unexpected error occurred during authentication: {e}")
#     exit(1)

# # Fetch tweets
# try:
#     tweets = api.user_timeline(screen_name='@JoanWanjiruN',
#                                count=100,
#                                include_rts=False,
#                                tweet_mode='extended')
#     for tweet in tweets:
#         print(tweet.full_text)
# except tweepy.errors.Unauthorized as e:
#     print(f'Error: {e}')
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")

# #Convert tweets to DataFrame or other formats for further processing
# df = pd.DataFrame(tweets)
# print(df)
import tweepy
import pandas as pd
import json
import datetime as datetime
import boto3

with open('config.json') as config_file:
    config = json.load(config_file)

access_key = config["access_key"]
access_secret = config["access_secret"]
consumer_key = config["consumer_key"]
consumer_secret = config["consumer_secret"]

# Authenticate Twitter requests using OAuth Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Setting an API object
api = tweepy.API(auth)

# Verify credentials to ensure authentication is successful
try:
    api.verify_credentials()
    print("Authentication OK")
except tweepy.errors.Unauthorized as e:
    print(f"Error during authentication: {e}")
    exit(1)  # Exit if authentication fails
except Exception as e:
    print(f"An unexpected error occurred during authentication: {e}")
    exit(1)

# Fetch tweets
try:
    tweets = api.user_timeline(screen_name='@JoanWanjiruN',
                               count=100,
                               include_rts=False,
                               tweet_mode='extended')
    for tweet in tweets:
        print(tweet.full_text)
except tweepy.errors.Unauthorized as e:
    print(f'Error: {e}')
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Convert tweets to DataFrame or other formats for further processing
df = pd.DataFrame([tweet._json for tweet in tweets])
print(df)
