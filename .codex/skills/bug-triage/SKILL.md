# Bug Triage

## Purpose

Стандартизировать ведение продуктовых дефектов.

## Use When

- найден дефект в логике бота;
- QA или разработка выявили расхождение ожидаемого и фактического поведения;
- нужно оформить bug artifact и root cause.

## Inputs

- `docs/autopilot/bug-flow.md`;
- bug template;
- dossier исходной задачи;
- reproduction evidence.

## Workflow

1. Подтверди, что это bug, а не incident.
2. Зафиксируй symptom, expected, actual.
3. Определи severity.
4. Зафиксируй шаги воспроизведения и среду.
5. Свяжи bug с основной задачей.
6. После фикса запиши root cause и verification.

## Outputs

- `bug.md`;
- bug entry в board при необходимости;
- решение по owner и next step.
