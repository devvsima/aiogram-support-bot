from aiogram import Dispatcher, executor
from database import *
from app import middlewares, filters, handlers
from loader import dp, bot


async def on_startup(_):
    print(" [On_startup] ")
    from utils.misc.set_bot_commands import set_defualt_commands
    await set_defualt_commands(dp=dp)

async def on_shutdown(dispatcher: Dispatcher):
    print("Shutting down...")


if __name__ == "__main__":
    executor.start_polling(     
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
    )
