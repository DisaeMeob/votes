from aiogram import Bot, Dispatcher, types, executor
import logging
from config import TOKEN, ADMIN_ID
from db import create_table, add_vote, count_votes

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)
create_table()

options = ["🔴 Красный", "🟢 Зелёный", "🔵 Синий"]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    for opt in options:
        kb.add(types.InlineKeyboardButton(text=opt, callback_data=opt))
    await message.answer("🎯 Выбери цвет:", reply_markup=kb)

@dp.callback_query_handler(lambda call: call.data in options)
async def add(call: types.CallbackQuery):
    user_id = call.message.from_user.id
    vote = call.data
    add_vote(user_id, vote)
    await call.answer("✅ Ваш голос засчитан!", show_alert=True)

@dp.message_handler(commands=['results'])
async def res(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Только администратор может просматривать результаты.")
    votes = count_votes()
    if not votes:
         return await message.answer("⏳ Пока никто не проголосовал.")

    text = "📊 Результаты голосования:\n\n"
    for opt,count in votes:
        text += f"{opt}: {count}\n"
    await message.answer(text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
