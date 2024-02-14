from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable
from core.settings import settings
import logging


class BanMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not event.from_user.id == settings.bots.admin_id:
            user = f'user{event.from_user.id}'
            check_user = await self.storage.redis.get(name=user)
            if check_user:
                res = int(check_user.decode())
                if res == 1:
                    await self.storage.redis.set(name=user, value=2)
                    await event.answer_sticker('CAACAgEAAxkBAAEpea9lzKJuD8z2bc4ObxbzjsgZCn_a3QACuwEAAnY3dj8KS-oFMQOZHTQE')
                    return await event.answer('догрався? тебе забанили\n\nдумаєш шо помилився? пиши @kft_cj_bot')
                elif res == 2:
                    return

            return await handler(event, data)
        else:
            try:
                splited = event.text.split()

                if splited[0] == '/ban':
                    await self.storage.redis.set(name=f'user{splited[1]}', value=1)
                    return await event.answer(f'banned {splited[1]}')

                elif splited[0] == '/unban':
                    await self.storage.redis.set(name=f'user{splited[1]}', value=0)
                    return await event.answer(f'unbanned {splited[1]}')

                else:
                    return await handler(event, data)

            except Exception as e:
                logging.exception(e)
                return await event.answer('wrong use')

