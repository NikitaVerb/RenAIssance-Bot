from typing import Optional

from aiogram.filters.callback_data import CallbackData


class UserDataCallbackFactory(CallbackData, prefix="solution"):
    action: str
    user_id: int
    subscription_type: str
    amount: int

