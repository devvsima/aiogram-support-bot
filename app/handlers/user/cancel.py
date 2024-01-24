from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot

from app.keyboards.inline.support import (
    support_keyboard,
    support_callback,
    check_support_available,
    get_support_manager,
    cancel_support_callback
)
@dp.callback_query_handler(cancel_support_callback.filter(),state=["in_support","wait_in_support",None])
async def exit_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id: 
            await second_state.reset_data()
            await bot.send_message(chat_id=user_id,
                                text="Пользователь завершил диалог")
    await call.message.edit_text("Вы завершили диалог")
    await state.reset_data()
