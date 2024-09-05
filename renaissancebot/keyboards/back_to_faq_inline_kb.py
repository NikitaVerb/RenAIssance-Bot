from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_to_faq_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="↩Назад", callback_data="faq")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
