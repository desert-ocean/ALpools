# AUTO-004

## Header

- `task_id`: `AUTO-004`
- `title`: `Каталог реализованных проектов и конверсия в заявку`
- `area`: `product`
- `priority`: `high`
- `status`: `ready_for_qa`

## Summary

Реализовать раздел `🏗 Реализованные проекты` как каталог с карточками проектов и кнопкой конверсии `💬 Хочу такой же проект`, которая переводит пользователя в существующий FSM заявки.

## Problem

Раздел реализованных проектов сейчас пустой и не даёт пользователю ни примеров работ, ни целевого перехода в заявку по понравившемуся проекту.

## Scope

- Создать слой данных каталога в `app/data/projects.py`.
- Создать inline-клавиатуры каталога в `app/keyboards/projects_kb.py`.
- Создать handlers каталога в `app/handlers/projects.py`.
- Показать список проектов и карточку проекта.
- Добавить кнопку `💬 Хочу такой же проект`.
- Сохранить `selected_project` в `FSMContext`.
- Перевести пользователя в существующий `ProjectFSM` без создания отдельной новой FSM.
- Подключить router каталога в текущую сборку приложения.

## Out Of Scope

- Изменение главного меню.
- Изменение текста кнопки входа в раздел.
- Перестройка общей архитектуры configurator flow.
- Загрузка реальных Telegram `file_id` из внешнего хранилища.

## Inputs

- Пользовательский запрос в текущем треде.
- `AGENTS.md`.
- `docs/autopilot/sources-of-truth.md`.
- `AUTOPILOT-FOUNDATION.md`.
- `app/handlers/menu.py`.
- `app/handlers/project_configurator.py`.
- `main.py`.

## Dependencies

- Активный FSM заявки в `app/handlers/project_configurator.py`.
- Текущий вход в раздел `🏗 Реализованные проекты` через `app/handlers/menu.py`.

## Definition Of Done

- Раздел `🏗 Реализованные проекты` показывает список из 23 тестовых проектов.
- Карточка проекта показывает `title`, `city`, `size`, `type`, `description`.
- При наличии `photos` отправляется `media_group`, при отсутствии фото карточка всё равно работает.
- Кнопка `💬 Хочу такой же проект` сохраняет `selected_project` в FSM.
- Переход выполняется в существующий `ProjectFSM`.
- Первое сообщение для конверсии из каталога: `💬 Заявка на проект: <название проекта>\n\nВведите ваше имя:`
- Главное меню и точка входа в раздел не меняются.

## Review Requirements

- Проверить router order и отсутствие конфликта с fallback из `menu.py`.
- Проверить callbacks `projects`, `project_`, `project_request_`.
- Проверить переход в существующий FSM без отдельной новой state machine.
- Проверить отправку карточки без фото.

## Main Artifact

- `app/handlers/projects.py`

## Next Handoff

- `QA` для проверки сценариев каталога и перехода в заявку.
