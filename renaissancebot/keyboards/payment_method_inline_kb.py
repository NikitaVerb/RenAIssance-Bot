from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def payment_method_inline_kb() -> InlineKeyboardMarkup:
    # Создаем inline-клавиатуру с одной кнопкой
    builder = InlineKeyboardBuilder()
    builder.button(text="💳 Карта РФ", callback_data="invoice")
    builder.button(text="💲 Криптовалюта", callback_data="crypto")
    builder.button(text="↩ Назад к подпискам", callback_data="catalog")
    builder.adjust(1)
    kb = builder.as_markup()
    return kb
