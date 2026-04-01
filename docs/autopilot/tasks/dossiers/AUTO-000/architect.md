# Architect Report

## Objective

Определить структуру automation contour так, чтобы он был независим от внешнего трекера и применим к текущему репозиторию бота.

## Inputs

- `AUTOPILOT-FOUNDATION.md`
- текущая структура репозитория;
- доменные документы;
- постановка bootstrap-задачи.

## Decisions

- Процессный слой размещается в `docs/autopilot/`, а не внутри `codex/`, чтобы быть локальным SSOT этого репозитория.
- Board и dossier ведутся в markdown/csv/json.
- Skills размещаются в `.codex/skills/` как repo-local contracts.
- Артефакты evidence отделяются в `artifacts/autopilot/`.

## Work Performed

- Спроектирована структура директорий.
- Определена минимальная статусная модель.
- Определена минимальная ролевая модель и шаблоны артефактов.

## Self-Analysis

- Контур intentionally file-first и без внешнего tracker adapter; в будущем может понадобиться адаптерный слой, но он не нужен для bootstrap.

## Risks

- При дальнейшем росте проекта может понадобиться автоматическая проверка ссылок и структуры dossier.

## Handoff

Передать в `Backend Bot Engineer`/`Autopilot Maintainer` на материализацию файловой структуры.
