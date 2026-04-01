# AUTO-000

## Header

- `task_id`: `AUTO-000`
- `title`: `Autopilot foundation for ALpools`
- `area`: `autopilot`
- `priority`: `high`
- `status`: `done`

## Summary

Создать полноценный project-specific contour automation для репозитория `ALpools` на основе приложенных документов и текущего кода.

## Problem

В проекте не было локального цельного operational framework для агентной разработки: отсутствовал root-level `AGENTS.md`, не было единого board/dossier контура и project-specific skills.

## Scope

- Корневой `AGENTS.md`.
- Процессные документы в `docs/autopilot/`.
- Board, templates и стартовый dossier.
- Project-specific skills в `.codex/skills/`.

## Out Of Scope

- Интеграция с внешним трекером.
- Реализация новых продуктовых фич бота.
- Полная автоматизация CI/валидации контура.

## Inputs

- пользовательский запрос;
- `AUTOPILOT-FOUNDATION.md`;
- `documents/tz_bass.docx`;
- `documents/rekviz_AKVA_LOGO.DOC`;
- текущий код `app/`.

## Dependencies

- нет внешних зависимостей, кроме локального доступа к репозиторию.

## Definition Of Done

- В корне есть `AGENTS.md`.
- Создан `docs/autopilot/` с process SSOT.
- Создан `board.csv`, `board.md`, templates и dossier.
- Создан набор skills, покрывающий роли и automation goals.

## Review Requirements

- Проверить внутреннюю связность файлов.
- Проверить полноту роли/статуса/шаблонов.
- Проверить, что контур можно использовать сразу.

## Main Artifact

- `AGENTS.md`

## Next Handoff

- `Coordinator` начинает использовать контур для следующих задач.
