from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums import ChatAction, ParseMode
from aiogram.fsm.context import FSMContext

from classes import gpt_client
from classes.chat_gpt import BotPath, BotPhoto, BotText, GPTMessage
from .handlers_state import ChatGPTRequests
from misc import bot_thinking

import os

from keyboards import kb_reply, ikb_celebrity, ikb_quiz

command_router = Router()


@command_router.message(F.text == 'Закончить')
@command_router.message(Command('start'))
async def com_start(message: Message):
    photo = BotPhoto('main').photo
    message_text = BotText('main').text
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
    ]
    await message.answer_photo(
        photo=photo,
        caption=message_text,
        reply_markup=kb_reply(buttons),
    )


@command_router.message(F.text == 'Хочу еще факт')
@command_router.message(Command('random'))
async def com_random(message: Message, bot: Bot):
    await bot_thinking(message)
    photo = BotPhoto('random').photo
    request_message = GPTMessage('random')
    buttons = [
        'Хочу еще факт',
        'Закончить',
    ]
    msg_text = await gpt_client.request(request_message)
    await message.answer_photo(
        photo=photo,
        caption=msg_text,
        reply_markup=kb_reply(buttons),
    )


@command_router.message(Command('gpt'))
async def com_gpt(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(ChatGPTRequests.wait_for_request)
    await bot_thinking(message)
    photo = BotPhoto('gpt').photo
    message_text = BotText('gpt').text
    await message.answer_photo(
        photo=photo,
        caption=message_text,
    )


@command_router.message(Command('talk'))
async def com_talk(message: Message, bot: Bot):
    await bot_thinking(message)
    photo = BotPhoto('talk').photo
    message_text = BotText('talk').text
    await message.answer_photo(
        photo=photo,
        caption=message_text,
        reply_markup=ikb_celebrity(),
    )


@command_router.message(Command('quiz'))
async def com_quiz(message: Message, bot: Bot):
    await bot_thinking(message)
    photo_path = os.path.join('resources', 'images', 'quiz.jpg')
    msg_path = os.path.join('resources', 'messages', 'quiz.txt')
    photo = FSInputFile(photo_path)
    with open(msg_path, 'r', encoding='UTF-8') as file:
        message_text = file.read()
    await message.answer_photo(
        photo=photo,
        caption=message_text,
        reply_markup=ikb_quiz(),
    )
