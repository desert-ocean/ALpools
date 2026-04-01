# AUTO-001

## Header

- `task_id`: `AUTO-001`
- `title`: `Добавить шаг подводного освещения в FSM конфигуратора`
- `area`: `product`
- `priority`: `high`
- `status`: `ready_for_lead_gate`

## Summary

Добавить в конфигуратор проектирования бассейна новый шаг "Дополнительные уточнения" после выбора количества аттракционов с вопросом про подводное освещение.

## Problem

Текущий FSM после шага аттракционов сразу переходит к расчёту стоимости. В результате нельзя учесть дополнительный параметр `lighting` и наценку за подводное освещение без точечного расширения сценария.

## Scope

- Новое состояние FSM после шага аттракционов.
- Inline-клавиатура `Да / Нет / Пропустить`.
- Сохранение `lighting = True | False | None`.
- Учёт `+10000 ₽`, если освещение выбрано.
- Обновление структуры `design` полями `attractions_count`, `lighting`, `price`.

## Out Of Scope

- Полная переработка FSM конфигуратора.
- Изменение уже существующих шагов до аттракционов.
- Расширение коммерческой модели сверх одного фиксированного доп. параметра.

## Inputs

- пользовательский запрос в текущем треде;
- `AGENTS.md`;
- `docs/autopilot/sources-of-truth.md`;
- `AUTOPILOT-FOUNDATION.md`;
- `app/handlers/project_configurator.py`.

## Dependencies

- существующий FSM конфигуратора в `app/handlers/project_configurator.py`.

## Definition Of Done

- Новый шаг идёт строго после выбора аттракционов.
- Значение `lighting` сохраняется как `True | False | None`.
- При `lighting=True` в расчёт добавляется `10000 ₽`.
- Структура `design` содержит `attractions_count`, `lighting`, `price`.
- Существующие шаги конфигуратора не переписаны и не сломаны.

## Review Requirements

- Проверить переход `choosing_attractions -> choosing_lighting -> result`.
- Проверить ветки `Да`, `Нет`, `Пропустить`.
- Проверить, что расчёт суммы и сохранение в FSM согласованы.

## Main Artifact

- `app/handlers/project_configurator.py`

## Next Handoff

- `TeamLead` для gate после QA.
