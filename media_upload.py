import asyncio
import os
from twikit import Client
from dotenv import load_dotenv

async def upload_image(client, image_path, status):
    """
    Uploads an image to Twitter with a status message.
    
    :param client: The Twikit Client object.
    :param image_path: The file path to the image to upload.
    :param status: The status message to accompany the image.
    """
    media_id = await client.upload_media(image_path)
    await client.create_tweet(text=status, media_ids=[media_id])

async def main():
    # Load environment variables from .env file
    load_dotenv()

    auth_info_1 = input("Enter your username: ")
    auth_info_2 = input("Enter your email: ")
    password = input("Enter your password: ")
    cookies_file = input("Enter the path to your cookies file: ")

    # Initialize client
    client = Client(language='en-US')

    # Authenticate to Twitter using the provided cookie
    await client.login(
        auth_info_1=auth_info_1,
        auth_info_2=auth_info_2,
        password=password,
        cookies_file=cookies_file,
    )

    # Define the image path and status message
    image_path = "image/Gemini_Generated_Image_nlhl6ynlhl6ynlhl.jpeg"
    status = 'Here is my new avatar!'

    # Upload the image with the status message
    await upload_image(client, image_path, status)

asyncio.run(main())
