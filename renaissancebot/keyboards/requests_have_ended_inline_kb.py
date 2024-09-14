from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def requests_have_ended_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="Закончились запросы", callback_data="req_have_ended")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
