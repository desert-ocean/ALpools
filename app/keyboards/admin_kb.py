from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def admin_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить проект")],
            [KeyboardButton(text="Список проектов")],
            [KeyboardButton(text="Удалить проект")],
        ],
        resize_keyboard=True,
    )


def project_type_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Частный"), KeyboardButton(text="Общественный")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
    )


def confirm_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сохранить"), KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
    )


def done_photos_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Готово")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
    )


def project_actions_kb(project_id: str | int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Редактировать",
                    callback_data=f"edit_project_{project_id}",
                ),
                InlineKeyboardButton(
                    text="Удалить",
                    callback_data=f"delete_project_{project_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📢 Опубликовать заново",
                    callback_data=f"publish_project_{project_id}",
                )
            ],
        ]
    )


def edit_project_fields_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Название"), KeyboardButton(text="Город")],
            [KeyboardButton(text="Размер"), KeyboardButton(text="Тип")],
            [KeyboardButton(text="Описание"), KeyboardButton(text="Фото")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
    )


def photo_edit_actions_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Заменить фото")],
            [KeyboardButton(text="Добавить новые фото")],
            [KeyboardButton(text="Очистить фото")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True,
    )


def delete_confirmation_kb(project_id: str | int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да",
                    callback_data=f"confirm_delete_project_{project_id}",
                ),
                InlineKeyboardButton(
                    text="Отмена",
                    callback_data=f"cancel_delete_project_{project_id}",
                ),
            ]
        ]
    )
