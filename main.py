import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import requests
from dotenv import load_dotenv
import os

load_dotenv()
# ----- Telegram API Info -----
api_id = int(os.getenv("TG_API_ID"))        # Your Telegram API ID
api_hash = os.getenv("TG_API_HASH")         # Your Telegram API Hash
session_str = os.getenv("TG_SESSION")       # Optional: Your saved session string

# ----- Facebook Info -----
fb_page_access_token = os.getenv("FB_ACCESS_TOKEN")  # Your page access token
fb_page_id = os.getenv("FB_PAGE_ID")                # Your page ID

# ----- Telegram Group -----
target_group = os.getenv("TG_GROUP")  # Group username or ID

# Initialize Telegram client
if session_str:
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
else:
    client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start()
    print("Telegram client started...")

    @client.on(events.NewMessage(chats=target_group))
    async def handler(event):
        if event.photo:
            print("New photo detected!")
            file_path = await event.download_media()
            print(f"Photo downloaded to {file_path}")
            
            # Post to Facebook
            with open(file_path, "rb") as f:
                response = requests.post(
                    f"https://graph.facebook.com/{fb_page_id}/photos",
                    files={"source": f},
                    data={"access_token": fb_page_access_token, "caption": event.message.message or ""}
                )
            if response.ok:
                print("Photo posted to Facebook successfully!")
            else:
                print("Failed to post to Facebook:", response.text)
            os.remove(file_path)

    print("Monitoring Telegram group...")
    await client.run_until_disconnected()

asyncio.run(main())
