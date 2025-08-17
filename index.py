from keys.keys import API_ID,API_HASH,BOT_TOKEN
from pyrogram import Client
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

os.chdir(application_path)

plugin = dict(root="plugins")

app = Client(name="course",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             plugins=plugin)

app.run()