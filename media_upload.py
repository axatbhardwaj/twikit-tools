import asyncio
import os
from twikit import Client
from dotenv import load_dotenv
import base64
from datetime import datetime


async def convet_to_image(img_data_b64):

    # convert image_data_base64 to jpg
    decoded_image_data = base64.b64decode(image_data_base64)

    # Create a unique filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    image_filename = f"image_{timestamp}.jpg"
    image_dir = "/home/xzat/personal/twikit-stress-test/image"
    image_path_output = os.path.join(image_dir, image_filename)

    # Ensure the directory exists
    os.makedirs(image_dir, exist_ok=True)

    # Decode base64 image data and save to file
    with open(image_path_output, "wb") as file:
        image_data = base64.b64decode(decoded_image_data)
        file.write(image_data)


async def upload_image(client, image_path, status):
    """
    Uploads an image to Twitter with a status message.
    
    :param client: The Twikit Client object.
    :param image_path: The file path to the image to upload.
    :param status: The status message to accompany the image.
    """

    media_id = await client.upload_media(image_path)
    await client.create_tweet(text=status, media_ids=[media_id])
    print("uploaded")

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
    image_path = "image/image_20250310104430.png"
    status = "new profile pic what do yall say ! ?"

    # Upload the image with the status message
    await upload_image(client, image_path, status)

    # await convet_to_image(image_data_base64)

asyncio.run(main())
