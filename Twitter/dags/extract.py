import tweepy
import pandas as pd
import time
from Twitter.config.config import access_token, access_token_secret, consumer_key, consumer_secret, bearer_token

# Authenticate Twitter requests using OAuth2 Bearer Token
client = tweepy.Client(bearer_token=bearer_token)

# Fetch all tweets using API v2 with rate limit handling
def fetch_all_tweets(username):
    try:
        user_id = client.get_user(username=username).data.id
        all_tweets = []
        pagination_token = None

        while True:
            try:
                tweets = client.get_users_tweets(
                    id=user_id, 
                    max_results=100, 
                    tweet_fields=['created_at', 'text'], 
                    expansions=['attachments.media_keys'], 
                    media_fields=['url'],
                    pagination_token=pagination_token
                )

                media_dict = {media.media_key: media.url for media in tweets.includes.get('media', [])}

                if tweets.data:
                    for tweet in tweets.data:
                        tweet_data = tweet.data
                        # Remove unwanted fields
                        tweet_data.pop('edit_history_tweet_ids', None)
                        tweet_data.pop('author_id', None)
                        media_keys = tweet_data.get('attachments', {}).get('media_keys', [])
                        tweet_data['image_urls'] = [media_dict[key] for key in media_keys if key in media_dict]
                        all_tweets.append(tweet_data)

                    # Update pagination token
                    pagination_token = tweets.meta.get('next_token', None)
                    if not pagination_token:
                        break
                else:
                    break
            
            except tweepy.TooManyRequests:
                print("Rate limit reached. Waiting for 15 minutes.")
                time.sleep(15 * 60)  # Wait for 15 minutes
                continue  # Retry the same request

        # Save all tweets to a single CSV file
        if all_tweets:
            df = pd.json_normalize(all_tweets)
            df.to_csv(f'{username}_tweets.csv', index=False)
            print(f'Successfully saved all tweets to {username}_tweets.csv')
        else:
            print("No tweets found for the user.")
    except tweepy.TweepyException as e:
        print(f'Error: {e}')
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Replace 'kabetes' with the desired username
fetch_all_tweets('kabetes')
