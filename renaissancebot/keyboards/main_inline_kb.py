from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру
    kb = [
        [InlineKeyboardButton(text="🛒 Купить подписку", callback_data="catalog")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="💌 Отзывы", url='https://t.me/RenAIssanceOpenFeedback'),
         InlineKeyboardButton(text="🕊 FAQ", callback_data="faq")],
        [InlineKeyboardButton(text="❓ Тех. поддержка", url='https://t.me/RenAIssanceSupport'),
         InlineKeyboardButton(text="👋 Тг-канал", url='https://t.me/plusgpt4')]
        ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb)

    return kb
