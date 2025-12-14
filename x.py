from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# Replace with your Telegram API info
api_id = int(input("Enter your Telegram API ID: "))
api_hash = input("Enter your Telegram API Hash: ")

# Start a client with a temporary session
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Please login with your Telegram account...")
    # The client will ask for phone number and 2FA password if enabled
    print("Your session string is:")
    print(client.session.save())
