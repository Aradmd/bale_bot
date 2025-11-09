import os
from bale import Bot

bot = Bot(token=os.getenv("BOT_TOKEN"))

@bot.router.message()
async def detect_packet(message):
    text = message.text or ""
    if "پاکت" not in text.lower():
        return
    if not message.packet:
        return

    packet_id = message.packet.packet_id
    user = message.from_user.first_name or "ناشناس"

    try:
        result = await bot.open_packet(packet_id=packet_id)
        amount = result.get("amount", 0)
        await bot.send_message(
            chat_id=message.chat.id,
            reply_to_message_id=message.message_id,
            text=f"پاکت باز شد!\nمبلغ: {amount:,} تومان\nممنون {user} عزیز!"
        )
        print(f"پاکت باز شد: {amount} تومان")
    except Exception as e:
        print("خطا:", e)

print("بات پاکت باز کن فعال شد...")
bot.run()
