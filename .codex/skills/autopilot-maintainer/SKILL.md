# Autopilot Maintainer

## Purpose

Развивать и поддерживать сам automation contour проекта.

## Use When

- нужно создать или обновить `AGENTS.md`;
- нужно добавить process docs;
- нужно добавить templates;
- нужно создать или обновить skills;
- нужно закрыть process gap, выявленный в incident или repeated bug.

## Inputs

- `AGENTS.md`;
- `docs/autopilot/`;
- `.codex/skills/`;
- `AUTOPILOT-FOUNDATION.md`;
- incidents и feedback из dossier.

## Workflow

1. Найди process gap или новую потребность.
2. Определи, что менять: правило, шаблон, статусную модель, skill или документацию.
3. Обнови все связанные артефакты, чтобы контур не расходился.
4. Зафиксируй change summary в соответствующем dossier.

## Outputs

- обновленные правила;
- обновленные skills;
- updated templates;
- closing note по process gap.
