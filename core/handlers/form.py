from aiogram import Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.utils.statesform import StepsForm
from core.handlers.appsched import send_message_middleware
from datetime import datetime, timedelta


async def get_form(message: Message, state: FSMContext):
    await message.answer(f'Test form. What\'s your name?')
    await state.set_state(StepsForm.GET_NAME)


async def get_name(message: Message, state: FSMContext):
    await message.answer(f'Your name: {message.text} What\'s your surname?')
    await state.update_data(name=message.text)
    await state.set_state(StepsForm.GET_SURNAME)


async def get_surname(message: Message, state: FSMContext):
    await message.answer(f'Your surname: {message.text} What\'s your age?')
    await state.update_data(surname=message.text)
    await state.set_state(StepsForm.GET_AGE)


async def get_age(message: Message, bot: Bot, state: FSMContext, apscheduler: AsyncIOScheduler):
    await message.answer(f'Your age: {message.text} What\'s your age?')
    context_data = await state.get_data()
    await message.answer(f'Saved data: \r\n{str(context_data)}')
    name = context_data.get('name')
    surname = context_data.get('surname')
    data_user = f"Your data: \r\n" \
                f"Name: {name} Surname: {surname} Age {message.text}"
    await message.answer(data_user)
    await state.clear()
    apscheduler.add_job(send_message_middleware, trigger='date', run_date=datetime.now() + timedelta(seconds=60),
                        kwargs={'chat_id': message.from_user.id, 'msg': 'Sent after some time after form fill'})



