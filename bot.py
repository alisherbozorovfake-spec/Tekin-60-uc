import json
import random
import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN, REQUIRED_CHANNEL, ANNOUNCE_CHANNEL, MAX_SPINS_PER_DAY

bot = Bot(7522892324:AAGR42CFy8HRyGz44S7LYj6Z_NFq2F0xayQ)
dp = Dispatcher(bot)

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(data):
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(@alishere100k, 8437585105)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    if not await check_sub(msg.from_user.id):
        btn = InlineKeyboardMarkup().add(
            InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")
        )
        await msg.answer("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=btn)
        return

    await msg.answer("🎰 Random botga xush kelibsiz!\n\n🎁 Kuniga 3 marta aylantira olasiz.")

@dp.message_handler(commands=["spin"])
async def spin(msg: types.Message):
    if not await check_sub(msg.from_user.id):
        await msg.answer("❌ Avval kanalga obuna bo‘ling!")
        return

    users = load_users()
    uid = str(msg.from_user.id)
    today = str(datetime.date.today())

    if uid not in users:
        users[uid] = {"date": today, "count": 0}

    if users[uid]["date"] != today:
        users[uid] = {"date": today, "count": 0}

    if users[uid]["count"] >= MAX_SPINS_PER_DAY:
        await msg.answer("⛔ Bugungi limit tugadi. Ertaga yana urinib ko‘ring.")
        return

    users[uid]["count"] += 1
    save_users(users)

    prize = random.choice(["❌ Hech narsa", "🎮 PUBG Mobile 60 UC"])

    if prize != "❌ Hech narsa":
        username = msg.from_user.username
        mention = f"@{username}" if username else f"<a href='tg://user?id={uid}'>Profil</a>"

        await bot.send_message(
            ANNOUNCE_CHANNEL,
            f"🏆 YANGI G‘OLIB!\n\n"
            f"👤 G‘olib: {mention}\n"
            f"🎁 Sovrin: {prize}",
            parse_mode="HTML"
        )

    await msg.answer(f"🎰 Natija:\n\n{prize}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
