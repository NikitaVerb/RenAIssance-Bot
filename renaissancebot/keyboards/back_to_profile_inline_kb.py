from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_to_profile_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="↩ Назад", callback_data="profile")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
