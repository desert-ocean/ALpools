## Objective

Реализовать миграцию каталога проектов на единый JSON-источник через `app/services/projects_service.py` и убрать legacy seed-данные из Python-кода.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-007.md`
- `docs/autopilot/tasks/dossiers/AUTO-007/analyst.md`
- `docs/autopilot/tasks/dossiers/AUTO-007/lead.md`

## Decisions

- `app/data/projects.py` оставлен только как source of truth для dataclass `ProjectCatalogItem`, без seed-данных и файловой логики.
- Новый файловый CRUD-слой реализован в `app/services/projects_service.py`.
- Хендлеры и клавиатуры переведены на service-layer без изменения FSM и callback contract.
- Фото-операции в админке реализованы через общий `update_project(...)`, без дублирующих helper-функций.

## Work Performed

- Создан `app/services/projects_service.py` с функциями:
  - `load_projects()`
  - `save_projects(data)`
  - `get_all_projects()`
  - `get_project_by_id(id)`
  - `add_project(project)`
  - `delete_project(id)`
  - `update_project(id, data)`
- В сервисе добавлена защита от отсутствующего файла: `data/projects.json` создается автоматически.
- В сервисе добавлена защита от пустого содержимого и невалидного JSON/list shape: возвращается пустой каталог с нормализацией файла в `[]`.
- Удалены test seed-проекты и вся runtime-логика каталога из `app/data/projects.py`.
- Обновлены импорты и использование каталога в:
  - `app/handlers/admin_projects.py`
  - `app/handlers/projects.py`
  - `app/handlers/project_configurator.py`
  - `app/keyboards/projects_kb.py`
- Из админки убрана ветка `legacy/custom`; теперь все проекты считаются JSON-проектами из единого источника.
- Локальная проверка выполнена:
  - `python -m py_compile app/data/projects.py app/services/projects_service.py app/handlers/admin_projects.py app/handlers/projects.py app/handlers/project_configurator.py app/keyboards/projects_kb.py`
  - inline Python check: добавить временный проект -> удалить -> повторно загрузить каталог; результат `found_after_delete=False`

## Self-Analysis

- Полноценный e2e Telegram-flow не прогонялся; подтверждение основано на py_compile и прямой проверке service-layer.
- Текущий формат JSON сохранен совместимым с существующими данными; миграция не требует преобразования `data/projects.json`.

## Risks

- Если в проде есть внешние места, импортирующие старые helper-функции из `app/data/projects.py`, они сломаются; внутри `app/` таких ссылок больше не найдено.
- В файле `data/projects.json` остались существующие данные как есть; содержательная корректность самих значений не валидируется сверх обязательных полей.

## Handoff

Передать в `QA` на проверку user/admin flows каталога и регрессии удаления через UI.
