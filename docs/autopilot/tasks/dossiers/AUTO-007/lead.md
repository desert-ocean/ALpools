## Objective

Разрешить coherent implementation slice по миграции каталога проектов на единый JSON-источник без изменения FSM и без расширения scope.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-007.md`
- `docs/autopilot/tasks/dossiers/AUTO-007/analyst.md`
- `app/data/projects.py`
- `app/handlers/admin_projects.py`
- `app/handlers/projects.py`
- `app/handlers/project_configurator.py`
- `app/keyboards/projects_kb.py`

## Decisions

- Разрешить write scope файлами `app/data/projects.py`, `app/services/projects_service.py`, `app/handlers/admin_projects.py`, `app/handlers/projects.py`, `app/handlers/project_configurator.py`, `app/keyboards/projects_kb.py`, `data/projects.json` и artifacts `AUTO-007`.
- Не менять FSM, callback contract и пользовательский flow.
- Не добавлять дублирующий data access в handlers.

## Work Performed

- Подтвержден целевой способ реализации через единый service-layer.
- Зафиксированы ограничения по scope и регрессионным рискам.

## Self-Analysis

- Архитектурное решение минимально инвазивно и не требует отдельного `Architect` gate, так как меняется локальный файловый слой без изменения межмодульных контрактов выше service boundary.

## Risks

- Неполная замена импортов оставит старое поведение в одной из точек каталога.

## Handoff

Передать в `Backend Bot Engineer` на реализацию и локальную проверку.
