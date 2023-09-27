from aiogram import types, Dispatcher
from loader import dp, bot
from database.supporters import supporters_list

@dp.message_handler(user_id=supporters_list(), commands="admin")
async def comm_start(message: types.Message):
    await message.answer(
        text=f"Вы админ"
    )
