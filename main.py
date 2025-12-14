import os
import asyncio
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Telegram config
api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
session_str = os.getenv("TG_SESSION")
target_group = os.getenv("TG_GROUP")

# Facebook config
fb_page_access_token = os.getenv("FB_ACCESS_TOKEN")
fb_page_id = os.getenv("FB_PAGE_ID")

# Telegram client
client = TelegramClient(StringSession(session_str), api_id, api_hash)

async def main():
    await client.start()
    print("Telegram client started...")
    print("Monitoring Telegram group...")

    @client.on(events.NewMessage(chats=target_group))
    async def handler(event):
        # Detect photos + image documents
        if event.photo or (event.file and event.file.mime_type and event.file.mime_type.startswith("image/")):
            print("New photo detected!")

            file_path = await event.download_media()
            print(f"Photo downloaded to {file_path}")

            # Upload to Facebook WITHOUT caption
            with open(file_path, "rb") as image:
                response = requests.post(
                    f"https://graph.facebook.com/{fb_page_id}/photos",
                    files={"source": image},
                    data={"access_token": fb_page_access_token}
                )

            if response.ok:
                print("Photo uploaded to Facebook successfully")
            else:
                print("Facebook upload failed:", response.text)

            os.remove(file_path)

    await client.run_until_disconnected()

asyncio.run(main())
