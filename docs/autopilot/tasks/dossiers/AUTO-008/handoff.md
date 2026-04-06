# Handoff

- `from_role`: `QA`
- `to_role`: `TeamLead`
- `current_status`: `ready_for_lead_gate`
- `next_status`: `done`

## What Was Done

Рабочий пункт главного меню переименован в `Виртуальный конфигуратор`, старый одноимённый пункт-заглушка удалён из меню и из `app/handlers/menu.py`. Связанный `cost_handler` сохранён без изменения логики и продолжает запускаться через ту же импортируемую константу.

## What To Do Next

Проверить, что артефакты dossier полны, а решение действительно ограничилось минимальным срезом без затрагивания FSM и бизнес-логики.

## Required Inputs

- `docs/autopilot/tasks/cards/AUTO-008.md`
- `docs/autopilot/tasks/dossiers/AUTO-008/implementation.md`
- `docs/autopilot/tasks/dossiers/AUTO-008/qa.md`
- `app/handlers/menu.py`
- `app/handlers/cost_handler.py`

## Known Risks

- Runtime-проверка в Telegram-клиенте не выполнялась.
- Исторические упоминания `конфигуратор` в старых dossier и технических логах сохранены.

## Links

- `docs/autopilot/tasks/cards/AUTO-008.md`
- `docs/autopilot/tasks/dossiers/AUTO-008/INDEX.md`
- `app/handlers/menu.py`
- `app/handlers/cost_handler.py`
