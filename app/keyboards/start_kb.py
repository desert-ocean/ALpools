from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_welcome_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📞 Получить консультацию",
                    callback_data="go_consult",
                )
            ]
        ]
    )
