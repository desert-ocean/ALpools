# Roles

## Coordinator

Отвечает за:

- `board.csv`;
- `board.md`;
- создание task ids;
- смену статусов по подтвержденным артефактам;
- контроль полноты dossier;
- контроль очереди и next owner.

## Analyst

Отвечает за:

- problem statement;
- scope / out of scope;
- DoD;
- decomposition;
- риски;
- список входных артефактов;
- открытые вопросы.

## TeamLead

Отвечает за три gate:

- после анализа;
- после реализации;
- после QA.

## Architect

Отвечает за:

- границы модулей;
- модель хранения данных;
- контракты между FSM, handlers, services, storage;
- расширяемость анкеты и pricing flow;
- cross-cutting decisions.

## Domain Modeler

Отвечает за:

- перевод технического задания по бассейну в формализованный опросник;
- структуру полей и их инженерную семантику;
- связи между ответами пользователя и итоговым ТЗ.

## Backend Bot Engineer

Отвечает за:

- handlers;
- FSM;
- services;
- persistence;
- интеграцию с Telegram;
- отправку заявок админу;
- pricing flow.

## QA

Отвечает за:

- проверку DoD;
- функциональные сценарии;
- регрессию;
- проверку dossier completeness;
- bug reports.

## Bug Triage

Отвечает за:

- классификацию дефекта;
- локализацию;
- severity;
- reproduction;
- связь бага с исходной задачей.

## Stability Engineer

Отвечает за:

- broken environment;
- broken run path;
- broken skill;
- broken board/status loop;
- broken artifacts generation;
- broken integration path;
- возврат задач из `system_blocked`.

## Customer Reporter

Отвечает за краткие owner-facing summaries.

## Autopilot Maintainer

Отвечает за:

- `AGENTS.md`;
- `docs/autopilot/`;
- `.codex/skills/`;
- templates;
- качество самого automation contour.
