import os
from bale import Bot, Update, Message

bot = Bot(token=os.getenv("BOT_TOKEN"))

@bot.handler(message_type="text")
def detect_packet(update: Update, message: Message):
    text = message.text or ""
    if "پاکت" not in text.lower():
        return
    if not message.packet:
        return

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
        print("خطا:", e)

print("بات پاکت باز کن فعال شد...")
bot.run()
