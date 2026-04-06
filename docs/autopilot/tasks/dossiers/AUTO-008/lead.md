## Objective

Подтвердить, что задача может быть выполнена минимальным кодовым срезом без архитектурной переработки и без риска для существующего FSM расчёта.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-008.md`
- `docs/autopilot/tasks/dossiers/AUTO-008/analyst.md`
- `app/handlers/menu.py`
- `app/handlers/cost_handler.py`
- `main.py`

## Decisions

- Разрешить write scope файлами `app/handlers/menu.py`, `docs/autopilot/tasks/board.csv`, `docs/autopilot/tasks/board.md`, `docs/autopilot/tasks/cards/AUTO-008.md` и dossier `AUTO-008`.
- Не трогать `cost_handler` по логике и состояниям; допустимо только подтвердить, что он использует обновлённую константу.
- Не трогать `project_configurator.py`, так как это отдельный продуктовый сценарий.

## Work Performed

- Проверен proposed scope на соответствие пользовательскому запросу и `AGENTS.md`.
- Подтверждено, что задача не требует `Architect`, так как не меняет data contracts, FSM structure или routing architecture.

## Self-Analysis

- Вывод: основной риск не в коде расчёта, а в том, чтобы не оставить дублирующий handler по тому же тексту кнопки.
- Не проводилась ручная UX-проверка в Telegram-клиенте; это переносится в QA как локальная верификация по коду и синтаксису.

## Risks

- Если в будущем появятся внешние ссылки на старое название `Предварительная стоимость бассейна`, они могут устареть.
- Если в кодовой базе есть неочевидные сравнения по literal-строке вместо константы, они могут не попасть в write scope, но поиск по `app/` таких мест не показал.

## Handoff

Передать задачу `Backend Bot Engineer` в статус `in_progress` для реализации минимальной правки меню и удаления мёртвых handler-веток.
