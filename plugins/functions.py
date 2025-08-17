from .redismanager import user_data
from keys.keys import *
from pyrogram import Client,filters
from pyrogram.types import Message

def ban_check():
    async def func(flt, c:Client, m:Message):
        try: return (await user_data.get_key(str(m.from_user.id))) != 'ban'
        except: return True
    return filters.create(func)