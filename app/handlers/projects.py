from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from app.data.projects import ProjectCatalogItem
from app.handlers.menu import BTN_PROJECTS
from app.handlers.project_configurator import ProjectFSM
from app.keyboards.projects_kb import keyboard_project_card, keyboard_projects_list
from app.services.projects_service import get_project_by_id

router = Router()


def _build_projects_list_text() -> str:
    return (
        "🏗 <b>Реализованные проекты</b>\n\n"
        "Выберите проект, чтобы посмотреть карточку и перейти в заявку."
    )


def _build_project_card_text(project: ProjectCatalogItem) -> str:
    return (
        f"🏊 <b>{project.title}</b>\n\n"
        f"📍 {project.city}\n"
        f"📐 {project.size}\n"
        f"💧 {project.type}\n\n"
        f"📝 {project.description}"
    )


async def _show_projects_list(message: Message) -> None:
    await message.answer(
        _build_projects_list_text(),
        reply_markup=keyboard_projects_list(),
    )


@router.message(F.text == BTN_PROJECTS)
async def realized_projects(message: Message) -> None:
    await _show_projects_list(message)


@router.callback_query(F.data == "projects")
async def projects_list_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        _build_projects_list_text(),
        reply_markup=keyboard_projects_list(),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("project_request_"))
async def project_request(callback: CallbackQuery, state: FSMContext) -> None:
    project_id = callback.data.removeprefix("project_request_")
    project = get_project_by_id(project_id)
    if project is None:
        await callback.answer("Проект не найден", show_alert=True)
        return

    await state.clear()
    await state.update_data(selected_project=project_id, request_source="project_catalog")
    await state.set_state(ProjectFSM.waiting_name)

    await callback.message.answer(
        f"💬 Заявка на проект:\n{project.title}\n\nВведите ваше имя:"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("project_"))
async def project_card(callback: CallbackQuery) -> None:
    project_id = callback.data.removeprefix("project_")
    project = get_project_by_id(project_id)
    if project is None:
        await callback.answer("Проект не найден", show_alert=True)
        return

    if project.photos:
        media = [InputMediaPhoto(media=file_id) for file_id in project.photos]
        await callback.message.answer_media_group(media)

    await callback.message.answer(
        _build_project_card_text(project),
        reply_markup=keyboard_project_card(project.id),
    )
    await callback.answer()
