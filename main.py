import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from app.bot.goals import router as goals_router
from app.bot.menu import router as menu_router
from app.core.config import settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def main() -> None:
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(menu_router)
    dp.include_router(goals_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
