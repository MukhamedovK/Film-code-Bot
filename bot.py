import logging

from aiogram import Bot, Dispatcher, executor, types
from database import *
from config import BOT_TOKEN, ADMINS


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await create_user(message.from_user.id, message.from_user.username)
    await message.answer("Здравствуйте! Я бот для нахождения кино и фильмов! 🎬\n\nОтправьте мне код кино или фильма!")


@dp.message_handler(content_types=['video'])
async def get_video_handler(message: types.Message):
    if message.from_user.id in ADMINS:
        caption = message.caption.split("\n")
        film_id = message.video.file_id
        await insert_film(int(caption[0]), caption[1], film_id)
        await message.answer("<b>Фильм добавлен! 👌</b>")


@dp.message_handler(content_types=['text'])
async def get_film_handler(message: types.Message):
    text = message.text

    if text.isdigit():
        data = await get_film_by_code(text)
        if data:
            await message.answer_video(data[2], caption=f"<b>КОД: {data[0]}\nНАЗВАНИЕ: <i>{data[1]}</i></b>")

        else:
            await message.answer("Извините, такой код не существует! ❌")
    else:
        await message.answer("Извините, такой код не существует! ❌")










if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=create_tables)