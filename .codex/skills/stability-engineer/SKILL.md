# Stability Engineer

## Purpose

Восстанавливать работоспособность самого контура разработки и автоматизации.

## Use When

- broken environment;
- broken skill;
- broken status loop;
- broken board/dossier structure;
- broken local tooling/run path;
- broken integration path мешает продолжать задачу.

## Inputs

- `docs/autopilot/stability.md`;
- incident template;
- логи, симптомы, failed commands;
- связанные dossiers.

## Workflow

1. Классифицируй проблему как incident.
2. Переведи задачу в `system_blocked` или `stability_fix`.
3. Создай `incident.md`.
4. Отдели symptom от root cause.
5. Восстанови работоспособность.
6. Зафиксируй prevention action.
7. Верни исходную задачу в рабочий поток.

## Outputs

- `incident.md`;
- recovery summary;
- обновленный skill/runbook/rule при необходимости.
