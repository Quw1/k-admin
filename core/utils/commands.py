from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='ну нападай'
        ),
        BotCommand(
            command='help',
            description='не гарантую'
        ),
        BotCommand(
            command='vote',
            description='вибори старости 2009'
        ),
    ]

    await bot.set_my_commands(commands)
