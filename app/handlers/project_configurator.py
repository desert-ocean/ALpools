from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from app.config import ADMIN_ID
from app.handlers.menu import BTN_DESIGN
from app.services.projects_service import get_project_by_id

router = Router()

# =====================================================
# НАСТРОЙКИ ПРОЕКТА
# =====================================================

PROJECT_SECTIONS = {
    "technology": {
        "name": "Технология",
        "price": 120_000,
        "option_percent": 15,
        "description": (
            "Раздел для водоподготовки, размещения оборудования, трубопроводов "
            "и подключения бассейна к инженерным сетям."
        ),
        "note": "",
        "base_sheets": [
            "Титульный лист",
            "Пояснительная записка",
            "Планы и разрезы с размещением закладных деталей системы водоподготовки бассейна",
            "Планы и разрезы с размещением проемов под закладные детали системы водоподготовки бассейна",
            "План размещения оборудования системы водоподготовки и аттракционов в техническом помещении бассейна",
            "План монтажа трубопроводов системы водоподготовки и аттракционов",
            "Принципиальная схема системы водоподготовки бассейна и аттракционов",
            "Аксонометрическая схема системы водоподготовки бассейна и аттракционов",
            "Строительное задание на подключение бассейна к инженерным сетям здания",
            "Спецификация оборудования",
        ],
        "optional_sheets": [
            "Визуализация бассейна и технического помещения",
            "Дополнительные планы проемов под закладные детали",
        ],
    },
    "architecture": {
        "name": "Архитектура",
        "price": 90_000,
        "option_percent": 10,
        "description": (
            "Раздел для гидроизоляции, облицовки, узлов и архитектурных листов "
            "по бассейну."
        ),
        "note": "Без финишной отделки, ее подбирает заказчик.",
        "base_sheets": [
            "Титульный лист",
            "Технологическая карта гидроизоляции и облицовки",
            "Общий план размещения бассейна",
            "Планы и разрезы с размещением закладных деталей",
            "Планы и разрезы с размещением проемов",
            "Раскладка плитки + ведомость",
            "Узлы стен, дна, переливного желоба",
            "Спецификация материалов",
        ],
        "optional_sheets": [
            "Узлы установки закладных деталей",
        ],
    },
    "electric": {
        "name": "Электрика",
        "price": 80_000,
        "option_percent": 12,
        "description": (
            "Раздел для расчета нагрузок, кабельных трасс, схем "
            "и спецификации по электроснабжению."
        ),
        "note": "",
        "base_sheets": [
            "Титульный лист",
            "Общие данные",
            "Расчет нагрузок",
            "Однолинейная схема",
            "План оборудования и кабельных трасс",
            "План кабельных лотков",
            "Кабельный журнал",
            "Схема уравнивания потенциалов",
            "Спецификация",
        ],
        "optional_sheets": [
            "Принципиальная схема шкафа",
        ],
    },
    "automation": {
        "name": "Автоматизация",
        "price": 70_000,
        "option_percent": 15,
        "description": (
            "Раздел для структурной схемы автоматизации, соединений, "
            "кабельных трасс и спецификации."
        ),
        "note": "",
        "base_sheets": [
            "Титульный лист",
            "Общие данные",
            "Структурная схема автоматизации",
            "Схема соединений",
            "План кабельных трасс",
            "План кабельных лотков",
            "Спецификация",
        ],
        "optional_sheets": [
            "Принципиальная схема шкафа",
            "Компоновка шкафа",
        ],
    },
    "constructive": {
        "name": "Конструктив",
        "price": 100_000,
        "option_percent": 8,
        "description": (
            "Раздел для чертежей чаши, армирования, разрезов и "
            "конструктивных узлов."
        ),
        "note": "Состав зависит от типа размещения бассейна.",
        "base_sheets": [
            "Титульный лист",
            "Общие данные",
            "План чаши",
            "Разрезы и узлы",
            "Планы армирования",
            "Разрезы с армированием",
            "Спецификация материалов",
        ],
        "optional_sheets": [],
    },
}

OPTIONAL_SHEET_PRICE = 20_000
ATTRACTION_PRICE = 18_000
LIGHTING_PRICE = 10_000


def _format_price(value: int) -> str:
    return f"{value:,}".replace(",", " ")


# =====================================================
# FSM
# =====================================================

class ProjectFSM(StatesGroup):
    choosing_sections = State()
    section_action = State()
    section_details = State()
    choosing_type = State()
    choosing_placement = State()
    choosing_attractions = State()
    choosing_lighting = State()
    result = State()
    waiting_name = State()
    waiting_phone = State()
    waiting_email = State()


# =====================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =====================================================

SECTION_LIST_TEXT = "📐 <b>Выберите разделы проектирования:</b>"
SECTION_EMOJIS = {
    "technology": "⚙️",
    "architecture": "🏗",
    "electric": "⚡",
    "automation": "🤖",
    "constructive": "🧱",
}


def _get_selected_section_keys(designs: dict[str, dict]) -> list[str]:
    return list(designs.keys())


def _build_design_payload(
    section_key: str,
    mode: str,
    selected_options: list[str] | None = None,
    attractions_count: int = 0,
    lighting: bool | None = None,
    price: int = 0,
) -> dict:
    return {
        "section": section_key,
        "mode": mode,
        "selected_options": list(selected_options or []),
        "attractions_count": attractions_count,
        "lighting": lighting,
        "price": price,
    }


def calculate_price(state_data: dict) -> tuple[int, list[str]]:
    designs = state_data.get("designs", {})
    sections = state_data.get("sections", [])
    pool_type = state_data.get("pool_type")
    placement = state_data.get("placement")
    attractions = state_data.get("attractions", 0)
    lighting = state_data.get("lighting")

    total = 0
    breakdown = ["📐 <b>Выбранные разделы:</b>", ""]

    for key in sections:
        section = PROJECT_SECTIONS[key]
        design = designs.get(key, {})
        base_price = section["price"]
        selected_options = design.get("selected_options", [])
        public_surcharge = int(base_price * 0.8) if key == "technology" and pool_type == "public" else 0
        outdoor_surcharge = int(base_price * 0.6) if key == "constructive" and placement == "outdoor" else 0
        optional_sheets_surcharge = len(selected_options) * OPTIONAL_SHEET_PRICE
        section_total = (
            base_price
            + public_surcharge
            + outdoor_surcharge
            + optional_sheets_surcharge
        )
        total += section_total

        mode = "быстрый выбор" if design.get("mode") == "fast" else "подробный выбор"
        selected_options_label = ", ".join(selected_options) if selected_options else "нет"

        breakdown.extend(
            [
                f"<b>{section['name']}</b>",
                f"Режим: {mode}",
                f"Состав: базовый комплект",
                f"Дополнительные листы: {selected_options_label}",
                f"Базовая: {_format_price(base_price)} ₽",
            ]
        )

        if public_surcharge:
            breakdown.append(
                "Доплата за общественный бассейн: "
                f"{_format_price(base_price)} × 0.8 = {_format_price(public_surcharge)} ₽"
            )

        if outdoor_surcharge:
            breakdown.append(
                "Доплата за отдельно стоящий бассейн: "
                f"{_format_price(base_price)} × 0.6 = {_format_price(outdoor_surcharge)} ₽"
            )

        if optional_sheets_surcharge:
            breakdown.append(
                "Доплата за дополнительные листы: "
                f"{len(selected_options)} × {_format_price(OPTIONAL_SHEET_PRICE)} = "
                f"{_format_price(optional_sheets_surcharge)} ₽"
            )

        breakdown.extend([
            f"Итого: {_format_price(section_total)} ₽",
            "",
        ])

    attractions_sum = attractions * ATTRACTION_PRICE
    if attractions:
        total += attractions_sum
        breakdown.extend(
            [
                "🎢 <b>Аттракционы:</b>",
                f"{attractions} × {_format_price(ATTRACTION_PRICE)} = {_format_price(attractions_sum)} ₽",
                "",
            ]
        )

    if lighting is True:
        total += LIGHTING_PRICE
        breakdown.extend(
            [
                "💡 <b>Подводное освещение:</b>",
                f"{_format_price(LIGHTING_PRICE)} ₽",
                "",
            ]
        )
    elif lighting is False:
        breakdown.extend([
            "💡 <b>Подводное освещение:</b>",
            "не выбрано",
            "",
        ])
    else:
        breakdown.extend([
            "💡 <b>Подводное освещение:</b>",
            "пропущено",
            "",
        ])

    return total, breakdown


def _render_preliminary_calculation_text(total: int, breakdown: list[str]) -> str:
    return (
        "💰 <b>Предварительный расчёт</b>\n\n"
        + "\n".join(breakdown).rstrip()
        + f"\n\n💵 <b>ИТОГО: {_format_price(total)} ₽</b>\n\n"
        + "⚠ <i>Расчёт ориентировочный.</i>"
    )


def _render_section_action_text(section_key: str) -> str:
    section = PROJECT_SECTIONS[section_key]
    parts = [
        f"📋 <b>{section['name']}</b>",
        "",
        section["description"],
    ]

    if section["note"]:
        parts.extend(["", f"ℹ️ <i>{section['note']}</i>"])

    return "\n".join(parts)


def _render_section_details_text(section_key: str, selected_options: list[str]) -> str:
    section = PROJECT_SECTIONS[section_key]
    parts = [f"📑 <b>{section['name']}: состав проекта</b>"]

    if section["note"]:
        parts.extend(["", f"ℹ️ <i>{section['note']}</i>"])

    parts.extend(["", "<b>Базовые листы (всегда включены):</b>"])
    parts.extend(f"• {sheet}" for sheet in section["base_sheets"])

    parts.extend(["", "<b>Опциональные листы:</b>"])
    if section["optional_sheets"]:
        for option in section["optional_sheets"]:
            mark = "[x]" if option in selected_options else "[ ]"
            parts.append(f"{mark} {option}")
    else:
        parts.append("Нет, доступен только базовый комплект.")

    return "\n".join(parts)


def _format_design_summary(section_key: str, designs: dict[str, dict]) -> str:
    design = designs.get(section_key, {})
    mode = design.get("mode", "fast")
    mode_label = "быстрый выбор" if mode == "fast" else "подробный выбор"
    options = design.get("selected_options", [])
    options_label = ", ".join(options) if options else "базовый комплект"
    return f"{PROJECT_SECTIONS[section_key]['name']} ({mode_label}) — {options_label}"


def _build_catalog_request_text(project_title: str) -> str:
    return (
        "📥 <b>НОВАЯ ЗАЯВКА ПО КАТАЛОГУ</b>\n\n"
        f"🏊 Проект: <b>{project_title}</b>"
    )


# =====================================================
# КЛАВИАТУРЫ
# =====================================================

def sections_keyboard(selected: list[str]) -> InlineKeyboardMarkup:
    buttons = []

    for key, section in PROJECT_SECTIONS.items():
        emoji = SECTION_EMOJIS[key]
        text_prefix = f"☑ {emoji}" if key in selected else emoji
        buttons.append([
            InlineKeyboardButton(
                text=f"{text_prefix} {section['name']} ({section['price']:,} ₽)",
                callback_data=f"section:{key}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="➡ Продолжить", callback_data="sections:next")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def section_action_keyboard(section_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подробнее", callback_data=f"section_details:{section_key}")],
        [InlineKeyboardButton(text="Выбрать сразу", callback_data=f"section_fast:{section_key}")],
        [InlineKeyboardButton(text="Пропустить", callback_data=f"section_skip:{section_key}")],
    ])


def section_details_keyboard(section_key: str, selected_options: list[str]) -> InlineKeyboardMarkup:
    buttons = []

    for index, option in enumerate(PROJECT_SECTIONS[section_key]["optional_sheets"]):
        mark = "☑" if option in selected_options else "⬜"
        buttons.append([
            InlineKeyboardButton(
                text=f"{mark} {option}",
                callback_data=f"section_option:{section_key}:{index}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="Готово", callback_data=f"section_done:{section_key}")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def attractions_keyboard(current: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data="attr:minus"),
            InlineKeyboardButton(text=str(current), callback_data="attr:noop"),
            InlineKeyboardButton(text="➕", callback_data="attr:plus"),
        ],
        [
            InlineKeyboardButton(text="💰 Рассчитать", callback_data="attr:calculate")
        ],
    ])


# =====================================================
# СТАРТ
# =====================================================

def lighting_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="lighting:yes"),
            InlineKeyboardButton(text="Нет", callback_data="lighting:no"),
        ],
        [
            InlineKeyboardButton(text="Пропустить", callback_data="lighting:skip"),
        ],
    ])


@router.message(F.text == BTN_DESIGN)
async def start_configurator(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ProjectFSM.choosing_sections)
    await state.update_data(
        sections=[],
        designs={},
        current_section=None,
        attractions=0,
        lighting=None,
    )

    await message.answer(
        SECTION_LIST_TEXT,
        reply_markup=sections_keyboard([]),
    )


# =====================================================
# ВЫБОР РАЗДЕЛОВ
# =====================================================

@router.callback_query(ProjectFSM.choosing_sections, F.data.startswith("section:"))
async def open_section_action(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":", maxsplit=1)[1]

    await state.update_data(current_section=key)
    await state.set_state(ProjectFSM.section_action)

    await callback.message.edit_text(
        _render_section_action_text(key),
        reply_markup=section_action_keyboard(key),
    )

    await callback.answer()


@router.callback_query(ProjectFSM.section_action, F.data.startswith("section_fast:"))
async def choose_section_fast(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    designs = dict(data.get("designs", {}))

    designs[key] = _build_design_payload(key, mode="fast")
    selected = _get_selected_section_keys(designs)

    await state.update_data(designs=designs, sections=selected, current_section=None)
    await state.set_state(ProjectFSM.choosing_sections)

    await callback.message.edit_text(
        SECTION_LIST_TEXT,
        reply_markup=sections_keyboard(selected),
    )

    await callback.answer("Сохранён базовый комплект")


@router.callback_query(ProjectFSM.section_action, F.data.startswith("section_skip:"))
async def skip_section(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    designs = dict(data.get("designs", {}))
    designs.pop(key, None)
    selected = _get_selected_section_keys(designs)

    await state.update_data(designs=designs, sections=selected, current_section=None)
    await state.set_state(ProjectFSM.choosing_sections)

    await callback.message.edit_text(
        SECTION_LIST_TEXT,
        reply_markup=sections_keyboard(selected),
    )

    await callback.answer("Раздел пропущен")


@router.callback_query(ProjectFSM.section_action, F.data.startswith("section_details:"))
async def open_section_details(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    designs = dict(data.get("designs", {}))
    selected_options = list(designs.get(key, {}).get("selected_options", []))

    await state.update_data(current_section=key)
    await state.set_state(ProjectFSM.section_details)

    await callback.message.edit_text(
        _render_section_details_text(key, selected_options),
        reply_markup=section_details_keyboard(key, selected_options),
    )

    await callback.answer()


@router.callback_query(ProjectFSM.section_details, F.data.startswith("section_option:"))
async def toggle_section_option(callback: CallbackQuery, state: FSMContext):
    _, section_key, option_index_raw = callback.data.split(":")
    option_index = int(option_index_raw)
    option_name = PROJECT_SECTIONS[section_key]["optional_sheets"][option_index]

    data = await state.get_data()
    designs = dict(data.get("designs", {}))
    selected_options = list(designs.get(section_key, {}).get("selected_options", []))

    if option_name in selected_options:
        selected_options.remove(option_name)
    else:
        selected_options.append(option_name)

    designs[section_key] = _build_design_payload(
        section_key,
        mode="detailed",
        selected_options=selected_options,
    )
    await state.update_data(designs=designs, current_section=section_key)

    await callback.message.edit_text(
        _render_section_details_text(section_key, selected_options),
        reply_markup=section_details_keyboard(section_key, selected_options),
    )

    await callback.answer()


@router.callback_query(ProjectFSM.section_details, F.data.startswith("section_done:"))
async def save_section_details(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    designs = dict(data.get("designs", {}))
    existing_options = list(designs.get(key, {}).get("selected_options", []))

    designs[key] = _build_design_payload(
        key,
        mode="detailed",
        selected_options=existing_options,
    )
    selected = _get_selected_section_keys(designs)

    await state.update_data(designs=designs, sections=selected, current_section=None)
    await state.set_state(ProjectFSM.choosing_sections)

    await callback.message.edit_text(
        SECTION_LIST_TEXT,
        reply_markup=sections_keyboard(selected),
    )

    await callback.answer("Состав раздела сохранён")


@router.callback_query(ProjectFSM.choosing_sections, F.data == "sections:next")
async def go_to_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if not data.get("sections"):
        await callback.answer("Выберите хотя бы один раздел", show_alert=True)
        return

    await state.set_state(ProjectFSM.choosing_type)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Частный", callback_data="type:private"),
            InlineKeyboardButton(text="Общественный", callback_data="type:public"),
        ]
    ])

    await callback.message.answer(
        "🏊 <b>Выберите тип бассейна:</b>",
        reply_markup=keyboard,
    )

    await callback.answer()


# =====================================================
# ТИП БАССЕЙНА
# =====================================================

@router.callback_query(ProjectFSM.choosing_type, F.data.startswith("type:"))
async def choose_pool_type(callback: CallbackQuery, state: FSMContext):
    pool_type = callback.data.split(":", maxsplit=1)[1]

    await state.update_data(pool_type=pool_type)
    await state.set_state(ProjectFSM.choosing_placement)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Внутри здания", callback_data="place:indoor"),
            InlineKeyboardButton(text="Отдельно стоящий", callback_data="place:outdoor"),
        ]
    ])

    await callback.message.answer(
        "📍 <b>Размещение бассейна:</b>",
        reply_markup=keyboard,
    )

    await callback.answer()


# =====================================================
# РАЗМЕЩЕНИЕ
# =====================================================

@router.callback_query(ProjectFSM.choosing_placement, F.data.startswith("place:"))
async def choose_placement(callback: CallbackQuery, state: FSMContext):
    placement = callback.data.split(":", maxsplit=1)[1]

    await state.update_data(placement=placement, attractions=0, lighting=None)
    await state.set_state(ProjectFSM.choosing_attractions)

    await callback.message.answer(
        "🎢 <b>Выберите количество аттракционов (до 5):</b>",
        reply_markup=attractions_keyboard(0),
    )

    await callback.answer()


# =====================================================
# АТТРАКЦИОНЫ
# =====================================================

@router.callback_query(ProjectFSM.choosing_attractions, F.data.startswith("attr:"))
async def manage_attractions(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":", maxsplit=1)[1]
    data = await state.get_data()
    count = data.get("attractions", 0)

    if action == "plus" and count < 5:
        count += 1
    elif action == "minus" and count > 0:
        count -= 1
    elif action == "calculate":
        await state.update_data(attractions=count)
        await state.set_state(ProjectFSM.choosing_lighting)
        await callback.message.answer(
            "💡 <b>Дополнительные уточнения</b>\n\n"
            "Необходимо ли подводное освещение бассейна?",
            reply_markup=lighting_keyboard(),
        )
        await callback.answer()
        return

    await state.update_data(attractions=count)

    await callback.message.edit_reply_markup(
        reply_markup=attractions_keyboard(count)
    )

    await callback.answer()


# =====================================================
# РАСЧЕТ
# =====================================================

@router.callback_query(ProjectFSM.choosing_lighting, F.data.startswith("lighting:"))
async def choose_lighting(callback: CallbackQuery, state: FSMContext):
    action = callback.data.split(":", maxsplit=1)[1]
    lighting_map = {
        "yes": True,
        "no": False,
        "skip": None,
    }
    lighting = lighting_map[action]

    data = await state.get_data()
    designs = dict(data.get("designs", {}))
    attractions = data.get("attractions", 0)

    for section_key, design in designs.items():
        updated_design = dict(design)
        updated_design["attractions_count"] = attractions
        updated_design["lighting"] = lighting
        designs[section_key] = updated_design

    await state.update_data(designs=designs, lighting=lighting)
    await calculate_price_result(callback, state)


async def calculate_price_result(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    total, breakdown = calculate_price(data)
    designs = dict(data.get("designs", {}))

    for section_key, design in designs.items():
        updated_design = dict(design)
        updated_design["price"] = total
        designs[section_key] = updated_design

    await state.update_data(designs=designs, total=total)
    await state.set_state(ProjectFSM.result)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить заявку", callback_data="send")]
    ])

    await callback.message.answer(
        _render_preliminary_calculation_text(total, breakdown),
        reply_markup=keyboard,
    )

    await callback.answer()


# =====================================================
# ЗАПРОС КОНТАКТОВ
# =====================================================

@router.callback_query(ProjectFSM.result, F.data == "send")
async def request_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProjectFSM.waiting_phone)

    await callback.message.answer(
        "📱 <b>Введите ваш номер телефона:</b>\n"
        "Например: +7 999 123 45 67"
    )

    await callback.answer()


@router.message(ProjectFSM.waiting_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text.strip())
    await state.set_state(ProjectFSM.waiting_phone)

    await message.answer(
        "📱 <b>Введите ваш номер телефона:</b>\n"
        "Например: +7 999 123 45 67"
    )


@router.message(ProjectFSM.waiting_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await state.set_state(ProjectFSM.waiting_email)

    await message.answer(
        "📧 <b>Введите email (или напишите - если не хотите указывать):</b>"
    )


@router.message(ProjectFSM.waiting_email)
async def process_email(message: Message, state: FSMContext):
    email = message.text.strip()
    if email == "-":
        email = "Не указан"

    await state.update_data(email=email)
    data = await state.get_data()

    user = message.from_user
    project = get_project_by_id(data.get("selected_project", ""))
    client_name = data.get("client_name") or user.full_name
    designs = data.get("designs", {})
    if project is not None and data.get("request_source") == "project_catalog":
        admin_text = (
            _build_catalog_request_text(project.title)
            + "\n\n"
            + f"👤 {client_name}\n"
            + f"🆔 {user.id}\n"
            + f"📱 {data.get('phone')}\n"
            + f"📧 {data.get('email')}\n"
            + f"📍 Город проекта: {project.city}\n"
            + f"📐 Размер: {project.size}\n"
            + f"💧 Тип: {project.type}"
        )
    else:
        sections_list = "\n".join(
            f"• {_format_design_summary(section_key, designs)}"
            for section_key in data.get("sections", [])
        )

        admin_text = (
            "📥 <b>НОВАЯ ЗАЯВКА</b>\n\n"
            f"👤 {client_name}\n"
            f"🆔 {user.id}\n"
            f"📱 {data.get('phone')}\n"
            f"📧 {data.get('email')}\n\n"
            f"📐 Разделы:\n{sections_list}\n\n"
            f"💰 Сумма: <b>{data.get('total', 0):,} ₽</b>"
        )

    await message.bot.send_message(ADMIN_ID, admin_text)

    await message.answer(
        "✅ Заявка отправлена.\nНаш специалист свяжется с вами."
    )

    await state.clear()
