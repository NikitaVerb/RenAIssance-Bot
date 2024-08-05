from aiogram import Router
from aiogram import types
from aiogram.filters import Command

import renaissancebot.filters.user_rights

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserRightFilter())


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Hi, {message.from_user.full_name}, id: {message.from_user.id}'
                         f'вы авторизованы')
