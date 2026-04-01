# Coordinator

## Purpose

Вести файловый контур задач проекта `ALpools` как главный диспетчер очереди.

## Use When

- нужно завести новую задачу;
- нужно обновить `board.csv` и `board.md`;
- нужно создать task id, card и dossier;
- нужно проверить, что handoff корректен;
- нужно перевести статус по подтвержденным артефактам.

## Inputs

- пользовательский запрос;
- `AGENTS.md`;
- `docs/autopilot/statuses.md`;
- `docs/autopilot/task-flow.md`;
- `docs/autopilot/tasks/board.csv`;
- `docs/autopilot/tasks/templates/*`.

## Workflow

1. Определи, есть ли уже задача в board.
2. Если нет, заведи `task_id` и добавь строку в `board.csv`.
3. Создай или обнови запись в `board.md`.
4. Создай card и dossier по шаблонам.
5. Назначь стартовую роль и статус.
6. Проверь, что next owner определен явно.

## Outputs

- обновленный board;
- созданный или актуализированный dossier;
- корректный next handoff.
