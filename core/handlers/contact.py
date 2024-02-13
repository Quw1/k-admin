from aiogram.types import Message
from aiogram import Bot


async def get_true_contact(message: Message, bot: Bot, phone: str):
    await message.answer(f'Phone number received {phone}')


async def get_fake_contact(message: Message, bot: Bot):
    await message.answer(f'Liar?')
