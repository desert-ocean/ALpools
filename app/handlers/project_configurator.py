from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.config import ADMIN_ID
from app.handlers.menu import BTN_DESIGN

router = Router()

# =========================
# НАСТРОЙКИ
# =========================

PROJECT_SECTIONS = {
    "technology": {"name": "Технология", "price": 120000, "option_percent": 15},
    "architecture": {"name": "Архитектура", "price": 90000, "option_percent": 10},
    "electric": {"name": "Электрика", "price": 80000, "option_percent": 12},
    "automation": {"name": "Автоматизация", "price": 70000, "option_percent": 15},
    "constructive": {"name": "Конструктив", "price": 100000, "option_percent": 8},
}

ATTRACTION_PRICE = 25000

TYPE_COEFFICIENT = {
    "private": 1.0,
    "public": 1.4
}

PLACEMENT_COEFFICIENT = {
    "indoor": 1.2,
    "outdoor": 1.0
}

# =========================
# FSM
# =========================

class ProjectFSM(StatesGroup):
    choosing_sections = State()
    choosing_type = State()
    choosing_placement = State()
    choosing_attractions = State()
    result = State()

# =========================
# СТАРТ КОНФИГУРАТОРА
# =========================

@router.message(F.text == BTN_DESIGN)
async def start_configurator(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ProjectFSM.choosing_sections)
    await state.update_data(sections=[], attractions=0)

    await message.answer(
        "📐 Выберите разделы проектирования:",
        reply_markup=sections_keyboard([])
    )

# =========================
# КНОПКИ РАЗДЕЛОВ
# =========================

def sections_keyboard(selected):
    buttons = []

    for key, section in PROJECT_SECTIONS.items():
        mark = "☑" if key in selected else "⬜"
        buttons.append([
            InlineKeyboardButton(
                text=f"{mark} {section['name']} ({section['price']:,} ₽)",
                callback_data=f"section_{key}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(text="➡ Продолжить", callback_data="sections_next")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(ProjectFSM.choosing_sections, F.data.startswith("section_"))
async def toggle_section(callback: CallbackQuery, state: FSMContext):
    key = callback.data.split("_")[1]
    data = await state.get_data()
    selected = data.get("sections", [])

    if key in selected:
        selected.remove(key)
    else:
        selected.append(key)

    await state.update_data(sections=selected)

    await callback.message.edit_reply_markup(
        reply_markup=sections_keyboard(selected)
    )

    await callback.answer()


@router.callback_query(ProjectFSM.choosing_sections, F.data == "sections_next")
async def choose_type(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if not data.get("sections"):
        await callback.answer("Выберите хотя бы один раздел", show_alert=True)
        return

    await state.set_state(ProjectFSM.choosing_type)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Частный", callback_data="type_private"),
            InlineKeyboardButton(text="Общественный", callback_data="type_public")
        ]
    ])

    await callback.message.answer("🏊 Выберите тип бассейна:", reply_markup=keyboard)
    await callback.answer()

# =========================
# ТИП БАССЕЙНА
# =========================

@router.callback_query(ProjectFSM.choosing_type, F.data.startswith("type_"))
async def choose_pool_type(callback: CallbackQuery, state: FSMContext):
    pool_type = callback.data.split("_")[1]
    await state.update_data(pool_type=pool_type)
    await state.set_state(ProjectFSM.choosing_placement)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Внутри здания", callback_data="place_indoor"),
            InlineKeyboardButton(text="Отдельно стоящий", callback_data="place_outdoor")
        ]
    ])

    await callback.message.answer("📍 Размещение бассейна:", reply_markup=keyboard)
    await callback.answer()

# =========================
# РАЗМЕЩЕНИЕ
# =========================

@router.callback_query(ProjectFSM.choosing_placement, F.data.startswith("place_"))
async def choose_placement(callback: CallbackQuery, state: FSMContext):
    placement = callback.data.split("_")[1]
    await state.update_data(placement=placement, attractions=0)
    await state.set_state(ProjectFSM.choosing_attractions)

    await callback.message.answer(
        "🎢 Выберите количество аттракционов (до 5):",
        reply_markup=attractions_keyboard(0)
    )
    await callback.answer()

# =========================
# АТТРАКЦИОНЫ
# =========================

def attractions_keyboard(current):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➖", callback_data="attr_minus"),
            InlineKeyboardButton(text=str(current), callback_data="noop"),
            InlineKeyboardButton(text="➕", callback_data="attr_plus")
        ],
        [
            InlineKeyboardButton(text="💰 Рассчитать", callback_data="calculate")
        ]
    ])


@router.callback_query(ProjectFSM.choosing_attractions, F.data.in_(["attr_plus", "attr_minus"]))
async def change_attractions(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data.get("attractions", 0)

    if callback.data == "attr_plus" and count < 5:
        count += 1
    elif callback.data == "attr_minus" and count > 0:
        count -= 1

    await state.update_data(attractions=count)

    await callback.message.edit_reply_markup(
        reply_markup=attractions_keyboard(count)
    )

    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery):
    await callback.answer()

# =========================
# РАСЧЁТ
# =========================

@router.callback_query(ProjectFSM.choosing_attractions, F.data == "calculate")
async def calculate_price(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    sections = data.get("sections", [])
    pool_type = data.get("pool_type")
    placement = data.get("placement")
    attractions = data.get("attractions", 0)

    breakdown = []
    total = 0

    breakdown.append("📐 <b>Выбранные разделы:</b>\n")

    for key in sections:
        section = PROJECT_SECTIONS[key]
        base = section["price"]
        percent = section["option_percent"]
        extra = base * percent / 100
        section_total = base + extra

        total += section_total

        breakdown.append(
            f"• <b>{section['name']}</b>\n"
            f"   Базовая: {base:,} ₽\n"
            f"   Доп. ({percent}%): {int(extra):,} ₽\n"
            f"   Итого: {int(section_total):,} ₽\n"
        )

    attractions_sum = attractions * ATTRACTION_PRICE
    total += attractions_sum

    if attractions > 0:
        breakdown.append(
            f"\n🎢 Аттракционы: {attractions} × {ATTRACTION_PRICE:,} ₽ = {attractions_sum:,} ₽"
        )

    type_coef = TYPE_COEFFICIENT.get(pool_type, 1)
    place_coef = PLACEMENT_COEFFICIENT.get(placement, 1)

    breakdown.append(f"\n🏊 Тип бассейна: x{type_coef}")
    breakdown.append(f"📍 Размещение: x{place_coef}")

    total = int(total * type_coef * place_coef)

    await state.update_data(total=total)
    await state.set_state(ProjectFSM.result)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📨 Отправить заявку", callback_data="send_request")]
    ])

    await callback.message.answer(
        "💰 <b>Предварительный расчёт стоимости проектирования</b>\n\n"
        + "\n".join(breakdown)
        + "\n\n━━━━━━━━━━━━━━━\n"
        + f"<b>ИТОГО: {total:,} ₽</b>\n\n"
        + "⚠ <i>Расчёт ориентировочный.</i>",
        reply_markup=keyboard
    )

    await callback.answer()

# =========================
# ОТПРАВКА ЗАЯВКИ
# =========================

@router.callback_query(ProjectFSM.result, F.data == "send_request")
async def send_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = callback.from_user

    sections_list = "\n".join(
        f"• {PROJECT_SECTIONS[s]['name']}" for s in data.get("sections", [])
    )

    admin_text = (
        "📥 <b>НОВАЯ ЗАЯВКА НА ПРОЕКТИРОВАНИЕ</b>\n\n"
        f"👤 Клиент: {user.full_name}\n"
        f"🆔 ID: {user.id}\n\n"
        f"📐 Разделы:\n{sections_list}\n\n"
        f"💰 Сумма: <b>{data.get('total', 0):,} ₽</b>"
    )

    await callback.bot.send_message(ADMIN_ID, admin_text)

    await callback.message.answer(
        "✅ Заявка отправлена.\nНаш специалист свяжется с вами."
    )

    await state.clear()
    await callback.answer()