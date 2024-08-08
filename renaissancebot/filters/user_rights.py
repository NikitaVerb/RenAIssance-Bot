from aiogram.filters import BaseFilter
from aiogram.types import Message

from renaissancebot.db import check_user_in_db, check_user_is_admin


class UserIsLogged(BaseFilter):
    async def __call__(self, message: Message):
        return await check_user_in_db(message.from_user.id)


class UserIsNotLogged(BaseFilter):
    async def __call__(self, message: Message):
        return not (await check_user_in_db(message.from_user.id))


class UserIsAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return await check_user_is_admin(message.from_user.id)
