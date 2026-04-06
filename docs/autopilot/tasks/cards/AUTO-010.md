# AUTO-010

## Header

- `task_id`: `AUTO-010`
- `title`: `Расширение стартовой MediaGroup до 6 фото`
- `area`: `product`
- `priority`: `high`
- `status`: `ready_for_lead_gate`

## Summary

Обновить рабочий `/start` в `app/handlers/menu.py`, чтобы бот отправлял все шесть проектных фото через `send_media_group`, при этом caption оставался на первом элементе, а консультационный flow и reply-меню не ломались.

## Problem

Текущая welcome-галерея в рабочем router отправляет только `project1.jpg`-`project3.jpg`. Новый запрос требует все шесть фото и уточняет, что текст должен оказаться на первом элементе галереи, а кнопка консультации должна сохраниться без поломки текущего поведения.

## Scope

- Обновить источник welcome-галереи в `app/data/welcome_media.py`.
- Перевести `/start` в `app/handlers/menu.py` на отправку всех шести фото через `send_media_group`.
- Поместить caption в первый элемент альбома.
- Сохранить существующий callback `go_consult` и reply-меню.
- Зафиксировать ограничение Telegram по inline-кнопкам в media group в dossier.

## Out Of Scope

- Изменение текстов приветствия.
- Изменение callback `go_consult` или consultation flow.
- Изменение альтернативного `/start` в `app/main.py` и `app/fsm/handlers.py`.
- Добавление новых фото, кроме уже существующих `project1.jpg`-`project6.jpg`.

## Inputs

- Пользовательский запрос в текущем треде.
- `AGENTS.md`
- `docs/autopilot/sources-of-truth.md`
- `AUTOPILOT-FOUNDATION.md`
- `app/handlers/menu.py`
- `app/data/welcome_media.py`
- `app/keyboards/start_kb.py`
- `app/data/photos/project1.jpg`
- `app/data/photos/project2.jpg`
- `app/data/photos/project3.jpg`
- `app/data/photos/project4.jpg`
- `app/data/photos/project5.jpg`
- `app/data/photos/project6.jpg`

## Dependencies

- Все шесть файлов должны существовать в `app/data/photos/`.
- Текущий Telegram-flow допускает caption только на первом элементе media group.
- Inline-кнопка консультации должна остаться совместимой с callback `go_consult`.

## Definition Of Done

- `/start` отправляет `MediaGroup` ровно из шести фото `project1.jpg`-`project6.jpg`.
- Первый элемент media group содержит `WELCOME_TEXT` в caption.
- Inline-кнопка `📞 Получить консультацию` остается доступной пользователю после альбома и использует существующий callback `go_consult`.
- Reply-меню после `/start` остается доступным.
- Изменение локализовано в существующем welcome-flow и не затрагивает другие разделы бота.
- Локальная синтаксическая проверка затронутых Python-файлов проходит без ошибок.

## Review Requirements

- Проверить, что в `WELCOME_GALLERY_SOURCES` перечислены `project1.jpg`-`project6.jpg`.
- Проверить, что caption задается только первому `InputMediaPhoto`.
- Проверить, что callback `go_consult` не менялся.
- Проверить, что `/start` после welcome-flow по-прежнему показывает существующее reply-меню.
- Проверить, что Telegram-ограничение по inline-кнопкам у media group явно задокументировано.

## Main Artifact

- `app/handlers/menu.py`

## Next Handoff

- `TeamLead`
