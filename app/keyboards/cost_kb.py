from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config.cost_steps import StepConfig

CB_PREFIX = "cost"
CB_SELECT = f"{CB_PREFIX}:select"
CB_NEXT = f"{CB_PREFIX}:next"
CB_CLEAR = f"{CB_PREFIX}:clear"
CB_BACK = f"{CB_PREFIX}:back"
CB_CANCEL = f"{CB_PREFIX}:cancel"
CB_ENGINEER = f"{CB_PREFIX}:engineer"

BTN_BACK = "⬅ Назад"
BTN_CANCEL = "❌ Отменить"
BTN_ENGINEER = "👨‍🔧 Консультация инженера"
BTN_DONE = "✔ Готово"
BTN_CLEAR = "🧹 Очистить"


def build_step_keyboard(step: StepConfig, selected: list[str] | None = None) -> InlineKeyboardMarkup | None:
    if not step.options:
        return _footer_keyboard(step)

    selected = selected or []
    rows: list[list[InlineKeyboardButton]] = []

    for option in step.options:
        checked = "✅ " if option.key in selected else ""
        rows.append([
            InlineKeyboardButton(
                text=f"{checked}{option.label}",
                callback_data=f"{CB_SELECT}:{option.key}",
            )
        ])

    if step.multi_select:
        rows.append([
            InlineKeyboardButton(text=BTN_DONE, callback_data=CB_NEXT),
            InlineKeyboardButton(text=BTN_CLEAR, callback_data=CB_CLEAR),
        ])

    rows.extend(_footer_rows(step))
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _footer_keyboard(step: StepConfig) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=_footer_rows(step))


def _footer_rows(step: StepConfig) -> list[list[InlineKeyboardButton]]:
    rows = [[InlineKeyboardButton(text=BTN_BACK, callback_data=CB_BACK), InlineKeyboardButton(text=BTN_CANCEL, callback_data=CB_CANCEL)]]
    if step.has_engineer_button:
        rows.append([InlineKeyboardButton(text=BTN_ENGINEER, callback_data=CB_ENGINEER)])
    return rows
