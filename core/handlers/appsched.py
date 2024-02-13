from aiogram import Bot
from core.settings import settings


async def send_message_time(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f"Sent after some delay")


async def send_message_cron(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f"Sent at some time")


async def send_message_interval(bot: Bot):
    await bot.send_message(settings.bots.admin_id, f"Sent interval")


async def send_message_middleware(bot: Bot, chat_id: int, msg: str):
    await bot.send_message(chat_id, msg)
