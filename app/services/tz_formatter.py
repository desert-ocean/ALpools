from typing import Any


FIELD_LABELS: dict[str, str] = {
    "dimensions": "Размеры бассейна",
    "private_or_public": "Частный/общественный",
    "project_need": "Что нужно",
    "indoor_outdoor": "Размещение",
    "equipment_location": "Расположение оборудования",
    "pool_type": "Тип бассейна",
    "embedded_material": "Материал чаши",
    "water_type": "Тип воды",
    "purpose": "Назначение",
    "finish": "Отделка",
    "heating": "Подогрев",
    "disinfection": "Дезинфекция",
    "extra_disinfection": "Доп. дезинфекция",
    "lighting": "Освещение",
    "music": "Музыка",
    "attractions": "Аттракционы",
    "cover": "Покрытие",
    "phone": "Телефон",
    "email": "Email",
    "volume": "Ориентировочный объём",
}


def format_tz_text(payload: dict[str, Any]) -> str:
    lines = ["📋 <b>Предварительные параметры бассейна</b>", ""]

    for key, value in payload.items():
        if value in (None, "", []):
            continue

        label = FIELD_LABELS.get(key, key)
        if isinstance(value, list):
            value_text = ", ".join(str(item) for item in value)
        elif key == "volume":
            value_text = f"{value} м³"
        else:
            value_text = str(value)

        lines.append(f"• <b>{label}:</b> {value_text}")

    return "\n".join(lines)
