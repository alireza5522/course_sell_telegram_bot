from datetime import *
from plugins.functions import *
from pyrogram import Client,filters
from pyrogram.types import Message
from plugins.keyboards import *
from plugins.redismanager import user_data
from keys.keys import *
from plugins.log import logger
from .log_analizer import analyze_logs

@Client.on_message(filters.command('adminstart') & filters.private) 
async def adminstart_handel(c:Client,m:Message):

     user = m.from_user
     logger.info(f"📌 /adminstart | UserID={user.id} | Username=@{user.username} | Name={user.first_name}")

     if m.from_user.id != ADMIN:
          logger.warning(f"Unauthorized attempt to use /adminstart by UserID={user.id}")
          return
     
     if user_data.isconnected == False:
          await user_data.connect()
          await user_data.select_db(0)
          logger.info("Connected to Redis (DB=0)")

     try:
          text = await c.get_messages(chat_id=CHANNEL,message_ids=MESSAGGE)
          await user_data.set_key("core",text.text,None)
          await m.reply_text(text='Done')
          logger.info("✅ Admin core data updated successfully")
     except Exception as e:
          logger.error("❌ Error in adminstart_handel", exc_info=True)
          raise e


@Client.on_message(filters.command("start") & filters.private & ban_check())
async def start_handel(c:Client,m:Message):
     user = m.from_user
     logger.info(f"📌 /start | UserID={user.id} | Username=@{user.username} | Name={user.first_name}")
     try:
          info = await user_data.get_key("core")
          await c.copy_message(chat_id=user.id,from_chat_id=CHANNEL,message_id=WELCOME,reply_markup=createkeyboard(info))

     except Exception as e:
          logger.error(f"❌ Error in start_handel | UserID={user.id}", exc_info=True)
          raise e


@Client.on_message(filters.private & filters.contact & ban_check())
async def handle_contact(c:Client, m: Message):
     user = m.from_user
     phone = m.contact.phone_number if m.contact else None
     logger.info(f"📌 Contact shared | UserID={user.id} | Username=@{user.username} | Name={user.first_name}")

     try:
          # ارسال شماره برای ادمین جهت تایید
          if not str(phone).startswith("+98"):
               await m.reply_text(text='شماره مورد نظر باید شماره ایران باشد\nلطفا با شماره اکانتی که شماره ایران دارد افدام به خرید کنید')
          else:
               await m.reply_text(text='شماره شما به اشتراک گذاشته شد')

          text = f"contanct: {phone}\nchat_id: {user.id}\nusernmae: {user.username}\nname: {user.first_name}"
          await c.send_message(chat_id=ADMIN,text=text)

          info = await user_data.get_key("core")
          await c.copy_message(chat_id=user.id,from_chat_id=CHANNEL,message_id=WELCOME,reply_markup=createkeyboard(info))

     except Exception as e:
          logger.error(f"❌ Error in handle_contact | UserID={user.id}", exc_info=True)
          raise e


@Client.on_message(filters.text & filters.private)
async def text_handle(c:Client,m:Message):

     if m.from_user.id != ADMIN:
          return
     
     if m.text.startswith('ban'):
          
          if len(m.text.split(' ')) < 2:
               await m.reply_text(text='ban chat_id')
               return

          target_user = m.text.split(' ')[1]

          try:
               await user_data.set_key(str(target_user),'ban',3600*24)
               await m.reply_text(text=f'banshod {target_user}')
               logger.info(f"✅ UserID={target_user} banned by {m.from_user}")
          except Exception as e:
               logger.error(f"❌ Error banning UserID={target_user}", exc_info=True)
               raise e

     elif m.text.startswith('status'):
          report = analyze_logs(LOG_FILE)
          await m.reply_text(report)

     elif m.text.startswith('help'):
          await m.reply_text(text=f'ban chat_id\nstatus')