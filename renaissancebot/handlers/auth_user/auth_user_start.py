from aiogram import Router
from aiogram import types
from aiogram.filters import Command

import renaissancebot.filters.user_rights
from keyboards import get_main_kb

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsLogged())


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(f'Hi, {message.from_user.full_name}, id: {message.from_user.id}'
                         f'вы авторизованы')
    await message.answer(
        'Если хотите посмотреть каталог, наш телеграм-канал или задать вопрос, воспользуйтесь кнопками под клавиатурой',
        reply_markup=get_main_kb())
    # TODO await message.answer("Каталог", reply_markup=catalog_inline_markup())


@router.message(Command("start_registration"))
async def start_registration(message: types.Message):
    await message.answer(
        "Вы уже зарегестрированны, если вы хотите сменить почту, то отправьте команду /edit_email."
        " Если хотите удалить свой профиль, отправьте команду /del_profile")
