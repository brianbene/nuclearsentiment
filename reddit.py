import praw
import time

# Initialize Reddit API with your credentials
reddit = praw.Reddit(
    client_id="SIMj3s0TiIsz5DzRclXLWg",
    client_secret="7pes8yoDZBhWqQYF5wKkXbmVlDlrjA",
    user_agent="Nuclear Sentiment Script by Alert_Celebration_35"
)

# Function to fetch posts from Reddit
def fetch_reddit_posts():
    subreddit = reddit.subreddit("all")  # Searching across all subreddits
    posts = []

    try:
        # Search for posts about nuclear power
        for post in subreddit.search("nuclear power", time_filter="year", limit=5):  # Adjust limit as needed
            posts.append({
                "title": post.title,
                "score": post.score,
                "created": post.created_utc,
                "selftext": post.selftext,
                "subreddit": post.subreddit.display_name
            })
            print(f"Title: {post.title}")
            time.sleep(2)  # Add delay to avoid rate-limiting

        print(f"Successfully fetched {len(posts)} posts.")
        return posts
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

# Fetch and print Reddit posts
reddit_posts = fetch_reddit_posts()

# Optional: Save posts to a CSV for further analysis
import pandas as pd
if reddit_posts:
    df = pd.DataFrame(reddit_posts)
    df.to_csv("reddit_nuclear_power_posts.csv", index=False)
    print("Posts saved to 'reddit_nuclear_power_posts.csv'.")
else:
    print("No posts to save.")
