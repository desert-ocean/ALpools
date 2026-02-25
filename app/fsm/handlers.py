from uuid import UUID

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.db.engine import AsyncSessionLocal
from app.enums.project_enums import ProjectStatus, ProjectStep
from app.fsm.states import ProjectCreation
from app.keyboards.project_kb import draft_resume_keyboard, review_keyboard
from app.services.project_service import ProjectService

router = Router()


def _build_review_text(project) -> str:
    return (
        "<b>Проверьте данные проекта</b>\n\n"
        "<b>Общая информация:</b>\n"
        f"ФИО: {project.full_name or '—'}\n"
        f"Телефон: {project.phone or '—'}\n"
        f"Email: {project.email or '—'}\n"
        f"Адрес: {project.address or '—'}\n\n"
        "<b>Геометрия:</b>\n"
        f"Длина: {project.length if project.length is not None else '—'}\n"
        f"Ширина: {project.width if project.width is not None else '—'}\n"
        f"Средняя глубина: {project.average_depth if project.average_depth is not None else '—'}"
    )


async def _show_review(message: Message, state: FSMContext, project_id: UUID) -> None:
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        project = await service.get_by_id(project_id)
        await service.set_step(project_id, ProjectStep.review)
    await state.set_state(ProjectCreation.review)
    await message.answer(_build_review_text(project), reply_markup=review_keyboard())


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    user_id = message.from_user.id
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        active_project = await service.get_active_project(user_id)

        if active_project is None:
            project = await service.create_draft(user_id)
            await state.update_data(project_id=str(project.id))
            await service.set_step(project.id, ProjectStep.general_info)
            await state.set_state(ProjectCreation.general_full_name)
            await message.answer("Введите ФИО:")
            return

    await state.update_data(project_id=str(active_project.id))
    await state.set_state(ProjectCreation.start)
    await message.answer(
        "У вас есть незавершенный проект. Что сделать?",
        reply_markup=draft_resume_keyboard(),
    )


@router.callback_query(F.data == "draft_continue")
async def draft_continue(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])

    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        project = await service.get_by_id(project_id)

    if project.current_step in {ProjectStep.start, ProjectStep.general_info}:
        if not project.full_name:
            await state.set_state(ProjectCreation.general_full_name)
            await callback.message.answer("Введите ФИО:")
        elif not project.phone:
            await state.set_state(ProjectCreation.general_phone)
            await callback.message.answer("Введите телефон:")
        elif not project.email:
            await state.set_state(ProjectCreation.general_email)
            await callback.message.answer("Введите email:")
        elif not project.address:
            await state.set_state(ProjectCreation.general_address)
            await callback.message.answer("Введите адрес:")
        else:
            async with AsyncSessionLocal() as session:
                await ProjectService(session).set_step(project_id, ProjectStep.geometry)
            await state.set_state(ProjectCreation.geometry_length)
            await callback.message.answer("Введите длину чаши (м):")
    elif project.current_step == ProjectStep.geometry:
        if project.length is None:
            await state.set_state(ProjectCreation.geometry_length)
            await callback.message.answer("Введите длину чаши (м):")
        elif project.width is None:
            await state.set_state(ProjectCreation.geometry_width)
            await callback.message.answer("Введите ширину чаши (м):")
        elif project.average_depth is None:
            await state.set_state(ProjectCreation.geometry_depth)
            await callback.message.answer("Введите среднюю глубину (м):")
        else:
            await _show_review(callback.message, state, project_id)
    else:
        await _show_review(callback.message, state, project_id)

    await callback.answer()


@router.callback_query(F.data == "draft_new")
async def draft_new(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.from_user is None:
        return

    data = await state.get_data()
    old_project_id = UUID(data["project_id"])

    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.set_status(old_project_id, ProjectStatus.cancelled)
        new_project = await service.create_draft(callback.from_user.id)
        await service.set_step(new_project.id, ProjectStep.general_info)

    await state.update_data(project_id=str(new_project.id))
    await state.set_state(ProjectCreation.general_full_name)
    await callback.message.answer("Создан новый проект.\nВведите ФИО:")
    await callback.answer()


@router.message(ProjectCreation.general_full_name)
async def general_full_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.update_field(project_id, "full_name", message.text)
        await service.set_step(project_id, ProjectStep.general_info)
    await state.set_state(ProjectCreation.general_phone)
    await message.answer("Введите телефон:")


@router.message(ProjectCreation.general_phone)
async def general_phone(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.update_field(project_id, "phone", message.text)
        await service.set_step(project_id, ProjectStep.general_info)
    await state.set_state(ProjectCreation.general_email)
    await message.answer("Введите email:")


@router.message(ProjectCreation.general_email)
async def general_email(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.update_field(project_id, "email", message.text)
        await service.set_step(project_id, ProjectStep.general_info)
    await state.set_state(ProjectCreation.general_address)
    await message.answer("Введите адрес:")


@router.message(ProjectCreation.general_address)
async def general_address(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.update_field(project_id, "address", message.text)
        await service.set_step(project_id, ProjectStep.geometry)
    await state.set_state(ProjectCreation.geometry_length)
    await message.answer("Введите длину чаши (м):")


@router.message(ProjectCreation.geometry_length)
async def geometry_length(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    length = float((message.text or "").replace(",", "."))
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.update_field(project_id, "length", length)
        await service.set_step(project_id, ProjectStep.geometry)
    await state.set_state(ProjectCreation.geometry_width)
    await message.answer("Введите ширину чаши (м):")


@router.message(ProjectCreation.geometry_width)
async def geometry_width(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    width = float((message.text or "").replace(",", "."))
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.update_field(project_id, "width", width)
        await service.set_step(project_id, ProjectStep.geometry)
    await state.set_state(ProjectCreation.geometry_depth)
    await message.answer("Введите среднюю глубину (м):")


@router.message(ProjectCreation.geometry_depth)
async def geometry_depth(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    depth = float((message.text or "").replace(",", "."))
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.update_field(project_id, "average_depth", depth)
    await _show_review(message, state, project_id)


@router.callback_query(F.data == "edit_general")
async def edit_general(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    async with AsyncSessionLocal() as session:
        await ProjectService(session).set_step(project_id, ProjectStep.general_info)
    await state.set_state(ProjectCreation.general_full_name)
    await callback.message.answer("Редактирование общей информации.\nВведите ФИО:")
    await callback.answer()


@router.callback_query(F.data == "edit_geometry")
async def edit_geometry(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    async with AsyncSessionLocal() as session:
        await ProjectService(session).set_step(project_id, ProjectStep.geometry)
    await state.set_state(ProjectCreation.geometry_length)
    await callback.message.answer("Редактирование геометрии.\nВведите длину чаши (м):")
    await callback.answer()


@router.callback_query(F.data == "confirm_project")
async def confirm_project(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    project_id = UUID(data["project_id"])
    async with AsyncSessionLocal() as session:
        service = ProjectService(session)
        await service.set_status(project_id, ProjectStatus.completed)
        await service.set_step(project_id, ProjectStep.completed)

    await state.clear()
    await callback.message.answer("Проект подтвержден и завершен ✅")
    await callback.answer()
