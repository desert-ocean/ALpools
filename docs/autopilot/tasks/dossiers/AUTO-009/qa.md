## Objective

Проверить, что новый `/start` в рабочем menu-router отправляет точный welcome-текст с фото и `MediaGroup`, не ломает существующий consultation flow и сохраняет доступ к разделам бота.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-009.md`
- `docs/autopilot/tasks/dossiers/AUTO-009/implementation.md`
- `main.py`
- `app/handlers/menu.py`
- `app/data/welcome_media.py`
- `app/keyboards/start_kb.py`

## Decisions

- Для этой задачи достаточно локальной QA-проверки через код-ревью, поиск по маршрутам и синтаксическую проверку затронутых модулей.
- Не заводить bug artifact: дефектов по итогам локальной проверки не найдено.

## Work Performed

- Проверено, что корневой `main.py` подключает `app.handlers.menu`.
- Проверено, что `/start` в `app/handlers/menu.py` вызывает `send_welcome_sequence()` и затем возвращает reply-меню.
- Проверено, что `WELCOME_TEXT` совпадает с текстом из пользовательского запроса.
- Проверено, что `MediaGroup` строится из `project1.jpg`, `project2.jpg`, `project3.jpg` без captions.
- Проверено, что inline-кнопка использует существующий callback `go_consult`.
- Проверено, что handler `go_consult` и flow отправки номера телефона не менялись.
- Проверено, что добавлен fallback на отсутствие файлов welcome-медиа без падения бота.
- Выполнена синтаксическая проверка командой `python -m py_compile app/handlers/menu.py app/data/welcome_media.py app/keyboards/start_kb.py main.py`.

## Self-Analysis

- Полный e2e-прогон в Telegram-клиенте не выполнялся, поэтому UX подтвержден на уровне кода, а не визуального рендера в мессенджере.
- Отдельно проверено, что изменение не затрагивает `cost_handler` и другие menu branches, поэтому основной регрессионный риск локализован в `/start`.

## Risks

- Визуальный порядок welcome-photo, gallery и reply-меню зависит от Telegram-клиента и не подтвержден live.
- Альтернативный entrypoint `app/main.py` остается со своим независимым `/start`.

## Handoff

Передать задачу в `TeamLead` для финального gate: подтвердить обоснованность write scope, осознанное невмешательство в альтернативный FSM-entrypoint и готовность закрыть задачу.
