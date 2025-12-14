from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 29559533
api_hash = f637a155977d9962c366b21a0edf022b
client = TelegramClient(StringSession(), api_id, api_hash)
client.start()
print("Session string:", client.session.save())
