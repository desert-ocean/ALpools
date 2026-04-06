# Handoff

## Objective

Зафиксировать передачу задачи `AUTO-004` после реализации и QA.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-004.md`

## Decisions

- Текущий статус: `ready_for_qa`.
- Следующий владелец: `QA`.

## Work Performed

- Оформлены card и dossier.
- Реализован каталог проектов отдельными слоями `data`, `keyboards`, `handlers`.
- Подключён router каталога в текущий `main.py`.
- Добавлен переход из карточки проекта в существующий `ProjectFSM` с сохранением `selected_project`.
- Выполнена синтаксическая локальная проверка затронутых модулей.

## Self-Analysis

Вывод: техническая реализация завершена, но пользовательский путь требует ручной Telegram-проверки, особенно для callback-навигации и финального UX.

## Risks

- Ветка `media_group` не была проверена на реальных `file_id`.
- Реальная order-of-messages проверяется только в Telegram-клиенте.

## Handoff

- Кто передает: `Backend Bot Engineer`
- Кому передает: `QA`
- Какой текущий статус: `ready_for_qa`
- В какой статус перевести: `qa_review` или вернуть в `in_progress` при дефектах
- Что уже сделано: реализованы каталог, карточка проекта, кнопка конверсии и интеграция с существующим `ProjectFSM`
- Что делать следующим шагом: проверить сценарии каталога и перехода в заявку
- Какие входы обязательны: `app/data/projects.py`, `app/keyboards/projects_kb.py`, `app/handlers/projects.py`, `app/handlers/project_configurator.py`, `main.py`
- Какие риски остаются: корректность перехода в существующий FSM и работа ветки без фото
