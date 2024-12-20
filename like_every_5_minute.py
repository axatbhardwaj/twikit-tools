import twikit
import json
import asyncio
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
SAVED_COOKIES_PATH = SCRIPT_DIR / "twikit_cookies.json"

def load_cookies() -> dict:
    """Load cookies from the saved cookies file"""
    with open(SAVED_COOKIES_PATH, "r", encoding="utf-8") as cookies_file:
        cookies = json.load(cookies_file)
    return cookies

async def like_tweets():
    """Fetch latest tweets and like the top 10 tweets with a 5-minute interval"""
    cookies = load_cookies()
    client = twikit.Client(cookies=cookies, language="en-US")

    # Fetch latest tweets from the feed
    tweets = await client.get_latest_timeline(count=10)

    for tweet in tweets:
        tweet_id = tweet.id  # Access the tweet ID attribute
        await client.favorite_tweet(tweet_id)
        print(f"Liked tweet {tweet_id}")
        await asyncio.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    asyncio.run(like_tweets())