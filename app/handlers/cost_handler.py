import logging
from typing import Any

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import ADMIN_ID
from app.config.cost_steps import STEPS, StepConfig
from app.handlers.menu import BTN_INDIVIDUAL_CALC
from app.keyboards.cost_kb import (
    CB_BACK,
    CB_CANCEL,
    CB_CLEAR,
    CB_ENGINEER,
    CB_NEXT,
    CB_PREFIX,
    CB_SELECT,
    build_step_keyboard,
)
from app.services.cost_service import build_cost_payload
from app.services.tz_formatter import format_tz_text

router = Router()
logger = logging.getLogger(__name__)

COST_STATES = [step.state for step in STEPS]


@router.message(F.text == BTN_INDIVIDUAL_CALC)
async def start_cost_estimator(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(STEPS[0].state)
    await state.update_data(current_step_index=0, answers={})

    logger.info("Cost configurator started by user_id=%s", message.from_user.id if message.from_user else "unknown")
    await _show_step(message, STEPS[0], state)


@router.message(StateFilter(*COST_STATES), F.text)
async def process_text_step(message: Message, state: FSMContext) -> None:
    idx, answers = await _load_progress(state)
    step = STEPS[idx]

    if step.options:
        await message.answer("Пожалуйста, используйте кнопки для выбора варианта.")
        return

    value = message.text.strip()

    if step.validator:
        is_valid, error = step.validator(value)
        if not is_valid:
            logger.warning("Validation error for step=%s user_id=%s", step.key, message.from_user.id if message.from_user else "unknown")
            await message.answer(error or "Некорректное значение. Попробуйте еще раз.")
            return

    answers[step.key] = value
    await state.update_data(answers=answers)
    await _go_next(message, state, idx)


@router.callback_query(StateFilter(*COST_STATES), F.data.startswith(f"{CB_PREFIX}:"))
async def process_step_callback(callback: CallbackQuery, state: FSMContext) -> None:
    if not callback.data or not callback.message:
        await callback.answer()
        return

    idx, answers = await _load_progress(state)
    step = STEPS[idx]
    data = callback.data

    if data == CB_CANCEL:
        await state.clear()
        await callback.message.answer("Конфигуратор отменен. Вы можете начать заново из меню.")
        await callback.answer()
        return

    if data == CB_BACK:
        if idx == 0:
            await callback.answer("Это первый шаг.")
            return
        prev_idx = idx - 1
        await state.update_data(current_step_index=prev_idx)
        await state.set_state(STEPS[prev_idx].state)
        await _show_step(callback.message, STEPS[prev_idx], state)
        await callback.answer()
        return

    if data == CB_ENGINEER:
        user = callback.from_user
        logger.info("Engineer consultation requested in configurator by user_id=%s", user.id)
        await callback.message.answer("Запрос отправлен. Инженер свяжется с вами в ближайшее время.")
        username = f"@{user.username}" if user.username else "не указан"
        await callback.bot.send_message(
            ADMIN_ID,
            (
                "👨‍🔧 Запрос консультации инженера из конфигуратора\n"
                f"ID: {user.id}\n"
                f"Имя: {user.full_name}\n"
                f"Username: {username}"
            ),
        )
        await callback.answer()
        return

    if data == CB_CLEAR and step.multi_select:
        answers[step.key] = []
        await state.update_data(answers=answers)
        await callback.message.edit_reply_markup(reply_markup=build_step_keyboard(step, []))
        await callback.answer("Выбор очищен")
        return

    if data.startswith(f"{CB_SELECT}:") and step.options:
        selected_key = data.split(":")[-1]
        if step.multi_select:
            selected = list(answers.get(step.key, []))
            if selected_key in selected:
                selected.remove(selected_key)
            else:
                selected.append(selected_key)
            answers[step.key] = selected
            await state.update_data(answers=answers)
            await callback.message.edit_reply_markup(reply_markup=build_step_keyboard(step, selected))
            await callback.answer()
            return

        answers[step.key] = selected_key
        await state.update_data(answers=answers)
        await callback.answer()
        await _go_next(callback.message, state, idx)
        return

    if data == CB_NEXT and step.multi_select:
        if not answers.get(step.key):
            await callback.answer("Выберите хотя бы один вариант.", show_alert=True)
            return
        await callback.answer()
        await _go_next(callback.message, state, idx)
        return

    await callback.answer()


async def _go_next(message: Message, state: FSMContext, idx: int) -> None:
    next_idx = idx + 1
    if next_idx >= len(STEPS):
        data = await state.get_data()
        answers = data.get("answers", {})
        human_answers = _humanize_answers(answers)
        payload = build_cost_payload(human_answers)
        text = format_tz_text(payload)

        logger.info("Cost configurator completed user_id=%s", message.from_user.id if message.from_user else "unknown")
        await message.answer(text)
        await state.clear()
        return

    await state.update_data(current_step_index=next_idx)
    await state.set_state(STEPS[next_idx].state)
    await _show_step(message, STEPS[next_idx], state)


async def _show_step(message: Message, step: StepConfig, state: FSMContext) -> None:
    data = await state.get_data()
    answers: dict[str, Any] = data.get("answers", {})
    selected = answers.get(step.key, []) if step.multi_select else []

    text = step.text
    if step.comment:
        text = f"{step.text}\n\n💬 {step.comment}"

    await message.answer(text, reply_markup=build_step_keyboard(step, selected))


async def _load_progress(state: FSMContext) -> tuple[int, dict[str, Any]]:
    data = await state.get_data()
    idx = int(data.get("current_step_index", 0))
    answers: dict[str, Any] = data.get("answers", {})
    return idx, answers


def _humanize_answers(answers: dict[str, Any]) -> dict[str, Any]:
    step_map = {step.key: step for step in STEPS}
    output: dict[str, Any] = {}

    for key, value in answers.items():
        step = step_map.get(key)
        if not step or not step.options:
            output[key] = value
            continue

        option_map = {option.key: option.label for option in step.options}
        if step.multi_select:
            output[key] = [option_map.get(item, item) for item in value]
        else:
            output[key] = option_map.get(value, value)

    return output
