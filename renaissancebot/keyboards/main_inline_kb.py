from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру
    builder = InlineKeyboardBuilder()
    builder.button(text="🛒Каталог", callback_data="catalog")
    builder.button(text="👤Профиль", callback_data="profile")
    builder.button(text="💌Отзывы", url='https://t.me/RenAIssanceOpenFeedback')
    builder.button(text="🕊FAQ", callback_data="faq")
    builder.button(text="❓Тех. поддержка", url='https://t.me/RenAIssanceSupport')
    builder.button(text="👋Тг-канал", url='https://t.me/plusgpt4')
    builder.adjust(2)
    kb = builder.as_markup()
    return kb
