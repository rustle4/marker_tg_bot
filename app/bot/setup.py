from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand, MenuButtonWebApp, WebAppInfo

from app.bot.handlers import router
from app.bot.middleware import DbSessionMiddleware
from app.core.config import settings


async def build_bot() -> tuple[Bot, Dispatcher]:
    if not settings.TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN is not configured")

    bot = Bot(settings.TELEGRAM_TOKEN, default=DefaultBotProperties)
    dp = Dispatcher()
    dp.message.middleware(DbSessionMiddleware())
    dp.callback_query.middleware(DbSessionMiddleware())
    dp.include_router(router)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Main menu"),
            BotCommand(command="goal", description="Add a goal"),
            BotCommand(command="goals", description="List of goals"),
        ]
    )

    if settings.WEB_APP_URL:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="Marker Bot", web_app=WebAppInfo(url=settings.WEB_APP_URL)
            )
        )
        return bot, dp
