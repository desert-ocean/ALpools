# Handoff

## Objective

Зафиксировать передачу `AUTO-006` после реализации и QA.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-006.md`

## Decisions

- Текущий статус: `ready_for_qa`.
- Следующий владелец: `QA`.

## Work Performed

- Создан task-first контур `AUTO-006`.
- Реализованы редактирование, удаление и публикация проектов каталога.
- Выполнена локальная синтаксическая проверка и импортный smoke-check.

## Self-Analysis

- Вывод: кодовый slice завершён, но для acceptance нужна ручная Telegram-проверка публикации в канал и UX редактирования фотографий.

## Risks

- Публикация в канал не подтверждена реальным окружением.
- Legacy seed-проекты намеренно не поддерживают edit/delete через UI.

## Handoff

- Кто передает: `Backend Bot Engineer`
- Кому передает: `QA`
- Какой текущий статус: `ready_for_qa`
- В какой статус перевести: `qa_review` или вернуть в `in_progress` при дефектах
- Что уже сделано: расширены data-layer, FSM, admin-клавиатуры, add/edit/delete/publish handlers и конфиг `CHANNEL_ID`
- Что делать следующим шагом: проверить сценарии редактирования, удаления, ручной публикации и автопубликации после добавления
- Какие входы обязательны: `app/data/projects.py`, `app/states/admin_states.py`, `app/keyboards/admin_kb.py`, `app/handlers/admin_projects.py`, `app/config.py`, `.env.example`
- Какие риски остаются: живой Telegram-check публикации и ограничения legacy-проектов
