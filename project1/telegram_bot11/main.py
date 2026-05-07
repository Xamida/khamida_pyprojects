import asyncio
import time

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
import os
from aiogram.filters import Command

from config import get_value
from keyboards import buttons_category
from open_pars import pars_texno

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = Bot(
    TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)
dp = Dispatcher()


@dp.message(Command("start"))
async def command_start(message: Message):
    full_name = message.from_user.full_name
    await message.answer(f"Hello {full_name}! Choose a category 👇", reply_markup=buttons_category())
    await show_category_menu(message)


async def show_category_menu(message: Message):
    markup = buttons_category()
    markup.one_time_keyboard = True
    await message.answer("Choose a category 👇", reply_markup=markup)


@dp.message()
async def get_product_mediapark(message: Message):
    category_text = message.text

    category_key = get_value(category_text)
    if category_key is None:
        return await message.answer(
            "This category does not exist!\n"
            "Please, choose categories below👇"
        )

    get_product = pars_texno(category_key)
    if not get_product:
        return await message.answer("⚠ The product is not found in this category")

    for product in get_product:
        image = product.get('image')
        title = product.get('title')
        price = product.get('price')

        await asyncio.sleep(0.5)
        await message.answer_photo(
            photo=image,
            caption=f"{title}\n\n{price}",
        )

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())