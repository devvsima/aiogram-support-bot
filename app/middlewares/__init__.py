from aiogram import dispatcher
from loader import dp

from .support_middleware import SupportMiddleware

if __name__ == "middlewares":
    dp.middleware.setup(SupportMiddleware())
