# Sources of Truth

## 1. Бизнес и домен

Основной источник истины по инженерной доменной модели проекта:

- `documents/tz_bass.docx`

Основной источник истины по реквизитам компании:

- `documents/rekviz_AKVA_LOGO.DOC`

## 2. Продукт и код

Основной источник истины по фактическому поведению бота:

- код в `app/`

Ключевые точки:

- `main.py` и `app/main.py` — точки запуска;
- `app/handlers/` — пользовательские сценарии;
- `app/fsm/` — stateful flows;
- `app/services/` — доменная и вспомогательная логика;
- `app/db/` — модель данных и доступ к БД;
- `app/config/` — конфигурация шагов и параметров.

## 3. Процесс

Основной источник истины по локальному automation contour:

- корневой `AGENTS.md`
- документы в `docs/autopilot/`
- templates в `docs/autopilot/tasks/templates/`
- project-specific skills в `.codex/skills/`

## 4. Приоритет источников

Если нужно выбрать, чему верить:

1. Явно подтвержденное пользовательское решение в текущем треде.
2. `documents/tz_bass.docx` и `documents/rekviz_AKVA_LOGO.DOC`.
3. Зафиксированные артефакты в `docs/autopilot/tasks/`.
4. `AGENTS.md` и `docs/autopilot/`.
5. Текущий код.
6. Общий фундамент `AUTOPILOT-FOUNDATION.md`.
