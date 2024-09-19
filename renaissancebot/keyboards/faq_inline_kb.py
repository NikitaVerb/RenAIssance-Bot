from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def faq_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру
    builder = InlineKeyboardBuilder()
    builder.button(text="Как это работает?", callback_data="faq_1")
    builder.button(text="Почему мы?", callback_data="faq_2")
    builder.button(text="Будет ли хватать запросов?", callback_data="faq_3")
    builder.button(text="На какой период действует подписка?", callback_data="faq_4")
    builder.button(text="Нужен ли VPN?", callback_data="faq_5")
    builder.button(text="↩ Назад в меню", callback_data="menu")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
