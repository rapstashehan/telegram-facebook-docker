from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("Enter your Telegram API ID: "))
api_hash = input("Enter your Telegram API Hash: ")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Login using your Telegram code and 2FA if enabled")
    print("Your NEW TG_SESSION string:")
    print(client.session.save())