# ربات تلگرام فروش دوره‌های آموزشی

این ربات تلگرام برای فروش و مدیریت دوره‌های آموزشی طراحی شده است. کاربران می‌توانند با استفاده از ربات، دوره‌های مورد نظر خود را مشاهده و خریداری کنند.

---

## ⚙️ پیش‌نیازها

قبل از راه‌اندازی ربات، مطمئن شوید که موارد زیر را نصب کرده‌اید:

- **پایتون 3.9 یا بالاتر**
- **Redis** (برای ذخیره‌سازی داده‌ها)
- **Git** (برای کلون کردن مخزن)

---

## 📦 نصب و راه‌اندازی

### 1. نصب پایتون و ابزارهای مورد نیاز

sudo apt update
sudo apt install -y python3 python3-pip python3-venv build-essential unzip curl wget git
### 2. نصب Redis
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
### 3. کلون کردن مخزن
git clone https://github.com/alireza5522/course_sell_telegram_bot
cd course_sell_telegram_bot
### 4. ایجاد محیط مجازی و نصب وابستگی‌ها
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
### 5. پیکربندی کلیدهای API

در پوشه keys/، فایل‌های کلیدهای API خود را قرار دهید. این پوشه در .gitignore قرار دارد تا از بارگذاری در گیت جلوگیری شود.

محتوای فایل keys.py
```
API_ID = 123456          # مقدار عددی API ID خود را وارد کنید
API_HASH = "your_api_hash_here"
BOT_TOKEN = "your_bot_token_here"

# شناسه تلگرام ادمین
ADMIN = 123456789        

# متن پیام های خود را در این کانال بگذارید
CHANNEL = "@YourChannel" 

#این پیام به برای نمایش پیام خوش آمد هنگام استارت کردن ربات توسط کاربر نمایش داده میشود
WELCOME = 1

#دکمه هایی که به کاربر نمایش داده میشود هنگام استرات کاربر یا برگشت به خانه
#اسم دکمه اول/ایدی پیام این دکمه/ایدی پیام دوم/ایدی پیام سوم
#اسم دکمه دوم/ایدی پیام این دکمه/ایدی پیام دوم/ایدی پیام سوم
MESSAGGE = 2
BUY = 3                  # ID پیام خرید
NUMBER = 4               # ID پیام درخواست شماره

LOG_FILE = "bot.log"     # نام فایل لاگ
```

پیکربندی پوشه‌‌ی پروژه
```
course_sell_telegram_bot/
├── keys/                   # پوشه حاوی کلیدهای API (حساس)
├── plugins/                # پلاگین‌های ربات
├── .gitignore              # فایل‌های نادیده‌گرفته‌شده توسط گیت
├── index.py                # نقطه شروع ربات
├── requirements.txt        # وابستگی‌های پایتون
└── setup_ubuntu_server.txt # راهنمای راه‌اندازی سرور اوبونتو
```
حقوق محفوظ برای کانال تلگرام https://t.me/sefrooyekk میباشد
