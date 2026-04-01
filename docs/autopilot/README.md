# ALpools Autopilot

Этот каталог содержит project-specific contour automation для `ALpools`.

Цель контура:

- превратить разработку Telegram-бота в управляемый artifact-driven процесс;
- зафиксировать источники истины, роли, статусы и handoff;
- вести продуктовые задачи, баги и системные инциденты в одном файловом контуре;
- стандартизировать skills для Codex-агентов;
- сделать развитие самого автопилота воспроизводимым.

## Состав

- `sources-of-truth.md` — что является истиной по домену, коду и процессу.
- `roles.md` — роли, обязанности, входы и выходы.
- `statuses.md` — статусная модель и разрешенные переходы.
- `task-flow.md` — feature/task lifecycle.
- `bug-flow.md` — bug lifecycle.
- `stability.md` — incident lifecycle и зона ответственности `Stability Engineer`.
- `reporting.md` — форматы task reports, handoff и owner reports.
- `skills-policy.md` — политика применения и эволюции skills.
- `tasks/` — board, cards, dossiers и templates.

## Как использовать

1. Любая новая нетривиальная работа начинается с `board.csv`.
2. Затем создается `task card`.
3. Затем создается `dossier`.
4. Каждая роль пишет свой отчет в dossier.
5. Переход статуса возможен только после появления подтверждающего артефакта.
