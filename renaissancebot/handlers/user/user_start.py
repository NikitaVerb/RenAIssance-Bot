from aiogram import Router
from aiogram import types
from aiogram.filters import Command
from renaissancebot.db import check_user_in_db

router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    text = await check_user_in_db('kuz')
    await message.answer(f"{text}")
    await message.answer(f'Hi, {message.from_user.full_name}, id: {message.from_user.id}')
