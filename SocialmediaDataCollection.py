import praw
import tweepy
import pandas as pd
import time
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import boto3

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Function to clean text
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    return text.lower().strip()

# 1. Reddit Data Collection
def fetch_reddit_posts():
    reddit = praw.Reddit(
        client_id="SIMj3s0TiIsz5DzRclXLWg",
        client_secret="7pes8yoDZBhWqQYF5wKkXbmVlDlrjA",
        user_agent="Nuclear Sentiment Script by Alert_Celebration_35"
    )

    subreddit = reddit.subreddit("all")
    posts = []

    try:
        for post in subreddit.search("nuclear power", time_filter="year", limit=500):
            sentiment = sia.polarity_scores(clean_text(post.title))['compound']
            posts.append({
                "platform": "Reddit",
                "text": post.title,
                "sentiment": sentiment,
                "location": None,  # Reddit doesn't provide location data
                "score": post.score,
                "created": post.created_utc
            })
            time.sleep(2)  # Add delay to avoid rate-limiting

        print(f"Successfully fetched {len(posts)} posts from Reddit.")
        return posts
    except Exception as e:
        print(f"Error fetching Reddit posts: {e}")
        return []

# 2. Twitter (X) Data Collection
def fetch_twitter_data():
    client = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAIWgxAEAAAAAzrIf9z7iFPlpCyNU%2BqzOoeIZM1w%3DLkUgiwxnjgO2mm2peYmfrHr7ke0Lv5ML5JTW21AjrXXGZtB6MW")
    query = "nuclear power -is:retweet"
    tweets = []

    try:
        response = client.search_recent_tweets(
            query=query,
            tweet_fields=["created_at", "geo", "public_metrics"],
            max_results=100
        )

        for tweet in response.data:
            sentiment = sia.polarity_scores(clean_text(tweet.text))['compound']
            tweets.append({
                "platform": "X",
                "text": tweet.text,
                "sentiment": sentiment,
                "location": tweet.geo if tweet.geo else None,
                "likes": tweet.public_metrics["like_count"],
                "retweets": tweet.public_metrics["retweet_count"],
                "created": tweet.created_at
            })

        print(f"Successfully fetched {len(tweets)} tweets from Twitter.")
        return tweets
    except Exception as e:
        print(f"Error fetching Twitter posts: {e}")
        return []

# Function to upload a file to S3
def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client(
        's3',
        aws_access_key_id="AKIAXBZV5TNYBPO5ESPJ",
        aws_secret_access_key="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"
    )

    try:
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"File '{file_name}' uploaded to S3 bucket '{bucket}' as '{object_name}'")
    except Exception as e:
        print(f"Error uploading file to S3: {e}")

# 3. Combine and Save Data
def collect_data():
    reddit_data = fetch_reddit_posts()
    twitter_data = fetch_twitter_data()

    # Combine all data into a single DataFrame
    all_data = reddit_data + twitter_data
    df = pd.DataFrame(all_data)

    # Save to CSV locally
    file_name = "nuclear_power_sentiment.csv"
    df.to_csv(file_name, index=False)

    # Upload to S3
    bucket_name = "nuclearsentiment"
    upload_to_s3(file_name, bucket_name, f"data/{file_name}")

# Run Data Collection
if __name__ == "__main__":
    collect_data()
