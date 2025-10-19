import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import load_config
from app.db import create_tables
from app.handlers.common import common_router
from app.handlers.quiz import quiz_router

logging.basicConfig(level=logging.INFO)

async def main():
    config = load_config()
    bot = Bot(token=config.api_token)
    dp = Dispatcher()

    # Роутеры
    dp.include_router(common_router)
    dp.include_router(quiz_router)

    # Инициализация БД
    await create_tables()

    await dp.start_polling(bot)

if __name__ == "__main__":
    # Windows-фикс на всякий
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass
    asyncio.run(main())
