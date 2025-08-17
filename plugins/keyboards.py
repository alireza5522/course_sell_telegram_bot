from pyrogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton

def createkeyboard(keyboard):
    keyboard = keyboard.split("\n")

    row = []
    
    for key in keyboard:
        buttons = key.split('/')
        row.append([InlineKeyboardButton(buttons[0], callback_data=f'cousrse:{buttons[1]}')])

    row.append([InlineKeyboardButton("پشتیبانی", url="https://t.me/MrManager_01"), InlineKeyboardButton("به اشتراک گذاری شماره", 'requestnumber')])
    
    return InlineKeyboardMarkup(row)

def coursekeyboard(info):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("مشاهده سرفصل ها", callback_data=f'topics:{info[1]}:{info[2]}:{info[3]}')],
        [InlineKeyboardButton("مشاهده ویدیو معرفی", callback_data=f'video:{info[1]}:{info[2]}:{info[3]}')],
        [InlineKeyboardButton("برگشت", callback_data=f'home'),InlineKeyboardButton("راهنمای خرید", callback_data=f'buy:{info[1]}:{info[2]}:{info[3]}')],
    ])

def pagekeyboard(info):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("برگشت", callback_data=f'back:{info[1]}:{info[2]}:{info[3]}'),InlineKeyboardButton("راهنمای خرید", callback_data=f'buy:{info[1]}:{info[2]}:{info[3]}')],
    ])

def backkeyboard(info):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("برگشت", callback_data=f'back:{info[1]}:{info[2]}:{info[3]}')],
    ])

def requestphone():
    return ReplyKeyboardMarkup(
        [[KeyboardButton("اشتراک گذاری شماره",request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
