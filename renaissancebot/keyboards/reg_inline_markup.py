from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def reg_inline_markup() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="Зарегестрироваться", callback_data="start_registration")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
