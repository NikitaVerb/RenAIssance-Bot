from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def reg_from_catalog_inline_markup() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="Зарегистрироваться", callback_data="start_registration")
    builder.button(text="↩ Назад к подпискам", callback_data="catalog")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
