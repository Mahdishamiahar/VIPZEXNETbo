import json
from rubika import Robot

# توکن ربات خودت را اینجا وارد کن
bot = Robot("BFAAA0VAVGVWZVFZCNCQWNVENKTXBTUWFXJBYOYQFMQMIWCSIAXJBVMJSQIOHXYM")

# بارگذاری تنظیمات از فایل config.json
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

@bot.on_message
def handle_message(msg):
    user_guid = msg.get('author_guid')
    text = msg.get("text", "").strip().lower()

    if user_guid is None:
        return  # اگر شناسه کاربر نبود کاری نکن

    if text == "/start":
        raw_buttons = config.get("buttons", [])
        buttons = [[{"text": b.get("text", ""), "link": b.get("link", "")}] for b in raw_buttons]

        bot.send_message(
            user_guid,
            config.get("welcome_message", "خوش آمدید!"),
            inline_buttons=buttons if buttons else None
        )
    else:
        bot.send_message(user_guid, config.get("unknown_command_message", "❓ لطفاً فقط دستور /start را ارسال کنید."))

bot.run()