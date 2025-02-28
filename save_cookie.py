import twikit
from typing import Optional
import json
import asyncio
from pathlib import Path
import time
from stringify_json import stringify_json

SCRIPT_DIR = Path(__file__).parent
COOKIES_DIR = SCRIPT_DIR / "cookies"
EXTRACTED_COOKIES_PATH = SCRIPT_DIR / "x.com.cookies.json"

# Create cookies directory if it doesn't exist
COOKIES_DIR.mkdir(exist_ok=True)

def get_cookie_path(username: str) -> Path:
    """Get the cookie file path for a specific username"""
    return COOKIES_DIR / f"{username}_cookies.json"


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
            # Generate stringified version
            stringify_json(str(cookie_path))
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
