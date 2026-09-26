import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.marker_telegram_bot.core.config import settings

TOKEN = getenv("TELEGRAM_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Greetings, {message.from_user.full_name}! This is Marker Bot!"
    )


async def main() -> None:
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
