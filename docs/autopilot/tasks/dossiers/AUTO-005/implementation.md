# Backend Bot Engineer Report

## Objective

Реализовать админ-панель управления проектами каталога с JSON-сохранением и изолированным FSM.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-005.md`
- `docs/autopilot/tasks/dossiers/AUTO-005/analyst.md`
- `docs/autopilot/tasks/dossiers/AUTO-005/lead.md`
- `app/data/projects.py`
- `main.py`

## Decisions

- Для минимального риска legacy-каталог оставлен в `app/data/projects.py` как seed-источник, а новые админские записи сохраняются в `data/projects.json`.
- Совместимость пользовательского каталога сохранена через прежние `get_projects()` и `get_project_by_id()`.
- Админский flow вынесен в отдельные `states`, `keyboards`, `handlers`.
- Доступ проверяется через `ADMIN_IDS`, а `ADMIN_ID` сохраняется как совместимый alias первого администратора.
- `Редактировать` и `Удалить` реализованы как явные заглушки с callback-кнопками.

## Work Performed

- Создан `data/projects.json` как файловое хранилище новых проектов.
- Обновлён `app/data/projects.py`:
  - добавлена загрузка и сохранение JSON;
  - добавлен `add_project(...)`;
  - `get_projects()` теперь возвращает legacy-проекты вместе с JSON-проектами;
  - `get_project_by_id()` сравнивает идентификаторы в нормализованном виде.
- Создан `app/states/admin_states.py` с FSM `AdminAddProject`.
- Создан `app/keyboards/admin_kb.py` с клавиатурами `admin_menu_kb()`, `project_type_kb()`, `confirm_kb()`, `done_photos_kb()` и inline-кнопками действий проекта.
- Создан `app/handlers/admin_projects.py`:
  - команда `/admin`;
  - админ-меню;
  - FSM добавления проекта;
  - приём нескольких фото с сохранением `file_id`;
  - подтверждение и сохранение в JSON;
  - админский список проектов;
  - заглушки редактирования и удаления.
- Обновлены `app/config.py` и `app/config/__init__.py` для `ADMIN_IDS`.
- Подключён `admin_projects_router` в `main.py` и `app/main.py`.
- Созданы task-first артефакты `AUTO-005`: card, dossier, board entry.
- Выполнены локальные проверки:
  - `python -m py_compile app/data/projects.py`
  - `python -m py_compile app/states/admin_states.py`
  - `python -m py_compile app/keyboards/admin_kb.py`
  - `python -m py_compile app/handlers/admin_projects.py`
  - `python -m py_compile main.py`
  - `python -m py_compile app/main.py`
  - импортный smoke-check: загрузка `router` и `get_projects()`

## Self-Analysis

- Решение осознанно не делает полную миграцию старого каталога в JSON, чтобы не рисковать регрессией уже работающего раздела. Это означает смешанный источник данных: legacy seed + admin JSON.
- Фото собираются сообщениями по одному, без отдельной album-агрегации. Для текущей задачи это достаточно, потому что сохраняется именно `file_id` каждого полученного изображения.
- Ветка редактирования и удаления намеренно остановлена на заглушках, чтобы не расширять scope без отдельной аналитики.

## Risks

- Нужна ручная Telegram-проверка реального UX пошаговой загрузки нескольких фото.
- Новые проекты получают числовые ID в JSON, а legacy-проекты сохраняют строковые ID; data-layer это нормализует, но список проектов в админке будет показывать смешанный формат идентификаторов.
- `app/main.py` в репозитории отличается по архитектуре от корневого `main.py`; router подключён в обоих местах для снижения риска запуска не той точки входа.

## Handoff

- Передать в `QA` для ручной проверки сценариев `/admin`, добавления проекта, подтверждения, повторного чтения из JSON и отсутствия регрессии пользовательского каталога.
