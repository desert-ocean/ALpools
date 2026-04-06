## Objective

Определить безопасный scope миграции каталога проектов с гибридного источника на единый JSON-источник без изменения FSM и без поломки админки.

## Inputs

- Пользовательский запрос в текущем треде.
- `AGENTS.md`
- `docs/autopilot/sources-of-truth.md`
- `AUTOPILOT-FOUNDATION.md`
- `app/data/projects.py`
- `app/handlers/admin_projects.py`
- `app/handlers/projects.py`
- `app/handlers/project_configurator.py`
- `app/keyboards/projects_kb.py`
- `data/projects.json`

## Decisions

- Источником истины для каталога должен стать только `data/projects.json`.
- Test seed-проекты из `app/data/projects.py` выводятся из эксплуатации и больше не участвуют в get/list/delete flows.
- Файловая логика выносится в отдельный service-layer `app/services/projects_service.py`.
- FSM и пользовательские сценарии не меняются; меняется только data access layer.

## Work Performed

- Выявлен root cause: `get_projects()` склеивает `PROJECTS + JSON`, а админка удаляет только записи, проходящие `is_custom_project()`.
- Найдены все точки использования каталога в handlers и keyboards.
- Сформулирован DoD для миграции на единый JSON-источник.

## Self-Analysis

- Не проверялись реальные прод-данные за пределами локального `data/projects.json`.
- Принято допущение, что существующий JSON-формат уже является целевым контрактом каталога.

## Risks

- Возможна регрессия в импортируемых функциях, если оставить старые имена без совместимости.
- Если в JSON окажутся данные вне текущего формата, сервис будет отфильтровывать некорректные записи.

## Handoff

Передать задачу `Backend Bot Engineer` для реализации service-layer, замены импортов и локальной проверки удаления проекта из JSON.
