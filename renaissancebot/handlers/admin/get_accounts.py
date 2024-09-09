from aiogram import Router
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command

import filters.user_rights
from db import get_emails_with_user_count, get_inactive_user_count_by_email

router = Router()
router.message.filter(filters.user_rights.UserIsAdmin())


@router.message(Command('get_accounts'))
async def get_accounts(message: types.Message):
    result = await get_emails_with_user_count()
    msg = '<аккаунт> <пароль> - <юзеры> <недейств юзеры>\n\n'
    for item in result:
        msg += f'`{item[0]}` `{item[1]}` - {item[2]} {await get_inactive_user_count_by_email(item[0])}\n\n'
    await message.answer(msg, parse_mode=ParseMode.MARKDOWN)
