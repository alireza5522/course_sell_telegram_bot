from .redismanager import user_data
from keys.keys import *
from pyrogram import Client,filters
from pyrogram.types import Message,LinkPreviewOptions
import json
import pyrogram
import datetime

def ban_check():
    async def func(flt, c:Client, m:Message):
        try: return (await user_data.get_key(str(m.from_user.id))) != 'ban'
        except: return True
    return filters.create(func)

message_store = {}

def message_store_action(action, key=None, value=None):
    """
    مدیریت دیکشنری گلوبال از طریق یک تابع

    action:
        - 'set'   -> اضافه کردن/آپدیت مقدار (نیاز به key و value)
        - 'get'   -> گرفتن مقدار (نیاز به key)
        - 'delete'-> حذف یک کلید (نیاز به key)
        - 'clear' -> خالی کردن کل دیکشنری
        - 'all'   -> برگرداندن کل دیکشنری
    """
    global message_store
    
    if action == "set" and key is not None:
        message_store[key] = value
        return True
    
    elif action == "get" and key is not None:
        return message_store.get(key, None)
    
    elif action == "delete" and key is not None:
        return message_store.pop(key, None)
    
    elif action == "clear":
        message_store.clear()
        return True
    
    elif action == "all":
        return dict(message_store)
    
    else:
        raise ValueError("Action یا پارامترها اشتباه هستن.")


async def store_messages(c):
    m_WELCOME,m_MESSAGGE,m_BUY,m_NUMBER = await c.get_messages(chat_id=CHANNEL,message_ids=[WELCOME,MESSAGGE,BUY,NUMBER])

    await user_data.set_key("core",m_MESSAGGE.text,None)
    message_store_action("set",WELCOME,m_WELCOME)
    message_store_action("set",BUY,m_BUY)
    message_store_action("set",NUMBER,m_NUMBER)

async def send_massage(c,m,message_id,keyboard,delete=False):
    try:
        if delete:
            await c.delete_messages(chat_id=m.chat.id,message_ids=m.id)

        info = message_store_action('get',message_id)

        if info == None:
            temp = await c.get_messages(chat_id=CHANNEL,message_ids=message_id)
            message_store_action('set',temp.id,temp)
            info = temp
        # print(type(repr(m_WELCOME)))
        # print(eval(repr(m_WELCOME)))


        if info.text:
            await m.reply_text(text=info.text,entities=info.entities,link_preview_options=LinkPreviewOptions(is_disabled=True),reply_markup=keyboard)
        elif info.video:
            await m.reply_video(video=info.video.file_id,caption=info.caption,caption_entities=info.caption_entities,reply_markup=keyboard)
        elif info.photo:
            await m.reply_photo(photo=info.photo.file_id,caption=info.caption,caption_entities=info.caption_entities,reply_markup=keyboard)
        else:
            await c.copy_message(chat_id=m.from_user.id,from_chat_id=CHANNEL,message_id=message_id,reply_markup=keyboard)
            message_store_action('delete',info.id)

    except:
        await c.copy_message(chat_id=m.from_user.id,from_chat_id=CHANNEL,message_id=message_id,reply_markup=keyboard)
        message_store_action('clear')
