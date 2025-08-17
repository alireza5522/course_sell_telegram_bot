import re
import pandas as pd

def analyze_logs(log_file="bot.log"):
    # الگوهای مختلف
    callback_pattern = re.compile(r"📌 Callback \| UserID=(\d+) .* \| Data=(.*)")
    ban_pattern = re.compile(r"⛔ Banned user tried access \| UserID=(\d+)")
    error_pattern = re.compile(r"❌ Error .* UserID=(\d+)")

    data = {
        "callbacks": [],
        "banned": [],
        "errors": []
    }

    # خواندن فایل لاگ
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            if "📌 Callback" in line:
                match = callback_pattern.search(line)
                if match:
                    user_id, data_clicked = match.groups()
                    data["callbacks"].append({"user": user_id, "data": data_clicked})
            
            elif "⛔ Banned" in line:
                match = ban_pattern.search(line)
                if match:
                    user_id = match.group(1)
                    data["banned"].append({"user": user_id})
            
            elif "❌ Error" in line:
                match = error_pattern.search(line)
                if match:
                    user_id = match.group(1)
                    data["errors"].append({"user": user_id})

    # ساخت DataFrame برای تحلیل
    df_callbacks = pd.DataFrame(data["callbacks"])
    df_banned = pd.DataFrame(data["banned"])
    df_errors = pd.DataFrame(data["errors"])

    # گزارش نهایی
    report = f"""
📊 گزارش نهایی

تعداد کلیک‌ها: {len(df_callbacks)}

بیشترین دکمه‌های کلیک‌ شده:
{(df_callbacks['data'].value_counts().head(5)) if not df_callbacks.empty else 'none'}

تعداد کاربران بن‌شده: {len(df_banned)}
تعداد خطاها: {len(df_errors)}
"""
    return report
