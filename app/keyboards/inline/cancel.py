from aiogram.types import (
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.callback_data import CallbackData
from database.supporters import supporters_list
from random import shuffle, choice
from loader import dp
from app.keyboards.inline.support import cancel_support_callback


def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Закрыть диалог",
                    callback_data=cancel_support_callback.new(
                        user_id=user_id
                        )
                )
            ]
        ]
    )
