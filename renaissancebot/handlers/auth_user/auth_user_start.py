from aiogram import Router
from aiogram import types
from aiogram.filters import Command

import filters.user_rights

router = Router()
router.message.filter(filters.user_rights.UserIsLogged())


@router.message(Command("start_registration"))
async def start_registration(message: types.Message):
    await message.answer(
        "Вы уже зарегистрированны, если вы хотите сменить почту, то отправьте команду /edit_email."
        " Если хотите удалить свой профиль, отправьте команду /del_profile")
