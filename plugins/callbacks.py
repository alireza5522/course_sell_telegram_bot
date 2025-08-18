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
            await send_massage(c,message,int(info[1]),coursekeyboard(info),True)

        elif data.startswith("topics"):
            info = data.split(":")
            await send_massage(c,message,int(info[2]),pagekeyboard(info),True)

        elif data.startswith("video"):
            info = data.split(":")
            await send_massage(c,message,int(info[3]),pagekeyboard(info),True)

        elif data.startswith("home"):
            info = await user_data.get_key("core")
            await send_massage(c,message,WELCOME,createkeyboard(info),True)

        elif data.startswith("buy"):
            info = data.split(":")
            await send_massage(c,message,BUY,backkeyboard(info),True)

        elif data.startswith("requestnumber"):
            await send_massage(c,message,NUMBER,requestphone(),True)

    except Exception as e:
        logger.error(
            f"❌ Error in callback | UserID={user.id} | Data={data} | Error={str(e)}",
            exc_info=True
        )
        raise e
