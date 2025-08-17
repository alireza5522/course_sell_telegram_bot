from datetime import *
from plugins.functions import *
from pyrogram.types import CallbackQuery
from plugins.keyboards import *
from plugins.redismanager import user_data
from keys.keys import *
from plugins.log import logger

@Client.on_callback_query(ban_check())
async def callback_query(c:Client, callback_query: CallbackQuery):

    message = callback_query.message
    data = callback_query.data
    user = callback_query.from_user

    # لاگ کاربر و دیتای کلیک‌شده
    logger.info(
        f"📌 Callback | UserID={user.id} | Username=@{user.username} | Name={user.first_name} | Data={data}"
    )

    try:
        if data.startswith("cousrse") or data.startswith("back"):
            info = data.split(":")
            await c.delete_messages(chat_id=message.chat.id,message_ids=message.id)
            await c.copy_message(chat_id=message.chat.id,from_chat_id=CHANNEL,message_id=int(info[1]),reply_markup=coursekeyboard(info))
        
        elif data.startswith("topics"):
            info = data.split(":")
            await c.delete_messages(chat_id=message.chat.id,message_ids=message.id)
            await c.copy_message(chat_id=message.chat.id,from_chat_id=CHANNEL,message_id=int(info[2]),reply_markup=pagekeyboard(info))
        
        elif data.startswith("video"):
            info = data.split(":")
            await c.delete_messages(chat_id=message.chat.id,message_ids=message.id)
            await c.copy_message(chat_id=message.chat.id,from_chat_id=CHANNEL,message_id=int(info[3]),reply_markup=pagekeyboard(info))
        
        elif data.startswith("home"):
            info = await user_data.get_key("core")
            await c.delete_messages(chat_id=message.chat.id,message_ids=message.id)
            await c.copy_message(chat_id=message.chat.id,from_chat_id=CHANNEL,message_id=WELCOME,reply_markup=createkeyboard(info))

        elif data.startswith("buy"):
            info = data.split(":")
            await c.delete_messages(chat_id=message.chat.id,message_ids=message.id)
            await c.copy_message(chat_id=message.chat.id,from_chat_id=CHANNEL,message_id=BUY,reply_markup=backkeyboard(info))
        
        elif data.startswith("requestnumber"):
            await c.delete_messages(chat_id=message.chat.id,message_ids=message.id)
            await c.copy_message(chat_id=message.chat.id,from_chat_id=CHANNEL,message_id=NUMBER,reply_markup=requestphone())

    except Exception as e:
        logger.error(
            f"❌ Error in callback | UserID={user.id} | Data={data} | Error={str(e)}",
            exc_info=True
        )
        raise e
