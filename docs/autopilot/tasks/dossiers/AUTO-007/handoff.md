# Handoff

- `from_role`: `Backend Bot Engineer`
- `to_role`: `QA`
- `current_status`: `ready_for_qa`
- `next_status`: `qa_review`

## What Was Done

- Создан `app/services/projects_service.py` как единый файловый CRUD-слой каталога.
- Удалены test seed-проекты и runtime-источник `PROJECTS` из `app/data/projects.py`.
- Переведены на service-layer `app/handlers/admin_projects.py`, `app/handlers/projects.py`, `app/handlers/project_configurator.py`, `app/keyboards/projects_kb.py`.
- Локально подтверждено удаление проекта через add/delete/reload проверку: удаленная запись не возвращается после повторной загрузки.

## What To Do Next

- Проверить каталог в Telegram UI:
  - список проектов для администратора;
  - удаление проекта через кнопки подтверждения;
  - повторную загрузку списка после удаления;
  - открытие карточки проекта пользователем;
  - переход из карточки проекта в заявку.
- Подтвердить отсутствие регрессии в add/edit/photo flows.

## Required Inputs

- `docs/autopilot/tasks/cards/AUTO-007.md`
- `docs/autopilot/tasks/dossiers/AUTO-007/analyst.md`
- `docs/autopilot/tasks/dossiers/AUTO-007/lead.md`
- `app/data/projects.py`
- `app/handlers/admin_projects.py`
- `app/handlers/projects.py`
- `app/handlers/project_configurator.py`
- `app/keyboards/projects_kb.py`
- `data/projects.json`

## Known Risks

- Не выполнен полный e2e прогон в Telegram.
- Нужна проверка UI-пути после удаления проекта из списка.

## Links

- `docs/autopilot/tasks/cards/AUTO-007.md`
- `docs/autopilot/tasks/dossiers/AUTO-007/INDEX.md`
