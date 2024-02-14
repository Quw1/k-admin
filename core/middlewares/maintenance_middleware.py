from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable
from core.settings import settings


class MaintenanceMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.mt = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if not event.from_user.id == settings.bots.admin_id and settings.bots.maintenance:
            await event.answer('бот вауті, почекай трохи')
        else:
            return await handler(event, data)

