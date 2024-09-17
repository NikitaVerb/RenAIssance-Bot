from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Клавиатура для поддержки
def support_inline_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Связаться с поддержкой", url="https://t.me/RenAIssanceSupport")],
        [InlineKeyboardButton(text="↩ Назад в меню", callback_data="menu")]
    ])
