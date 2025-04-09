from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbSessionMiddleware(BaseMiddleware):

    def __init__(self, session_pool: async_sessionmaker) -> None:
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
        try:
            return await handler(event, data)
        except Exception:
            await session.rollback()
            raise
        finally:
            # The garbage collector is trying to clean up non-checked-in connection...
            # Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly...
            await session.close() # предотвращение ошибки