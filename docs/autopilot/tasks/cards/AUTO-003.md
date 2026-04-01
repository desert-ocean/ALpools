# AUTO-003

## Header

- `task_id`: `AUTO-003`
- `title`: `Замена квадратных маркеров на эмодзи в меню разделов проектирования`
- `area`: `product`
- `priority`: `medium`
- `status`: `ready_for_lead_gate`

## Summary

Улучшить UX меню выбора разделов проектирования: заменить квадратные визуальные маркеры на эмодзи разделов и сохранить индикатор выбранного состояния.

## Problem

Текущие кнопки разделов используют квадраты как основной визуальный маркер. Это хуже считывается пользователем и выглядит менее понятно, чем предметные эмодзи разделов.

## Scope

- Обновить только текст кнопок разделов в `sections_keyboard()` в `app/handlers/project_configurator.py`.
- Добавить явный mapping эмодзи для разделов.
- Сохранить индикатор выбранного состояния `☑`.

## Out Of Scope

- Изменение `callback_data`.
- Изменение FSM и handlers.
- Изменение кнопки `➡ Продолжить`.
- Изменение других клавиатур и меню деталей раздела.

## Inputs

- Пользовательский запрос в текущем треде.
- `AGENTS.md`.
- `docs/autopilot/sources-of-truth.md`.
- `AUTOPILOT-FOUNDATION.md`.
- `app/handlers/project_configurator.py`.

## Dependencies

- Текущее меню разделов в `app/handlers/project_configurator.py`.

## Definition Of Done

- Для `technology`, `architecture`, `electric`, `automation`, `constructive` отображаются заданные эмодзи.
- Для выбранных разделов формат равен `☑ EMOJI Раздел`.
- Для невыбранных разделов формат равен `EMOJI Раздел`.
- `callback_data="section:{key}"` не меняется.
- FSM и кнопка `➡ Продолжить` не меняются.

## Review Requirements

- Проверить формат текста кнопок в состояниях selected/unselected.
- Проверить неизменность `callback_data`.
- Проверить отсутствие побочных изменений в других кнопках.

## Main Artifact

- `app/handlers/project_configurator.py`

## Next Handoff

- `TeamLead` для финального gate.
