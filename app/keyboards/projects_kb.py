from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.data.projects import get_projects


def keyboard_projects_list() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"🏊 {project.title}",
                callback_data=f"project_{project.id}",
            )
        ]
        for project in get_projects()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def keyboard_project_card(project_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Хочу такой же проект",
                    callback_data=f"project_request_{project_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅ Назад к списку",
                    callback_data="projects",
                )
            ],
        ]
    )
