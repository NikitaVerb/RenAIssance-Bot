from aiogram import Router
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from email_validator import validate_email, EmailNotValidError
from aiogram import F

import renaissancebot.filters.user_rights
from db import add_user
from db import check_user_email_in_db

router = Router()
router.message.filter(renaissancebot.filters.user_rights.UserIsNotLogged())


class RegistrationState(StatesGroup):
    user_email = State()
    cancel = State()


@router.message(Command("cancel"))
async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state:
        await state.clear()
        await message.answer(
            "Процесс регистрации был отменен. Вы можете начать регистрацию снова, отправив команду /start_registration.")
    else:
        await message.answer("В данный момент нет активного процесса регистрации.")


@router.message(StateFilter(None), Command("start_registration"))
async def start_registration(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш email:")
    await message.answer("Вы можете остановить процесс регистрации, отправив команду /cancel")
    await state.set_state(RegistrationState.user_email)


@router.callback_query(F.data.startswith("start_registration"))
async def start_registration_callback(callback_query: types.CallbackQuery, state: FSMContext):
    # Отправляем сообщение о начале регистрации
    await callback_query.message.answer("Пожалуйста, введите ваш email:")
    await callback_query.message.answer("Вы можете остановить процесс регистрации, отправив команду /cancel")
    # Устанавливаем состояние регистрации
    await state.set_state(RegistrationState.user_email.state)
    # Удаляем сообщение с кнопкой
    await callback_query.message.delete()


@router.message(RegistrationState.user_email)
async def process_user_email(message: types.Message, state: FSMContext):
    user_email = message.text

    try:
        # Проверяем валидность email
        valid = validate_email(user_email)
        # Если email валиден, возвращаем его
        email = valid.email
        if await check_user_email_in_db(email):
            await message.answer("Пользователь с таким email уже существует")
        else:
            await message.answer('Email принят. Обработка завершена.')
            await add_user(message.from_user.id, email)
            await message.answer("Вы успешно зарегистрированы!", parse_mode=ParseMode.MARKDOWN)
            await state.clear()
    except EmailNotValidError as e:
        # Если email невалидный, сообщаем об ошибке
        await message.answer(f"Неверный формат email. Пожалуйста, введите корректный email. Ошибка: {str(e)}")
