## Objective

Сформировать decision-complete задачу на добавление welcome-сценария `/start` с фото компании, фиксированным текстом, inline-кнопкой консультации и последующей галереей `MediaGroup` без поломки существующего бота.

## Inputs

- Пользовательский запрос в текущем треде.
- `AGENTS.md`
- `docs/autopilot/sources-of-truth.md`
- `AUTOPILOT-FOUNDATION.md`
- `main.py`
- `app/handlers/menu.py`
- `app/fsm/handlers.py`
- `app/data/photos/welcome.jpg`
- `app/data/photos/project1.jpg`
- `app/data/photos/project2.jpg`
- `app/data/photos/project3.jpg`

## Decisions

- Реализовывать welcome-flow в `app/handlers/menu.py`, потому что именно этот router подключается в корневом `main.py`, который является рабочей точкой запуска пользовательского меню.
- Не трогать `app/fsm/handlers.py` и `app/main.py`: там `/start` обслуживает отдельный DB/FSM flow черновика проекта, и смешивание с маркетинговым welcome-сценарием создаст несанкционированное изменение продукта.
- Вынести welcome-текст и photo sources в `app/data/welcome_media.py` как единый source of truth.
- Вынести inline-кнопку в `app/keyboards/start_kb.py`.
- Для inline-кнопки использовать существующий callback `go_consult`, чтобы не создавать новый consultation path и не вводить фиктивную ссылку менеджера.
- После welcome-блока вернуть reply-меню отдельным сообщением, чтобы не ломать текущую навигацию по разделам.

## Work Performed

- Проверены текущие entrypoints `main.py` и `app/main.py`.
- Проверены все обработчики `/start` в репозитории.
- Проверено наличие нужных файлов изображений в `app/data/photos/`.
- Зафиксированы scope и out-of-scope для безопасной реализации.

## Self-Analysis

- Вывод: ключевой риск был не в самом `MediaGroup`, а в наличии нескольких `/start`-handlers в разных entrypoints. Решение ограничить изменения `menu.py` минимизирует регрессию и соответствует текущему рабочему запуску.
- Не подтверждено документально, какой из entrypoints используется в production прямо сейчас; вывод сделан по текущему корневому `main.py` и существующему menu-router.

## Risks

- Если production запускается не через корневой `main.py`, а через `app/main.py`, новый welcome-flow не появится в том entrypoint.
- Без живого прогона в Telegram нельзя подтвердить реальный визуальный порядок сообщений в клиенте, только код и синтаксис.

## Handoff

Передать задачу в `Backend Bot Engineer` на минимальную реализацию в `app/handlers/menu.py`, `app/data/welcome_media.py` и `app/keyboards/start_kb.py` с последующей локальной проверкой.
