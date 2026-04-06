# AUTO-009

## Header

- `task_id`: `AUTO-009`
- `title`: `Приветственный /start с фото компании и MediaGroup`
- `area`: `product`
- `priority`: `high`
- `status`: `done`

## Summary

Добавить в стартовый сценарий бота раздела «Бассейны» приветственное сообщение с основным фото, фиксированным текстом, inline-кнопкой консультации и дополнительной галереей через `MediaGroup`, не ломая существующие handlers и меню.

## Problem

Текущий `/start` в рабочем маршруте `main.py -> app/handlers/menu.py` показывает только текстовое меню и не дает стартового визуального блока компании. Пользовательский запрос требует отдельный welcome-flow с фото, акцентом на 10-летний опыт и последующей галереей проектов, при этом существующие пути консультации и reply-меню должны остаться рабочими.

## Scope

- Обновить рабочий `/start` в `app/handlers/menu.py`.
- Добавить source-of-truth для welcome-текста и стартовых фото в `app/data/`.
- Добавить inline-клавиатуру для кнопки `📞 Получить консультацию` в `app/keyboards/`.
- Отправлять основное фото с точным текстом и inline-кнопкой.
- После основного фото отправлять галерею `MediaGroup` из `project1.jpg`, `project2.jpg`, `project3.jpg`.
- Сохранить существующее reply-меню и callback `go_consult`.
- Обновить board, card и dossier.

## Out Of Scope

- Изменение FSM-сценариев и логики заявок.
- Изменение `app/main.py`, где `/start` запускает отдельный DB/FSM flow черновика проекта; вмешательство туда создало бы отдельный продуктовый сценарий вне текущего scope.
- Изменение текстов существующих разделов меню, кроме стартового приветствия.
- Добавление новых внешних ссылок менеджера, если можно переиспользовать существующий consultation flow.

## Inputs

- Пользовательский запрос в текущем треде.
- `AGENTS.md`
- `docs/autopilot/sources-of-truth.md`
- `AUTOPILOT-FOUNDATION.md`
- `main.py`
- `app/handlers/menu.py`
- `app/data/photos/welcome.jpg`
- `app/data/photos/project1.jpg`
- `app/data/photos/project2.jpg`
- `app/data/photos/project3.jpg`

## Dependencies

- Наличие файлов welcome-галереи в `app/data/photos/`.
- Сохранение callback `go_consult` и reply-меню как совместимого контракта для существующего consultation flow.

## Definition Of Done

- `/start` в рабочем entrypoint отправляет основное фото `welcome.jpg` с точным текстом из запроса.
- На основном welcome-сообщении есть inline-кнопка `📞 Получить консультацию`.
- Нажатие на inline-кнопку использует существующий callback `go_consult` и не ломает консультационный сценарий.
- После основного фото отправляется `MediaGroup` без текста из `project1.jpg`, `project2.jpg`, `project3.jpg`.
- После welcome-блока пользователю доступно существующее reply-меню разделов.
- Изменения вынесены по структуре проекта в `handlers`, `keyboards`, `data`.
- Локальная синтаксическая проверка затронутых Python-файлов проходит без ошибок.

## Review Requirements

- Проверить точное совпадение welcome-текста с запросом.
- Проверить, что `MediaGroup` собирается из файлов `app/data/photos/project1.jpg`-`project3.jpg`.
- Проверить, что callback `go_consult` не менялся и inline-кнопка ведет в существующий поток консультации.
- Проверить, что `main_menu` после `/start` по-прежнему доступно.
- Проверить, что `app/main.py` и `app/fsm/handlers.py` сознательно не менялись как отдельный flow.

## Main Artifact

- `app/handlers/menu.py`

## Next Handoff

- `Coordinator`
