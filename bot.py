import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import BOT_TOKEN
from database import init_db, add_user, get_user, update_user
from exercises import sequence
from logic import get_level

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_states = {}

@dp.message(Command("start"))
async def start(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer(
        "🧠 NeuroGym\n\n"
        "/train — тренировка\n"
        "/stats — статистика"
    )

@dp.message(Command("train"))
async def train(message: types.Message):
    user = await get_user(message.from_user.id)
    lvl = user[1]
    seq = sequence(lvl)
    user_states[message.from_user.id] = seq

    await message.answer(
        "Запомни последовательность:\n" +
        " ".join(map(str, seq))
    )
    await asyncio.sleep(7)
    await message.answer("Введи ответ:")

@dp.message(Command("stats"))
async def stats(message: types.Message):
    user = await get_user(message.from_user.id)
    await message.answer(
        f"🏆 Баллы: {user[0]}\n"
        f"🎯 Уровень: {user[1]}"
    )

@dp.message()
async def answer(message: types.Message):
    if message.from_user.id not in user_states:
        return

    correct = user_states.pop(message.from_user.id)
    user = await get_user(message.from_user.id)

    try:
        if list(map(int, message.text.split())) == correct:
            points = user[0] + 10
            level = get_level(points)
            await update_user(message.from_user.id, points, level)
            await message.answer("✅ Верно! +10 баллов")
        else:
            await message.answer("❌ Неверно")
    except:
        await message.answer("Ошибка ввода")

async def main():
    await init_db()
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
