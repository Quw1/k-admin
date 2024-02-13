from aiogram import Bot
from aiogram.types import Message
from core.utils.dbconnect import Request
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.enums.chat_member_status import ChatMemberStatus
from core.utils.callbackdata import CallbackTestInfo
from core.keyboards.inline import get_vote_markup, get_confirm_vote_markup, get_start_voting
from core.utils.statesform import UserVoting
from core.settings import settings


async def start_voting(message: Message, bot: Bot, request: Request, state: FSMContext):
    if message.chat.type != 'private':
        await message.reply('іді в лс')
    else:
        try:
            user = await bot.get_chat_member(chat_id=settings.bots.supergroup_id, user_id=message.from_user.id)
            if user.status != ChatMemberStatus.LEFT:
                res = await request.get_vote(user_id=message.from_user.id)
                if res is None:
                    await state.set_state(UserVoting.START_VOTING)
                    await message.answer('канали голосування відкриті, шо, готовий?', reply_markup=get_start_voting())
                else:
                    await message.answer('та куда, ти вже все')
            else:
                await message.answer('ти хто такий')
        except Exception as e:
            print(e)
            await message.answer(f'ти хто такий? я? я є {e}')


async def make_vote(call: CallbackQuery, bot: Bot, callback_data: CallbackTestInfo, state: FSMContext):
    await call.answer()
    await state.set_state(UserVoting.CHOOSE_CANDIDATE)
    await call.message.edit_text('кого старостою?', reply_markup=get_vote_markup())


async def ask_confirm_vote(call: CallbackQuery, bot: Bot, callback_data: CallbackTestInfo, state: FSMContext):
    await call.answer()
    candidate = callback_data.candidate
    await state.set_state(UserVoting.CONFIRM)
    await state.update_data(candidate=candidate)
    await call.message.edit_text(f'голосуємо за {candidate}?', reply_markup=get_confirm_vote_markup())


async def confirm_vote(call: CallbackQuery, bot: Bot, request: Request, callback_data: CallbackTestInfo, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    candidate = data.get('candidate')
    await state.clear()
    user_id = call.from_user.id
    res = await request.get_vote(user_id=user_id)
    if res is None:
        res = await request.add_vote(user_id=user_id, username=call.from_user.username, name=call.from_user.first_name,
                                     voted=True, voted_for=candidate)
        print(res)
        await call.message.edit_text(f'ну я записав - {candidate}')
    else:
        await call.message.edit_text(f'альо, ти вже голосував')


async def back_to_manu_vote(call: CallbackQuery, bot: Bot, callback_data: CallbackTestInfo, state: FSMContext):
    await call.answer()
    await state.clear()
    await state.set_state(UserVoting.CHOOSE_CANDIDATE)
    await call.message.edit_text('кого старостою?', reply_markup=get_vote_markup())


async def show_warning(call: CallbackQuery, bot: Bot, callback_data: CallbackTestInfo, state: FSMContext):
    await call.answer(show_alert=True, text='не спам /vote, використовуй лише одне вікошко для голосування. якшо шось'
                                            ' пішло не так, пиши /vote ще раз')
