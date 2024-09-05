from aiogram import F, Bot
from aiogram import Router
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from email_validator import validate_email, EmailNotValidError

import renaissancebot.filters.user_rights
from db import add_user
from db import check_user_email_in_db
from keyboards import back_to_menu_inline_kb
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
            "Процесс регистрации был отменен.", reply_markup=back_to_menu_inline_kb())
    else:
        await message.answer("В данный момент нет активного процесса регистрации.")


@router.message(StateFilter(None), Command("start_registration"))
async def start_registration(message: types.Message, state: FSMContext, bot: Bot):
    await bot.edit_message_text(chat_id=message.chat.id,
                                message_id=message.message_id,
                                text="Пожалуйста, введите ваш email.\nВы можете остановить процесс регистрации,"
                                     " отправив команду /cancel")
    await state.set_state(RegistrationState.user_email)


@router.callback_query(F.data.startswith("start_registration"))
async def start_registration_callback(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    # Отправляем сообщение о начале регистрации
    await bot.edit_message_text(chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                text="Пожалуйста, введите ваш email.\nВы можете остановить процесс регистрации,"
                                     " отправив команду /cancel")
    # Устанавливаем состояние регистрации
    await state.set_state(RegistrationState.user_email.state)
    # Удаляем сообщение с кнопкой


@router.message(RegistrationState.user_email)
async def process_user_email(message: types.Message, state: FSMContext, bot: Bot):
    user_email = message.text

    try:
        # Проверяем валидность email
        valid = validate_email(user_email)
        # Если email валиден, возвращаем его
        email = valid.email
        if await check_user_email_in_db(email):
            await message.answer("Пользователь с таким email уже существует. Пожалуйста, введите корректный email:")
        else:
            await add_user(message.from_user.id, email)
            await message.answer("Вы успешно зарегистрированы!\n"
                                 "Теперь вы можете совершать покупки и следить за статусом подписок в профиле",
                                 parse_mode=ParseMode.MARKDOWN, reply_markup=back_to_menu_inline_kb())
            await state.clear()
    except EmailNotValidError as e:
        # Если email невалидный, сообщаем об ошибке
        await message.answer(f"Неверный формат email. Пожалуйста, введите корректный email:")
