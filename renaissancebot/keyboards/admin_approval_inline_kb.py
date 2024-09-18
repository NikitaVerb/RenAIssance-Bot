from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.user_data_callback_factory import UserDataCallbackFactory


def admin_approval_inline_kb(user_id: int, sub_type: str, amount: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Одобрить", callback_data=UserDataCallbackFactory(action="approve",
                                                                          user_id=user_id,
                                                                          subscription_type=sub_type,
                                                                          amount=amount))
    builder.button(text="Есть проблема", callback_data=UserDataCallbackFactory(action="problem",
                                                                               user_id=user_id,
                                                                               subscription_type=sub_type,
                                                                               amount=amount))
    return builder.as_markup()
