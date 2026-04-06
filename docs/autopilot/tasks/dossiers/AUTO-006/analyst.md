# Analyst Report

## Objective

Сформировать decision-complete задачу на расширение админ-панели проектов операциями редактирования, удаления и публикации в Telegram-канал.

## Inputs

- Пользовательский запрос в текущем треде
- `AGENTS.md`
- `docs/autopilot/sources-of-truth.md`
- `AUTOPILOT-FOUNDATION.md`
- `app/data/projects.py`
- `app/handlers/admin_projects.py`
- `data/projects.json`

## Decisions

- Не ломать текущую гибридную модель: seed-проекты остаются в `app/data/projects.py`, редактируемыми через UI считаются только JSON-проекты.
- Создать отдельный FSM `AdminEditProject`, не смешивая его со сценариями добавления.
- Публикацию реализовать как best-effort: отсутствие `CHANNEL_ID` или ошибка Telegram API не должны ронять admin-flow.
- Формат поста должен совпадать с пользовательской карточкой проекта по основным полям, но быть пригодным и для `media_group`, и для текста.
- Callback admin-операций можно расширить, сохраняя совместимость с текущими inline-кнопками.

## Work Performed

- Проверен текущий data-layer каталога и подтверждено, что новые админские проекты уже живут в `data/projects.json`.
- Подтверждено, что `AUTO-005` закрывал только add-flow и сознательно оставлял edit/delete заглушками.
- Зафиксирован безопасный scope: edit/delete для JSON-проектов, read-only для legacy seed.

## Self-Analysis

Вывод: пользователь запросил callback-префиксы `edit_project_` и `delete_project_`, но в коде уже есть `admin_project_edit:` и `admin_project_delete:`. Для минимального риска реализация должна поддержать целевое поведение, не ломая текущий admin-list; это лучше сделать совместимостью на уровне handler'ов и клавиатур, а не массовым переименованием внешних контрактов.

## Risks

- Редактирование legacy seed-проектов из Python-файла без миграции в JSON небезопасно и выходит за разумный минимальный slice.
- Отправка `media_group` в Telegram требует отдельной обработки `caption`: его можно безопасно класть только в первый media item.
- Реальная проверка публикации возможна только с доступным каналом и валидными `file_id`.

## Handoff

Передать в `Backend Bot Engineer`: расширить JSON-layer, FSM и admin handlers, затем зафиксировать результаты и ограничения в dossier.
