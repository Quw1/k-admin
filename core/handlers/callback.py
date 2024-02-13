from aiogram import Bot
from aiogram.types import CallbackQuery
from core.utils.callbackdata import CallbackTestInfo
from aiogram.types import Message
from core.utils.dbconnect import Request
from aiogram.fsm.context import FSMContext
from core.keyboards.inline import get_vote_markup, get_confirm_vote_markup
from core.utils.statesform import UserVoting


async def do_test(call: CallbackQuery, bot: Bot, callback_data: CallbackTestInfo):
    btn = callback_data.btn_num
    answer = f'You pressed the button #{btn}'
    await call.message.answer(answer)
    await call.message.edit_text(answer)
    await call.answer()




