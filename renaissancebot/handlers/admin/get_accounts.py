from aiogram import Router
from aiogram import types
from aiogram.filters import Command

import renaissancebot.filters.user_rights
from db import get_emails_with_user_count

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('get_accounts'))
async def get_accounts(message: types.Message):
    result = await get_emails_with_user_count()
    msg = '<аккаунт> <пароль> - <кол-во юзеров>\n'
    for item in result:
        msg += f'{item[0]} {item[1]} - {item[2]}\n'
    await message.answer(msg, parse_mode=None)
