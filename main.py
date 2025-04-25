from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command

from aiogram.utils.keyboard import ReplyKeyboardBuilder

import asyncio
import os


bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def com_start(message: Message):
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(
        text='/start',
    )
    keyboard.button(
        text='Java',
    )
    keyboard.button(
        text='PHONE',
        request_contact=True,
    )
    await message.answer(
        text=f'Приветствую тебя, {message.from_user.full_name}!\nЯ готов к работе!\nТы прислал: {message.text}',
        reply_markup=keyboard.as_markup(),
    )


@dp.message(F.text.lower() == 'java')
async def com_help(message: Message):
    await message.answer(
        text='JavaRush is the BEST!',
    )


@dp.message(F.text == 'STONE')
async def com_help(message: Message):
    await message.answer(
        text='STONE! STONE!',
    )


async def start_bot():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
