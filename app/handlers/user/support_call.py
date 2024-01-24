from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from app.keyboards.inline.cancel import cancel_support
from app.keyboards.inline.support import (
    support_keyboard,
    support_callback,
    check_support_available,
    get_support_manager,
)


@dp.message_handler(Command("support_call"))
async def ask_support(message: types.Message):
    text = "Хотите написать сообщение техподдержке? Нажмите кнопку ниже!"
    keyboard = await support_keyboard(messages="many")
    if not keyboard:
        await message.answer("К сожалению, сейчас нет свободных операторов. Попробуйте позже.")
        return
    await message.answer(text, reply_markup=keyboard)



@dp.callback_query_handler(support_callback.filter(messages="many", as_user="yes"))
async def send_to_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text(
        "Вы обратились в техподдержку. Ждем ответа от оператора!"
    )
    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:support_id = user_id

    if not support_id:
        await call.message.edit_text(
            "К сожалению, сейчас все операторы заняты. Поробуйте позже"
        )
        await state.reset_state()
        return
    
    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    keyboard = await support_keyboard(messages="many", user_id=call.from_user.id)
    await bot.send_message(
        chat_id=support_id,
        text=f"С вами хочет связаться пользователь {call.from_user.full_name}",
        reply_markup=keyboard,
    )


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="no"))
async def answer_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != "wait_in_support":
        await call.message.edit_text("Пользователь уже недоступен")
        return
    await state.set_state("in_support")
    await user_state.set_state("in_support")

    await state.update_data(second_id=second_id)
    keyboard = cancel_support(user_id=second_id)
    keyboard_second_user = cancel_support(user_id=call.from_user.id)

    await call.message.edit_text(text="Вы создали диалог с пользователем!\nЧтобы завершить его нажмите на кнопкку",
                                 reply_markup=keyboard)
    await bot.send_message(chat_id=second_id,
                           text="Вас связало с оператором! Можете писать свое сообщение.\n Для завершения диалога нажмите на кнопку.",
                           reply_markup=keyboard_second_user)
    

@dp.message_handler(state="wait_in_support", content_types=types.ContentType.ANY)
async def not_supported(message: types.Message,state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")
    keyboard=cancel_support(second_id)

    await message.answer(text="Дождитесь ответа от опретора! Или нажмите на кнопк для завершения",
                         reply_markup=keyboard)