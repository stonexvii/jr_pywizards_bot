from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from classes import gpt_client
from classes.resource import Resource
from classes.chat_gpt import GPTMessage
from .handlers_state import ChatGPTRequests
from misc import bot_thinking


from keyboards import kb_reply, ikb_celebrity, ikb_quiz_select_topic

command_router = Router()


@command_router.message(F.text == 'Закончить')
@command_router.message(Command('start'))
async def com_start(message: Message):
    resource = Resource('main')
    buttons = [
        '/random',
        '/gpt',
        '/talk',
        '/quiz',
    ]
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=kb_reply(buttons),
    )


@command_router.message(F.text == 'Хочу еще факт')
@command_router.message(Command('random'))
async def com_random(message: Message):
    await bot_thinking(message)
    resource = Resource('random')
    gpt_message = GPTMessage('random')
    buttons = [
        'Хочу еще факт',
        'Закончить',
    ]
    msg_text = await gpt_client.request(gpt_message)
    await message.answer_photo(
        photo=resource.photo,
        caption=msg_text,
        reply_markup=kb_reply(buttons),
    )


@command_router.message(Command('gpt'))
async def com_gpt(message: Message, state: FSMContext):
    await state.set_state(ChatGPTRequests.wait_for_request)
    await bot_thinking(message)
    resource = Resource('gpt')
    await message.answer_photo(
        **resource.as_kwargs(),
    )


@command_router.message(Command('talk'))
async def com_talk(message: Message):
    await bot_thinking(message)
    resource = Resource('talk')
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_celebrity(),
    )


@command_router.message(Command('quiz'))
async def com_quiz(message: Message):
    await bot_thinking(message)
    resource = Resource('quiz')
    await message.answer_photo(
        **resource.as_kwargs(),
        reply_markup=ikb_quiz_select_topic(),
    )
