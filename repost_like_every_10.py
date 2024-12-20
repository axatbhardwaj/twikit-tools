import twikit
import json
import asyncio
import random
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
SAVED_COOKIES_PATH = SCRIPT_DIR / "twikit_cookies.json"

def load_cookies() -> dict:
    """Load cookies from the saved cookies file"""
    with open(SAVED_COOKIES_PATH, "r", encoding="utf-8") as cookies_file:
        cookies = json.load(cookies_file)
    return cookies

async def like_and_repost_tweets():
    """Fetch latest tweets every 10 minutes, randomly like and repost tweets"""
    cookies = load_cookies()
    client = twikit.Client(cookies=cookies, language="en-US")

    while True:
        # Fetch latest tweets from the feed
        tweets = await client.get_latest_timeline(count=10)

        if tweets:
            # Randomly select a tweet to like
            tweet_to_like = random.choice(tweets)
            await client.like_tweet(tweet_to_like.id)
            print(f"Liked tweet {tweet_to_like.id}")

            # Randomly select another tweet to repost
            tweet_to_repost = random.choice(tweets)
            await client.retweet(tweet_to_repost.id)
            print(f"Reposted tweet {tweet_to_repost.id}")

        # Wait for 10 minutes before fetching tweets again
        await asyncio.sleep(600)

if __name__ == "__main__":
    asyncio.run(like_and_repost_tweets())