from dataclasses import dataclass
from typing import Callable

from aiogram.fsm.state import State

from app.fsm.cost_estimate import CostEstimateFSM
from app.utils.validators import validate_dimensions, validate_email, validate_phone

Validator = Callable[[str], tuple[bool, str | None]]


@dataclass(frozen=True)
class Option:
    key: str
    label: str


@dataclass(frozen=True)
class StepConfig:
    key: str
    state: State
    text: str
    options: list[Option] | None = None
    multi_select: bool = False
    validator: Validator | None = None
    comment: str | None = None
    has_engineer_button: bool = True


STEPS: list[StepConfig] = [
    StepConfig(
        key="dimensions",
        state=CostEstimateFSM.dimensions,
        text="1/19. Укажите размеры чаши в формате <b>длина x ширина x глубина</b> (например, 10x4x1.6).",
        validator=validate_dimensions,
        comment="Можно использовать x, х или * как разделитель.",
    ),
    StepConfig(
        key="private_or_public",
        state=CostEstimateFSM.private_or_public,
        text="2/19. Объект частный или общественный?",
        options=[Option("private", "Частный"), Option("public", "Общественный")],
    ),
    StepConfig(
        key="project_need",
        state=CostEstimateFSM.project_need,
        text="3/19. Что требуется?",
        options=[Option("new", "Новый бассейн"), Option("reconstruction", "Реконструкция")],
    ),
    StepConfig(
        key="indoor_outdoor",
        state=CostEstimateFSM.indoor_outdoor,
        text="4/19. Где расположен бассейн?",
        options=[Option("indoor", "В помещении"), Option("outdoor", "На улице")],
    ),
    StepConfig(
        key="equipment_location",
        state=CostEstimateFSM.equipment_location,
        text="5/19. Где будет расположено оборудование?",
        options=[Option("plant_room", "Техпомещение"), Option("near_pool", "Рядом с чашей")],
    ),
    StepConfig(
        key="pool_type",
        state=CostEstimateFSM.pool_type,
        text="6/19. Выберите тип бассейна.",
        options=[Option("skimmer", "Скиммерный"), Option("overflow", "Переливной")],
    ),
    StepConfig(
        key="embedded_material",
        state=CostEstimateFSM.embedded_material,
        text="7/19. Какой материал чаши?",
        options=[Option("concrete", "Бетон"), Option("composite", "Композит"), Option("polypropylene", "Полипропилен")],
    ),
    StepConfig(
        key="water_type",
        state=CostEstimateFSM.water_type,
        text="8/19. Какая вода в бассейне?",
        options=[Option("fresh", "Пресная"), Option("salt", "Солевая")],
    ),
    StepConfig(
        key="purpose",
        state=CostEstimateFSM.purpose,
        text="9/19. Основное назначение бассейна?",
        options=[Option("family", "Семейный"), Option("sports", "Спортивный"), Option("spa", "SPA/релакс")],
    ),
    StepConfig(
        key="finish",
        state=CostEstimateFSM.finish,
        text="10/19. Выберите отделку чаши.",
        options=[Option("tile", "Плитка"), Option("mosaic", "Мозаика"), Option("liner", "Лайнер")],
    ),
    StepConfig(
        key="heating",
        state=CostEstimateFSM.heating,
        text="11/19. Нужен подогрев воды?",
        options=[Option("yes", "Да"), Option("no", "Нет")],
    ),
    StepConfig(
        key="disinfection",
        state=CostEstimateFSM.disinfection,
        text="12/19. Основной способ дезинфекции?",
        options=[Option("chlorine", "Хлор"), Option("electrolysis", "Электролиз"), Option("oxygen", "Активный кислород")],
    ),
    StepConfig(
        key="extra_disinfection",
        state=CostEstimateFSM.extra_disinfection,
        text="13/19. Выберите дополнительную дезинфекцию.",
        options=[Option("uv", "УФ"), Option("ozone", "Озон"), Option("none", "Не требуется")],
        multi_select=True,
    ),
    StepConfig(
        key="lighting",
        state=CostEstimateFSM.lighting,
        text="14/19. Нужна подсветка?",
        options=[Option("basic", "Базовая"), Option("rgb", "RGB"), Option("no", "Без подсветки")],
    ),
    StepConfig(
        key="music",
        state=CostEstimateFSM.music,
        text="15/19. Планируется музыкальная система?",
        options=[Option("yes", "Да"), Option("no", "Нет")],
    ),
    StepConfig(
        key="attractions",
        state=CostEstimateFSM.attractions,
        text="16/19. Выберите аттракционы.",
        options=[Option("counterflow", "Противоток"), Option("hydromassage", "Гидромассаж"), Option("waterfall", "Водопад")],
        multi_select=True,
    ),
    StepConfig(
        key="cover",
        state=CostEstimateFSM.cover,
        text="17/19. Нужно покрытие бассейна?",
        options=[Option("roller", "Роллетное"), Option("bubble", "Пузырьковое"), Option("no", "Не требуется")],
    ),
    StepConfig(
        key="phone",
        state=CostEstimateFSM.phone,
        text="18/19. Укажите телефон для связи.",
        validator=validate_phone,
    ),
    StepConfig(
        key="email",
        state=CostEstimateFSM.email,
        text="19/19. Укажите email для отправки результата.",
        validator=validate_email,
    ),
]

STEP_BY_KEY = {step.key: step for step in STEPS}
