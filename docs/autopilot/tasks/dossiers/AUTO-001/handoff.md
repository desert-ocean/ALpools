# Handoff

- `from_role`: `QA`
- `to_role`: `TeamLead`
- `current_status`: `ready_for_lead_gate`
- `next_status`: `done`

## What Was Done

В FSM конфигуратора добавлен новый шаг про подводное освещение после выбора аттракционов. Значение `lighting` сохраняется в FSM и payload `design`, а при выборе `Да` в расчёт добавляется `10000 ₽`.

## What To Do Next

Проверить, что такой способ хранения `price` в `design` приемлем для текущего продукта, и закрыть задачу после lead gate.

## Required Inputs

- `docs/autopilot/tasks/cards/AUTO-001.md`
- `docs/autopilot/tasks/dossiers/AUTO-001/implementation.md`
- `docs/autopilot/tasks/dossiers/AUTO-001/qa.md`
- `app/handlers/project_configurator.py`

## Known Risks

- Live e2e сценарий не прогонялся.
- `design["price"]` сейчас хранит итоговую общую сумму, а не цену конкретного раздела.

## Links

- `docs/autopilot/tasks/cards/AUTO-001.md`
- `docs/autopilot/tasks/dossiers/AUTO-001/INDEX.md`
