from aiogram import types

async def set_defualt_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("support", "Написать сообщение в техподдержку"),
        types.BotCommand("support_call", "Связаться с техподдержкой"),
        types.BotCommand("help", "Помощь"),


    ])