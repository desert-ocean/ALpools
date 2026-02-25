from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def draft_resume_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Продолжить", callback_data="draft_continue")],
            [InlineKeyboardButton(text="Создать новый", callback_data="draft_new")],
        ]
    )


def review_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✏ Редактировать общую информацию", callback_data="edit_general")],
            [InlineKeyboardButton(text="📐 Редактировать геометрию", callback_data="edit_geometry")],
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_project")],
        ]
    )
