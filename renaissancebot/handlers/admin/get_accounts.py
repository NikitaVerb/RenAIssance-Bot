from aiogram import Router
from aiogram import types
from aiogram.filters import Command

import renaissancebot.filters.user_rights
from db import get_emails_with_user_count, get_inactive_user_count_by_email

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsAdmin())


@router.message(Command('get_accounts'))
async def get_accounts(message: types.Message):
    result = await get_emails_with_user_count()
    msg = '<аккаунт> <пароль> - <юзеры> <недейств юзеры>\n'
    for item in result:
        msg += f'{item[0]} {item[1]} - {item[2]} {await get_inactive_user_count_by_email(item[0])}\n'
    await message.answer(msg, parse_mode=None)
