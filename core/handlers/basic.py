from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from core.keyboards.reply import reply_keyboard, loc_tel_poll_keyboard, get_reply_keyboard
from core.keyboards.inline import inline_test, get_inline_keyboard
from core.utils.dbconnect import Request
from core.utils.statelogin import UserState


async def get_start(message: Message, bot: Bot, request: Request):
    await request.add_data_telegram(message.from_user.id, message.from_user.first_name)
    await message.answer('не тягни, жмякай /love')


async def get_other(message: Message, bot: Bot):
    if message.chat.type == 'private':
        await message.answer('га?')


async def get_help(message: Message, bot: Bot):
    await message.answer(f'не можу')


async def get_you(message: Message, bot: Bot):
    await message.answer('а я тебе ні (лан жартую)')


async def get_chat_id(message: Message, bot: Bot):
    await message.answer(str(message.chat.id))


