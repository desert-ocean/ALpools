import logging
from html import escape

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message, ReplyKeyboardRemove

from app.config import ADMIN_IDS, CHANNEL_ID
from app.keyboards.admin_kb import (
    admin_menu_kb,
    confirm_kb,
    delete_confirmation_kb,
    done_photos_kb,
    edit_project_fields_kb,
    photo_edit_actions_kb,
    project_actions_kb,
    project_type_kb,
)
from app.services.projects_service import (
    add_project,
    delete_project,
    get_all_projects,
    get_project_by_id,
    update_project,
)
from app.states.admin_states import AdminAddProject, AdminEditProject

router = Router()
logger = logging.getLogger(__name__)

BTN_ADD_PROJECT = "Добавить проект"
BTN_LIST_PROJECTS = "Список проектов"
BTN_DELETE_PROJECT = "Удалить проект"
BTN_CANCEL = "Отмена"
BTN_DONE = "Готово"
BTN_SAVE = "Сохранить"
BTN_TITLE = "Название"
BTN_CITY = "Город"
BTN_SIZE = "Размер"
BTN_TYPE = "Тип"
BTN_DESCRIPTION = "Описание"
BTN_PHOTOS = "Фото"
BTN_REPLACE_PHOTOS = "Заменить фото"
BTN_ADD_NEW_PHOTOS = "Добавить новые фото"
BTN_CLEAR_PHOTOS = "Очистить фото"

PROJECT_TYPES = {"Частный", "Общественный"}
EDITABLE_FIELDS = {
    BTN_TITLE: ("title", AdminEditProject.waiting_title, "Введите новое название проекта"),
    BTN_CITY: ("city", AdminEditProject.waiting_city, "Введите новый город"),
    BTN_SIZE: ("size", AdminEditProject.waiting_size, "Введите новый размер"),
    BTN_TYPE: ("type", AdminEditProject.waiting_type, "Выберите новый тип бассейна"),
    BTN_DESCRIPTION: ("description", AdminEditProject.waiting_description, "Введите новое описание проекта"),
}
PHOTO_ACTIONS = {
    BTN_REPLACE_PHOTOS: "replace",
    BTN_ADD_NEW_PHOTOS: "append",
}


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


async def _deny_message(message: Message) -> None:
    await message.answer("Доступ запрещён.")


async def _deny_callback(callback: CallbackQuery) -> None:
    await callback.answer("Доступ запрещён.", show_alert=True)


def _is_blank(value: str | None) -> bool:
    return not value or not value.strip()


def _build_confirmation_text(data: dict) -> str:
    return (
        "<b>Проверьте проект перед сохранением</b>\n\n"
        f"<b>Название:</b> {escape(data['title'])}\n"
        f"<b>Город:</b> {escape(data['city'])}\n"
        f"<b>Размер:</b> {escape(data['size'])}\n"
        f"<b>Тип:</b> {escape(data['type'])}\n"
        f"<b>Описание:</b> {escape(data['description'])}\n"
        f"<b>Фото:</b> {len(data.get('photos', []))} шт."
    )


def _build_project_admin_text(project_id: str | int) -> str:
    project = get_project_by_id(project_id)
    if project is None:
        return "Проект не найден."

    return (
        f"<b>{escape(project.title)}</b>\n"
        f"ID: <code>{project.id}</code>\n"
        "Источник: JSON\n"
        f"Город: {escape(project.city)}\n"
        f"Размер: {escape(project.size)}\n"
        f"Тип: {escape(project.type)}\n"
        f"Фото: {len(project.photos)} шт."
    )


def _build_publish_text(project_id: str | int) -> str:
    project = get_project_by_id(project_id)
    if project is None:
        return "Проект не найден."

    return (
        f"🏊 <b>{escape(project.title)}</b>\n\n"
        f"📍 {escape(project.city)}\n"
        f"📐 {escape(project.size)}\n"
        f"💧 {escape(project.type)}\n\n"
        f"📝 {escape(project.description)}"
    )


def _extract_project_id(callback_data: str, prefixes: tuple[str, ...]) -> str:
    for prefix in prefixes:
        if callback_data.startswith(prefix):
            return callback_data.removeprefix(prefix)
    return ""


async def _show_admin_menu(message: Message, text: str = "Админ-панель проектов") -> None:
    await message.answer(text, reply_markup=admin_menu_kb())


async def _show_projects_list(message: Message) -> None:
    projects = get_all_projects()
    if not projects:
        await message.answer("Каталог проектов пуст.", reply_markup=admin_menu_kb())
        return

    await message.answer(f"Всего проектов: {len(projects)}", reply_markup=admin_menu_kb())
    for project in projects:
        await message.answer(
            _build_project_admin_text(project.id),
            reply_markup=project_actions_kb(project.id),
        )


async def _show_edit_menu(message: Message, project_id: str | int, text: str) -> None:
    await message.answer(
        f"{text}\n\n{_build_project_admin_text(project_id)}",
        reply_markup=edit_project_fields_kb(),
    )


async def _publish_project(message: Message, project_id: str | int) -> str:
    project = get_project_by_id(project_id)
    if project is None:
        return "Проект не найден."

    if CHANNEL_ID is None:
        return "Публикация пропущена: `CHANNEL_ID` не задан."

    text = _build_publish_text(project_id)
    try:
        if project.photos:
            media = [
                InputMediaPhoto(
                    media=project.photos[0],
                    caption=text,
                    parse_mode="HTML",
                )
            ]
            media.extend(InputMediaPhoto(media=file_id) for file_id in project.photos[1:])
            await message.bot.send_media_group(chat_id=CHANNEL_ID, media=media)
        else:
            await message.bot.send_message(chat_id=CHANNEL_ID, text=text)
    except Exception as exc:
        logger.exception("Не удалось опубликовать проект %s в канал", project_id)
        return f"Публикация не выполнена: {exc.__class__.__name__}."

    return "Проект опубликован в канал."


async def _save_text_field(
    message: Message,
    state: FSMContext,
    field_name: str,
    value: str,
    success_text: str,
) -> None:
    data = await state.get_data()
    project_id = data["edit_project_id"]
    project = update_project(project_id, {field_name: value})
    if project is None:
        await state.clear()
        await _show_admin_menu(message, "Проект не найден или недоступен для редактирования.")
        return

    await state.set_state(AdminEditProject.choosing_field)
    await _show_edit_menu(message, project.id, success_text)


@router.message(Command("admin"))
async def open_admin_panel(message: Message, state: FSMContext) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await _deny_message(message)
        return

    await state.clear()
    await _show_admin_menu(message)


@router.message(F.text == BTN_ADD_PROJECT)
async def start_add_project(message: Message, state: FSMContext) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await _deny_message(message)
        return

    await state.clear()
    await state.update_data(photos=[])
    await state.set_state(AdminAddProject.waiting_title)
    await message.answer("Введите название проекта", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == BTN_LIST_PROJECTS)
async def show_projects_list(message: Message) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await _deny_message(message)
        return

    await _show_projects_list(message)


@router.message(F.text == BTN_DELETE_PROJECT)
async def delete_project_stub(message: Message) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await _deny_message(message)
        return

    await message.answer("Удаление доступно через кнопку «Удалить» в списке проектов.", reply_markup=admin_menu_kb())


@router.callback_query(
    F.data.startswith("edit_project_") | F.data.startswith("admin_project_edit:")
)
async def start_edit_project(callback: CallbackQuery, state: FSMContext) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny_callback(callback)
        return

    project_id = _extract_project_id(callback.data, ("edit_project_", "admin_project_edit:"))
    project = get_project_by_id(project_id)
    if project is None:
        await callback.answer("Проект не найден.", show_alert=True)
        return

    await state.clear()
    await state.update_data(edit_project_id=str(project_id), edit_photos=[], photo_mode=None)
    await state.set_state(AdminEditProject.choosing_field)
    await callback.message.answer(
        f"Что изменить?\n\n{_build_project_admin_text(project_id)}",
        reply_markup=edit_project_fields_kb(),
    )
    await callback.answer()


@router.callback_query(
    F.data.startswith("delete_project_") | F.data.startswith("admin_project_delete:")
)
async def delete_project_request(callback: CallbackQuery) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny_callback(callback)
        return

    project_id = _extract_project_id(callback.data, ("delete_project_", "admin_project_delete:"))
    project = get_project_by_id(project_id)
    if project is None:
        await callback.answer("Проект не найден.", show_alert=True)
        return

    await callback.message.answer(
        f'Удалить проект "{escape(project.title)}"?',
        reply_markup=delete_confirmation_kb(project.id),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_delete_project_"))
async def confirm_delete_project(callback: CallbackQuery) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny_callback(callback)
        return

    project_id = callback.data.removeprefix("confirm_delete_project_")
    project = delete_project(project_id)
    if project is None:
        await callback.answer("Проект не найден.", show_alert=True)
        return

    await callback.answer("Проект удалён.")
    await callback.message.answer(
        f'Проект "<b>{escape(project.title)}</b>" удалён.',
        reply_markup=admin_menu_kb(),
    )
    await _show_projects_list(callback.message)


@router.callback_query(F.data.startswith("cancel_delete_project_"))
async def cancel_delete_project(callback: CallbackQuery) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny_callback(callback)
        return

    await callback.answer("Удаление отменено.")
    await callback.message.answer("Удаление отменено.", reply_markup=admin_menu_kb())


@router.callback_query(F.data.startswith("publish_project_"))
async def publish_project(callback: CallbackQuery) -> None:
    if not callback.from_user or not _is_admin(callback.from_user.id):
        await _deny_callback(callback)
        return

    project_id = callback.data.removeprefix("publish_project_")
    result_text = await _publish_project(callback.message, project_id)
    await callback.message.answer(result_text, reply_markup=admin_menu_kb())
    await callback.answer()


@router.message(F.text == BTN_CANCEL)
async def cancel_admin_flow(message: Message, state: FSMContext) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await _deny_message(message)
        return

    await state.clear()
    await _show_admin_menu(message, "Действие отменено.")


@router.message(AdminAddProject.waiting_title)
async def process_project_title(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Название не может быть пустым. Введите название проекта.")
        return

    await state.update_data(title=message.text.strip())
    await state.set_state(AdminAddProject.waiting_city)
    await message.answer("Введите город")


@router.message(AdminAddProject.waiting_city)
async def process_project_city(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Город не может быть пустым. Введите город.")
        return

    await state.update_data(city=message.text.strip())
    await state.set_state(AdminAddProject.waiting_size)
    await message.answer("Введите размер (например 8x4 или 8 4 1.5)")


@router.message(AdminAddProject.waiting_size)
async def process_project_size(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Размер не может быть пустым. Введите размер.")
        return

    await state.update_data(size=message.text.strip())
    await state.set_state(AdminAddProject.waiting_type)
    await message.answer("Выберите тип бассейна", reply_markup=project_type_kb())


@router.message(AdminAddProject.waiting_type)
async def process_project_type(message: Message, state: FSMContext) -> None:
    if message.text not in PROJECT_TYPES:
        await message.answer("Используйте кнопки выбора типа бассейна.", reply_markup=project_type_kb())
        return

    await state.update_data(type=message.text)
    await state.set_state(AdminAddProject.waiting_description)
    await message.answer("Введите описание проекта", reply_markup=ReplyKeyboardRemove())


@router.message(AdminAddProject.waiting_description)
async def process_project_description(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Описание не может быть пустым. Введите описание проекта.")
        return

    await state.update_data(description=message.text.strip(), photos=[])
    await state.set_state(AdminAddProject.waiting_photos)
    await message.answer(
        "Загрузите фото проекта. Можно отправить несколько изображений по одному. Если фото нет, нажмите «Готово».",
        reply_markup=done_photos_kb(),
    )


@router.message(AdminAddProject.waiting_photos, F.photo)
async def process_project_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photos = list(data.get("photos", []))
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    await message.answer(f"Фото сохранено. Сейчас загружено: {len(photos)}")


@router.message(AdminAddProject.waiting_photos, F.text == BTN_DONE)
async def finish_project_photos(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await state.set_state(AdminAddProject.waiting_confirmation)
    await message.answer(_build_confirmation_text(data), reply_markup=confirm_kb())


@router.message(AdminAddProject.waiting_photos)
async def ignore_non_photo_input(message: Message) -> None:
    await message.answer("На этом шаге отправьте фото или нажмите «Готово».")


@router.message(AdminAddProject.waiting_confirmation, F.text == BTN_SAVE)
async def save_project(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project = add_project(
        {
            "title": data["title"],
            "city": data["city"],
            "size": data["size"],
            "type": data["type"],
            "description": data["description"],
            "photos": list(data.get("photos", [])),
        }
    )
    publish_result = await _publish_project(message, project.id)

    await state.clear()
    await message.answer(
        (
            f"Проект сохранён.\n"
            f"ID: <code>{project.id}</code>\n"
            f"Название: <b>{escape(project.title)}</b>\n\n"
            f"{publish_result}"
        ),
        reply_markup=admin_menu_kb(),
    )


@router.message(AdminAddProject.waiting_confirmation)
async def confirm_project_with_buttons(message: Message) -> None:
    await message.answer("Используйте кнопки «Сохранить» или «Отмена».", reply_markup=confirm_kb())


@router.message(AdminEditProject.choosing_field)
async def choose_edit_field(message: Message, state: FSMContext) -> None:
    if message.text == BTN_PHOTOS:
        await state.set_state(AdminEditProject.waiting_photo_action)
        await message.answer("Выберите действие с фотографиями.", reply_markup=photo_edit_actions_kb())
        return

    field_config = EDITABLE_FIELDS.get(message.text or "")
    if field_config is None:
        await message.answer("Используйте кнопки выбора поля.", reply_markup=edit_project_fields_kb())
        return

    _, next_state, prompt = field_config
    await state.set_state(next_state)
    if next_state == AdminEditProject.waiting_type:
        await message.answer(prompt, reply_markup=project_type_kb())
    else:
        await message.answer(prompt, reply_markup=ReplyKeyboardRemove())


@router.message(AdminEditProject.waiting_title)
async def edit_project_title(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Название не может быть пустым. Введите новое название проекта.")
        return

    await _save_text_field(message, state, "title", message.text.strip(), "Название обновлено. Что изменить дальше?")


@router.message(AdminEditProject.waiting_city)
async def edit_project_city(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Город не может быть пустым. Введите новый город.")
        return

    await _save_text_field(message, state, "city", message.text.strip(), "Город обновлён. Что изменить дальше?")


@router.message(AdminEditProject.waiting_size)
async def edit_project_size(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Размер не может быть пустым. Введите новый размер.")
        return

    await _save_text_field(message, state, "size", message.text.strip(), "Размер обновлён. Что изменить дальше?")


@router.message(AdminEditProject.waiting_type)
async def edit_project_type(message: Message, state: FSMContext) -> None:
    if message.text not in PROJECT_TYPES:
        await message.answer("Используйте кнопки выбора типа бассейна.", reply_markup=project_type_kb())
        return

    await _save_text_field(message, state, "type", message.text, "Тип обновлён. Что изменить дальше?")


@router.message(AdminEditProject.waiting_description)
async def edit_project_description(message: Message, state: FSMContext) -> None:
    if _is_blank(message.text):
        await message.answer("Описание не может быть пустым. Введите новое описание проекта.")
        return

    await _save_text_field(
        message,
        state,
        "description",
        message.text.strip(),
        "Описание обновлено. Что изменить дальше?",
    )


@router.message(AdminEditProject.waiting_photo_action)
async def edit_project_photos_action(message: Message, state: FSMContext) -> None:
    if message.text == BTN_CLEAR_PHOTOS:
        data = await state.get_data()
        project = update_project(data["edit_project_id"], {"photos": []})
        if project is None:
            await state.clear()
            await _show_admin_menu(message, "Проект не найден или недоступен для редактирования.")
            return

        await state.set_state(AdminEditProject.choosing_field)
        await _show_edit_menu(message, project.id, "Фото очищены. Что изменить дальше?")
        return

    action = PHOTO_ACTIONS.get(message.text or "")
    if action is None:
        await message.answer("Используйте кнопки выбора действия.", reply_markup=photo_edit_actions_kb())
        return

    await state.update_data(photo_mode=action, edit_photos=[])
    await state.set_state(AdminEditProject.waiting_photos)
    await message.answer(
        "Отправьте фотографии по одной. Когда закончите, нажмите «Готово».",
        reply_markup=done_photos_kb(),
    )


@router.message(AdminEditProject.waiting_photos, F.photo)
async def process_edit_project_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photos = list(data.get("edit_photos", []))
    photos.append(message.photo[-1].file_id)
    await state.update_data(edit_photos=photos)
    await message.answer(f"Фото сохранено. Сейчас загружено: {len(photos)}")


@router.message(AdminEditProject.waiting_photos, F.text == BTN_DONE)
async def finish_edit_project_photos(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    photos = list(data.get("edit_photos", []))
    if not photos:
        await message.answer("Сначала загрузите хотя бы одно фото.")
        return

    project_id = data["edit_project_id"]
    if data.get("photo_mode") == "replace":
        project = update_project(project_id, {"photos": photos})
        success_text = "Фото заменены. Что изменить дальше?"
    else:
        current_project = get_project_by_id(project_id)
        if current_project is None:
            project = None
        else:
            project = update_project(project_id, {"photos": list(current_project.photos) + photos})
        success_text = "Новые фото добавлены. Что изменить дальше?"

    if project is None:
        await state.clear()
        await _show_admin_menu(message, "Проект не найден или недоступен для редактирования.")
        return

    await state.update_data(edit_photos=[], photo_mode=None)
    await state.set_state(AdminEditProject.choosing_field)
    await _show_edit_menu(message, project.id, success_text)


@router.message(AdminEditProject.waiting_photos)
async def ignore_non_photo_edit_input(message: Message) -> None:
    await message.answer("На этом шаге отправьте фото или нажмите «Готово».")
