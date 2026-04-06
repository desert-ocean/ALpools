# AUTO-007

## Header

- `task_id`: `AUTO-007`
- `title`: `Миграция каталога проектов на единый JSON-источник`
- `area`: `product`
- `priority`: `high`
- `status`: `ready_for_qa`

## Summary

Убрать тестовые seed-проекты из Python-кода и перевести каталог проектов на единый файловый источник `data/projects.json` через отдельный сервисный слой.

## Problem

Сейчас каталог использует гибридную модель: test seed-проекты живут в `app/data/projects.py`, а реальные админские записи в `data/projects.json`. Из-за этого админка удаляет только JSON-записи, а legacy-проекты остаются неудаляемыми и формируют второй источник истины.

## Scope

- Убрать или закомментировать `PROJECTS` в `app/data/projects.py`.
- Создать `app/services/projects_service.py`.
- Перевести загрузку каталога на единый источник `data/projects.json`.
- Перевести add/get/update/delete на service-layer.
- Обновить пользовательский каталог и админку без изменения FSM.
- Обработать отсутствие файла и пустой JSON без падения.

## Out Of Scope

- Изменение пользовательского сценария проектирования.
- Изменение FSM состояний.
- Изменение формата карточки проекта и callback naming.
- Введение БД или нового persistence layer кроме JSON.

## Inputs

- Пользовательский запрос в текущем треде.
- `AGENTS.md`
- `docs/autopilot/sources-of-truth.md`
- `AUTOPILOT-FOUNDATION.md`
- `app/data/projects.py`
- `app/handlers/admin_projects.py`
- `app/handlers/projects.py`
- `app/handlers/project_configurator.py`
- `app/keyboards/projects_kb.py`
- `data/projects.json`

## Dependencies

- `AUTO-004`
- `AUTO-005`
- `AUTO-006`

## Definition Of Done

- `app/data/projects.py` больше не хранит test seed-каталог.
- Создан `app/services/projects_service.py` с требуемыми CRUD-функциями.
- Все чтение и запись проектов идут только через `data/projects.json`.
- Удаление проекта удаляет запись из JSON и не возвращает ее при повторной загрузке.
- При отсутствии `data/projects.json` файл создается автоматически.
- При пустом JSON сервис возвращает пустой каталог без исключения.
- Админка и пользовательский каталог продолжают работать без изменения FSM.

## Review Requirements

- Проверить, что каталог читается только из `data/projects.json`.
- Проверить добавление, обновление и удаление проекта через service-layer.
- Проверить удаление существующего JSON-проекта с повторной загрузкой списка.
- Проверить отсутствие регрессии в пользовательском открытии карточки проекта и выборе проекта в заявку.

## Main Artifact

- `app/services/projects_service.py`

## Next Handoff

- `Backend Bot Engineer`
