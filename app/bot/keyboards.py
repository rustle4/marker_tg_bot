from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


def main_menu(web_app_url: str | None) -> InlineKeyboardMarkup:
    rows = []
    if web_app_url:
        rows.append(
            [
                InlineKeyboardButton(
                    text="Open Marker", web_app=WebAppInfo(url=web_app_url)
                )
            ]
        )
    rows.extend([[InlineKeyboardButton(text="Goals", callback_data="show:goals")]])

    return InlineKeyboardMarkup(inline_keyboard=rows)


def goal_keyboard(goal_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Done", callback_data=f"goal:done:{goal_id}")]
        ]
    )
