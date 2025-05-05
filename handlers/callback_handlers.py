from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, FSInputFile

import os

from keyboards.callback_data import CelebrityData

callback_router = Router()


@callback_router.callback_query(CelebrityData.filter(F.button == 'select_celebrity'))
async def celebrity_callbacks(callback: CallbackQuery, callback_data: CelebrityData, bot: Bot):
    photo_path = os.path.join('resources', 'images', callback_data.file_name + '.jpg')
    msg_path = os.path.join('resources', 'prompts', callback_data.file_name + '.txt')
    with open(msg_path, 'r', encoding='UTF-8') as file:
        message_text = file.read()
    photo = FSInputFile(photo_path)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=photo,
        caption=message_text,
    )
