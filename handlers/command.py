from aiogram import Bot, Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums import ChatAction, ParseMode
from aiogram.fsm.context import FSMContext

from classes import gpt_client
from .handlers_state import ChatGPTRequests

import os

from keyboards import kb_reply, ikb_celebrity, ikb_quiz

command_router = Router()


@command_router.message(ChatGPTRequests.wait_for_request)
async def wait_for_gpt_handler(message: Message, bot: Bot, state: FSMContext):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    gpt_response = await gpt_client.gpt_request(message.text)
    photo_path = os.path.join('resources', 'images', 'gpt.jpg')
    photo = FSInputFile(photo_path)
    await message.answer_photo(
        photo=photo,
        caption=gpt_response,
    )
    await state.clear()


@command_router.message(F.text == 'Закончить')
@command_router.message(Command('start'))
async def com_start(message: Message):
    photo_path = os.path.join('resources', 'images', 'main.jpg')
    text_path = os.path.join('resources', 'messages', 'main.txt')
    photo = FSInputFile(photo_path)
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
    ]
    with open(text_path, 'r', encoding='UTF-8') as file:
        msg_text = file.read()
    await message.answer_photo(
        photo=photo,
        caption=msg_text,
        reply_markup=kb_reply(buttons),
    )


@command_router.message(F.text == 'Хочу еще факт')
@command_router.message(Command('random'))
async def com_random(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    photo_path = os.path.join('resources', 'images', 'random.jpg')
    photo = FSInputFile(photo_path)
    buttons = [
        'Хочу еще факт',
        'Закончить',
    ]
    msg_text = await gpt_client.random_request()
    await message.answer_photo(
        photo=photo,
        caption=msg_text,
        reply_markup=kb_reply(buttons),
    )


@command_router.message(Command('gpt'))
async def com_gpt(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(ChatGPTRequests.wait_for_request)
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    photo_path = os.path.join('resources', 'images', 'gpt.jpg')
    msg_path = os.path.join('resources', 'messages', 'gpt.txt')
    photo = FSInputFile(photo_path)
    with open(msg_path, 'r', encoding='UTF-8') as file:
        message_text = file.read()
    await message.answer_photo(
        photo=photo,
        caption=message_text,
    )


@command_router.message(Command('talk'))
async def com_talk(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
    photo_path = os.path.join('resources', 'images', 'talk.jpg')
    msg_path = os.path.join('resources', 'messages', 'talk.txt')
    photo = FSInputFile(photo_path)
    with open(msg_path, 'r', encoding='UTF-8') as file:
        message_text = file.read()
    await message.answer_photo(
        photo=photo,
        caption=message_text,
        reply_markup=ikb_celebrity(),
    )


@command_router.message(Command('quiz'))
async def com_quiz(message: Message, bot: Bot):
    await bot.send_chat_action(
        chat_id=message.from_user.id,
        action=ChatAction.TYPING,
    )
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
