# Backend Bot Engineer Report

## Objective

Реализовать каталог реализованных проектов и перевод пользователя из карточки проекта в существующий FSM заявки.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-004.md`
- `docs/autopilot/tasks/dossiers/AUTO-004/analyst.md`
- `docs/autopilot/tasks/dossiers/AUTO-004/lead.md`
- `app/handlers/menu.py`
- `app/handlers/project_configurator.py`
- `main.py`

## Decisions

- Данные каталога вынесены в `app/data/projects.py`.
- Inline-клавиатуры вынесены в `app/keyboards/projects_kb.py`.
- Обработчики каталога собраны в `app/handlers/projects.py`.
- Для конверсии в заявку используется существующий `ProjectFSM` с отдельным входом в шаг запроса имени.

## Work Performed

- Создан `app/data/projects.py` с dataclass `ProjectCatalogItem`, helper-функциями и 23 тестовыми проектами.
- Создан `app/keyboards/projects_kb.py` со списком проектов и карточкой проекта.
- Создан `app/handlers/projects.py`:
  - вход по кнопке `🏗 Реализованные проекты`;
  - callback `projects` для возврата к списку;
  - callback `project_<id>` для показа карточки;
  - callback `project_request_<id>` для конверсии в заявку.
- В `app/handlers/project_configurator.py` расширен существующий `ProjectFSM` состоянием `waiting_name`.
- Для сценария из каталога реализовано:
  - `state.clear()`;
  - `state.update_data(selected_project=project_id, request_source="project_catalog")`;
  - `state.set_state(ProjectFSM.waiting_name)`.
- В админское сообщение добавлена отдельная ветка для заявок из каталога с данными выбранного проекта.
- В `main.py` подключен `projects_router` до `menu_router`, чтобы каталог не перехватывался placeholder/fallback-логикой из `menu.py`.
- Выполнена локальная проверка:
  - `python -m py_compile app/data/projects.py`
  - `python -m py_compile app/keyboards/projects_kb.py`
  - `python -m py_compile app/handlers/projects.py`
  - `python -m py_compile app/handlers/project_configurator.py`
  - `python -m py_compile main.py`

## Self-Analysis

Решение сохраняет текущую архитектуру и не создаёт отдельную FSM для каталога. Гипотеза: использование пустых `photos=()` корректно покрывает требование обработки отсутствия фото, но ветка `media_group` останется непроверенной до появления валидных Telegram `file_id`.

## Risks

- Ручная проверка в Telegram всё ещё нужна для подтверждения UX и порядка сообщений.
- Для тестовых проектов не заведены реальные `file_id`, поэтому фактическая отправка `media_group` не проверялась.
- Ветка configurator по-прежнему начинает сбор контактов с телефона; шаг имени добавлен только как отдельная точка входа из каталога.

## Handoff

Передать в `QA` для ручной проверки сценариев каталога, карточки проекта, возврата к списку и перехода в заявку.
