import twikit
from typing import Optional
import json
import asyncio
from pathlib import Path
import time

SCRIPT_DIR = Path(__file__).parent
COOKIES_DIR = SCRIPT_DIR / "cookies"
EXTRACTED_COOKIES_PATH = SCRIPT_DIR / "x.com.cookies.json"

# Create cookies directory if it doesn't exist
COOKIES_DIR.mkdir(exist_ok=True)

def get_cookie_path(username: str) -> Path:
    """Get the cookie file path for a specific username"""
    return COOKIES_DIR / f"{username}_cookies.json"

def await_for_cookies() -> dict:
    """Awaits for the cookies file"""

    print(f"Please copy the '{EXTRACTED_COOKIES_PATH}' file into this repo...")

    while not EXTRACTED_COOKIES_PATH.exists():
        time.sleep(5)

    print("Cookie file detected")

    with open(EXTRACTED_COOKIES_PATH, "r", encoding="utf-8") as cookies_file:
        cookies = json.load(cookies_file)

    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies}
    return cookies_dict


async def async_get_twitter_cookies(username, email, password) -> Optional[str]:
    """Verifies that the Twitter credentials are correct and get the cookies"""

    client = twikit.Client(
        language="en-US"
    )

    try:
        valid_cookies = False

        # If cookies exist, try with those and validate
        cookie_path = get_cookie_path(username)
        if cookie_path.exists():
            with open(cookie_path, "r", encoding="utf-8") as cookies_file:
                cookies = json.load(cookies_file)
                client.set_cookies(cookies)

            user = await client.user()
            valid_cookies = user.screen_name == username

        if not valid_cookies:
            print("Logging in with password")
            await client.login(
                auth_info_1=username,
                auth_info_2=email,
                password=password,
            )
            client.save_cookies(cookie_path)

    except twikit.errors.BadRequest:
        print("Twitter login failed due to a known issue with the login flow.\nPlease check the known issues section in the README to find the solution. You will need to provide us with a cookies file.")
        cookies = await_for_cookies()
        client.set_cookies(cookies)
        client.save_cookies(cookie_path)  # Save cookies to the specified path

    return json.dumps(client.get_cookies()).replace(" ", "")


def get_twitter_cookies(username, email, password) -> Optional[str]:
    """get_twitter_cookies"""
    return asyncio.run(async_get_twitter_cookies(username, email, password))


async def verify_and_save_cookies(username: str, email: str, password: str) -> bool:
    client = twikit.Client(language="en-US")
    
    try:
        await client.login(
            auth_info_1=username,
            auth_info_2=email,
            password=password,
        )
        
        user = await client.user()
        if user.screen_name == username:
            cookies = client.get_cookies()
            cookie_path = get_cookie_path(username)
            with open(cookie_path, "w", encoding="utf-8") as f:
                json.dump(cookies, f, indent=4)
            print(f"Cookies successfully saved to {cookie_path}")
            return True
    except Exception as e:
        print(f"Login failed: {e}")
        return False

def main():
    username = input("Enter your Twitter username: ")
    email = input("Enter your Twitter email: ")
    password = input("Enter your Twitter password: ")
    
    success = asyncio.run(verify_and_save_cookies(username, email, password))
    if not success:
        print("Failed to verify and save cookies")

if __name__ == "__main__":
    main()


async def async_validate_twitter_credentials(username: str, email: str, password: str):
    """Test twitter credential validity"""
    cookie_path = get_cookie_path(username)

    # Load cookies if they exist
    cookies = None
    if cookie_path.exists():
        with open(cookie_path, "r", encoding="utf-8") as cookie_file:
            cookies = json.load(cookie_file)

    # Instantiate the client
    client = twikit.Client(language="en-US")

    if cookies:
        client.set_cookies(cookies)

    # Try to read using cookies
    try:
        tweet = await client.get_tweet_by_id("1741522811116753092")
        is_valid_cookies = tweet.user.id == "1450081635559428107"
        return is_valid_cookies, None
    except twikit.errors.Forbidden:
        is_valid_cookies = False
        cookies = await async_get_twitter_cookies(username, email, password)
        
        # Save new cookies to username-specific path
        with open(cookie_path, "w", encoding="utf-8") as cookie_file:
            json.dump(cookies, cookie_file, indent=4)
        return is_valid_cookies, cookies


def validate_twitter_credentials(username: str, email: str, password: str) -> Optional[str]:
    """Validate twitter credentials"""
    return asyncio.run(async_validate_twitter_credentials(username, email, password))
