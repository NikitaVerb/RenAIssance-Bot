from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_approval_inline_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Одобрить", callback_data="approve")],
        [InlineKeyboardButton(text="Есть проблема", callback_data="problem")]
    ])
    return keyboard