from aiogram import Bot
from aiogram.types import Message
from core.settings import settings


async def set_mt(message: Message, bot: Bot):
    settings.bots.maintenance = abs(int(settings.bots.maintenance) - 1)
    await message.answer(f'Maintenance is now: {settings.bots.maintenance}')


async def set_voting(message: Message, bot: Bot):
    settings.bots.voting = abs(int(settings.bots.voting) - 1)
    print(settings.bots.voting)
    await message.answer(f'voting is: {settings.bots.voting}')


async def output_to_group(message: Message, bot: Bot):
    await bot.send_message(settings.bots.supergroup_id, message.text[4:])
