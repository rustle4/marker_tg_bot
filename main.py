import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from src.marker_telegram_bot.bot.handlers.menu import router as menu_router
from src.marker_telegram_bot.core.config import settings

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def main() -> None:
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    dp = Dispatcher()

    dp.include_router(menu_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
