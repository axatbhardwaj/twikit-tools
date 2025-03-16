import asyncio
import twikit_grok 
import os
from dotenv import load_dotenv

load_dotenv()

async def main():

    # load environment variables from .env file

    auth_info_1 = os.getenv("TWIKIT_USERNAME")
    auth_info_2 = os.getenv("TWIKIT_EMAIL")
    password = os.getenv("TWIKIT_PASSWORD")
    cookies_file = os.getenv("TWIKIT_COOKIES_PATH")

    # check if the environment variables are set if not ask the user to enter them
    if not auth_info_1 or not auth_info_2 or not password or not cookies_file:

        auth_info_1 = input("Enter your username: ")
        auth_info_2 = input("Enter your email: ")
        password = input("Enter your password: ")
        cookies_file = input("Enter the path to your cookies file: ")

    print(f"auth_info_1: {auth_info_1}")
    print(f"auth_info_2: {auth_info_2}")
    print(f"password: {password}")
    print(f"cookies_file: {cookies_file}")

    client = twikit_grok.Client(language='en-US')

    await client.login(
        auth_info_1=auth_info_1,
        auth_info_2=auth_info_2,
        password=password,
        cookies_file=cookies_file,
    )

    # create a new conversation
    conversation = await client.create_grok_conversation()
    # generate a response via image
    media = await client.upload_grok_attachment("image/image_20250310120820.png")
    print (media)
    response = await conversation.generate("Describe this image please", file_attachments=[media])

    print(response.message)

asyncio.run(main())
