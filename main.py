import os
import time
from bale import Bot

bot = Bot(token=os.getenv("BOT_TOKEN"))
offset = 0

print("بات پاکت باز کن فعال شد...")

while True:
    try:
        updates = bot.get_updates(offset=offset, timeout=10)
        for update in updates:
            offset = update.update_id + 1
            message = update.message
            if not message or not message.text:
                continue

            text = message.text.lower()
            if "پاکت" not in text:
                continue
            if not message.packet:
                continue

            packet_id = message.packet.packet_id
            user = message.from_user.first_name or "ناشناس"

            try:
                result = bot.open_packet(packet_id=packet_id)
                amount = result.get("amount", 0)
                bot.send_message(
                    chat_id=message.chat.id,
                    reply_to_message_id=message.message_id,
                    text=f"پاکت باز شد!\nمبلغ: {amount:,} تومان\nممنون {user} عزیز!"
                )
                print(f"پاکت باز شد: {amount} تومان")
            except Exception as e:
                print("خطا در باز کردن پاکت:", e)

    except Exception as e:
        print("خطا در دریافت آپدیت:", e)
        time.sleep(5)
