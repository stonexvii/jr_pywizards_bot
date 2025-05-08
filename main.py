from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import asyncio
import os

import misc

from handlers import routers

bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    default=DefaultBotProperties(
        parse_mode=ParseMode.MARKDOWN,
    )
)
dp = Dispatcher()


async def start_bot():
    dp.startup.register(misc.on_start)
    dp.shutdown.register(misc.on_shutdown)
    dp.include_routers(*routers)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
