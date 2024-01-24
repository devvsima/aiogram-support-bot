from aiogram.types import (
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.callback_data import CallbackData
from database.supporters import supporters_list
from random import shuffle,choice
from loader import dp

support_callback = CallbackData("ask_support", "messages", "user_id", "as_user")
cancel_support_callback = CallbackData("cancel_support", "user_id")


async def check_support_available(support_id):
    state = dp.current_state(chat=support_id, user=support_id)
    state_str = str(await state.get_state())
    if state_str == "in_support":
        return
    else:
        return support_id


async def get_support_manager():
    support_ids = supporters_list()
    shuffle(support_ids)
    for support_id in support_ids:
        support_id = await check_support_available(support_id)
        if support_id:
            return support_id


async def support_keyboard(messages, user_id=None):
    support_ids = supporters_list()
    if user_id:
        contact_id = int(user_id)
        as_user = "no"
        text = "Ответить пользователю"
    else:
        contact_id = await get_support_manager()
        as_user = "yes"
        if messages == "many" and contact_id is None:
            return False
        elif messages == "one" and contact_id is None:
            contact_id = choice(support_ids)
        if messages == "one":
            text = "Написать 1 сообщение в техподдержку"
        else:
            text = "Связаться с опертором"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=text,
            callback_data=support_callback.new(messages=messages,
                                               user_id=contact_id,
                                               as_user=as_user
                                               )
        )
    )
    if messages == "many":keyboard.add(
        InlineKeyboardButton(
            text="Завершить сеанс",
            callback_data=cancel_support_callback.new(user_id=contact_id)
        )
    )
    return keyboard