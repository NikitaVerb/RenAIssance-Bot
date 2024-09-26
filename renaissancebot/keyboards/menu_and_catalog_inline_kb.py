from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def menu_and_catalog_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒 Купить подписку", callback_data="catalog")
    builder.button(text="↩ Назад в меню", callback_data="menu")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
