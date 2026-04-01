# Universal Codex Autopilot Foundation

> Канонический фундамент для запуска автопилота разработки на базе Codex CLI в любом проекте.
> Этот документ описывает не один конкретный репозиторий, а переносимую операционную систему агентной разработки.

## 1. Назначение

Этот документ нужен, чтобы в любом новом проекте можно было быстро развернуть:
- единый цикл разработки;
- файловый контур управления задачами;
- предсказуемую ролевую модель;
- обязательную отчётность и handoff;
- контроль качества после QA;
- отдельный контур обработки багов;
- отдельный контур обработки сбоев автопилота и окружения;
- Codex CLI как агентное ядро процесса.

Цель не в том, чтобы "помогать кодить", а в том, чтобы выстроить воспроизводимый и контролируемый контур разработки, где:
- не теряется контекст;
- решения не остаются только в чате;
- баги и инциденты фиксируются;
- blocked/system_blocked не висят без владельца;
- любой следующий агент или человек может поднять задачу с документов, а не с пересказа.

## 2. Принципы

### 2.1. Файловый контур как ядро

Базовая модель не зависит от Redmine, Jira или GitLab issues.

Ядро живёт в:
- `md`
- `csv`
- `json`

Внешние трекеры допускаются только как адаптеры, а не как источник истины по умолчанию.

### 2.2. Decision-complete документация

Любая задача должна доходить до состояния, где следующий исполнитель:
- понимает цель;
- понимает границы;
- понимает критерии готовности;
- понимает, что уже сделано;
- понимает, что осталось;
- понимает, почему были приняты именно такие решения.

### 2.3. Никаких устных handoff

Если решение принято, но не попало в артефакты:
- его не существует для автопилота;
- задача считается неполной;
- следующий исполнитель имеет право вернуть её назад.

### 2.4. Разделение продуктовых и системных проблем

Нужно жёстко различать:
- продуктовая задача;
- продуктовый баг;
- системный инцидент;
- сбой автопилота;
- сбой окружения;
- сбой интеграции.

Иначе команда начинает лечить всё одинаково и теряет контроль.

### 2.5. QA не является последним слоем контроля

После QA должен существовать ещё один gate:
- архитектурный;
- процессный;
- управленческий.

Этот gate выполняет `TeamLead`.

### 2.6. Автопилот тоже нуждается в сопровождении

Если:
- сломан агентный пайплайн;
- перестал работать Figma MCP;
- битый skill;
- завис blocked/status cycle;
- развалился context pack;
- сломались секреты, runner, shell, dev-контур;

этим должен заниматься не разработчик фичи, а отдельная роль:
- `Stability Engineer`.

## 3. Базовая ролевая модель

Рекомендуемая команда автопилота на 5-8 ролей:

### 3.1. Coordinator

Отвечает за:
- очередь задач;
- `board.csv`;
- смену статусов;
- порядок handoff;
- review queue;
- контроль, что документы и очередь не расходятся.

Не пишет продуктовый код по умолчанию.

### 3.2. Analyst

Отвечает за:
- постановку задачи;
- problem statement;
- user intent;
- scope / out of scope;
- входные источники истины;
- DoD;
- риски;
- open questions;
- decomposition readiness.

Главный результат:
- задача становится исполнимой, а не просто "идеей".

### 3.3. TeamLead

Отвечает за:
- gate после аналитики;
- gate после реализации;
- gate после QA;
- решение, можно ли задачу запускать, дробить, откладывать или блокировать;
- проверку качества не только результата, но и процесса.

TeamLead должен проверять:
- не принято ли слабое архитектурное решение;
- не потеряны ли важные ограничения;
- нет ли скрытого долга;
- полны ли отчёты;
- достаточно ли хорошо оформлен handoff.

### 3.4. Architect

Отвечает за:
- cross-cutting решения;
- архитектурные контракты;
- boundary между слоями;
- integration model;
- схемы взаимодействия подсистем;
- data/auth/API contracts;
- ADR.

Architect не должен заменять Analyst и не должен подменять собой FE/BE implementation.

### 3.5. Design Agent

Отвечает за:
- Figma MCP;
- `node-id`;
- baseline screenshots;
- screen states;
- `design.md`;
- design-to-frontend handoff.

### 3.6. Frontend

Отвечает за:
- UI;
- layout;
- navigation;
- responsive behavior;
- frontend implementation;
- точное следование design contract.

Не определяет API и domain shape по собственной инициативе.

### 3.7. Backend

Отвечает за:
- API;
- domain layer;
- service layer;
- data access;
- auth/session internals;
- backend integration.

Не должен молча менять product behavior, если это не закреплено в specs и contracts.

### 3.8. QA

Отвечает за:
- проверку DoD;
- test scenarios;
- regression;
- review readiness;
- баг-репорты;
- проверку полноты handoff.

QA отвечает за качество подтверждения, но не является последней инстанцией закрытия задачи.

### 3.9. Stability Engineer

Обязательная роль.

Отвечает за:
- `system_blocked`;
- `stability_fix`;
- сломанное окружение;
- сломанный CI/CD;
- сломанные access-paths;
- сломанные агенты и skills;
- broken prompts/rules/context packs;
- Figma/Git/integration incidents;
- контур здоровья самого автопилота.

Это не DevOps в узком смысле.
Это инженер устойчивости контура разработки.

## 4. Базовая структура файлового контура

Рекомендуемая структура для любого проекта:

```text
docs/autopilot/
  README.md
  sources-of-truth.md
  roles.md
  statuses.md
  task-flow.md
  bug-flow.md
  reporting.md
  stability.md
  skills-policy.md
  codex-cli.md
  review-gates.md

docs/autopilot/tasks/
  board.csv
  board.md
  cards/
  dossiers/
  templates/

artifacts/autopilot/
  evidence/
  bugs/
  incidents/
  logs/
  screenshots/
```

### 4.1. Source of truth

Machine source of truth:
- `board.csv`

Human-readable summary:
- `board.md`

Task-specific source of truth:
- `cards/<TASK_ID>.md`
- `dossiers/<TASK_ID>/`

### 4.2. Что хранится в dossier

Минимум:
- `INDEX.md`
- `manifest.json`
- `analyst.md`
- `lead.md`
- `architect.md` при необходимости
- `design.md` для UI-задач
- `frontend.md` / `backend.md`
- `qa.md`
- `handoff.md`

Дополнительно:
- `bug.md`
- `incident.md`
- `review.md`
- ссылки на screenshots, evidence, logs

## 5. Status model

### 5.1. Основные статусы

- `todo`
- `analysis`
- `ready_for_lead`
- `ready_for_arch`
- `ready_for_design`
- `ready_for_impl`
- `in_progress`
- `ready_for_qa`
- `qa_review`
- `ready_for_lead_gate`
- `done`
- `canceled`

### 5.2. Проблемные статусы

- `blocked`
- `system_blocked`
- `stability_fix`

### 5.3. Семантика

#### `blocked`

Используется, если:
- нет решения;
- нет доступа;
- не утверждён scope;
- конфликт требований;
- ждём внешний ответ;
- не хватает продукта/дизайна/данных.

Владелец:
- текущая ведущая роль задачи;
- эскалация к `Coordinator` или `TeamLead`.

#### `system_blocked`

Используется, если:
- сломано окружение;
- не работают агенты;
- broken skill;
- broken CI;
- broken runner;
- broken MCP;
- broken secret visibility;
- broken branch/push/deploy/tooling path.

Владелец:
- `Stability Engineer`

#### `stability_fix`

Используется, если:
- системная проблема принята в работу;
- идёт восстановление контура;
- создаётся incident report;
- задача ещё не возвращена в обычный поток.

Владелец:
- `Stability Engineer`

### 5.4. Кто может менять статус

- `Coordinator` — может менять все workflow-статусы по подтверждённым артефактам.
- `TeamLead` — может переводить в `blocked`, `ready_for_impl`, `ready_for_lead_gate`, `done`, `canceled`.
- `QA` — может переводить в `qa_review`, `ready_for_lead_gate`, назад в `in_progress`, или в `blocked`.
- `Stability Engineer` — может переводить в `system_blocked`, `stability_fix`, `ready_for_impl` после восстановления контура.

## 6. Артефакты задачи

### 6.1. Task Card

Должна содержать:
- `task_id`
- title
- summary
- scope
- out of scope
- inputs
- DoD
- main artifact
- review requirements
- next handoff

### 6.2. Dossier Index

Должен содержать:
- current status
- current owner role
- epic / area
- updated_at
- список role reports
- main artifacts
- manifest

### 6.3. Manifest

Нужен как machine-readable summary.

Минимальные поля:
- `task_id`
- `title`
- `status`
- `role`
- `area`
- `main_artifact`
- `review_required`
- `review_artifact`
- `review_summary`
- `depends_on`
- `next_task`
- `updated_at`

## 7. Role report standard

Каждый role report должен содержать одинаковые секции:

- `Objective`
- `Inputs`
- `Decisions`
- `Work Performed`
- `Self-Analysis`
- `Risks`
- `Handoff`

### 7.1. Self-Analysis обязателен

Каждая роль должна отвечать:
- что могло быть понято неправильно;
- что не проверено до конца;
- где есть риск слабого решения;
- что должна перепроверить следующая роль.

Это обязательная часть автопилота, чтобы агент:
- не имитировал уверенность;
- сам указывал слабые места;
- оставлял материал для следующей проверки.

## 8. Handoff contract

Каждый handoff обязан содержать:
- from role
- to role
- current status
- next status
- what was done
- what exactly to do next
- required inputs
- known risks
- links to artifacts

Следующий исполнитель должен мочь начать работу:
- без чата;
- без допроса предыдущего исполнителя;
- только по dossier.

## 9. Review gates

### 9.1. QA Gate

QA проверяет:
- выполнен ли DoD;
- соответствуют ли артефакты постановке;
- нет ли явных пропусков;
- есть ли regression risk;
- есть ли корректный review artifact.

### 9.2. TeamLead Gate

После QA задача обязательно идёт в `ready_for_lead_gate`.

TeamLead проверяет:
- качество решения;
- полноту отчётности;
- корректность boundary и contracts;
- отсутствие скрытых долгов;
- готовность к фактическому закрытию.

Без TeamLead Gate задача не считается по-настоящему закрытой.

## 10. Feature cycle

Базовый цикл:

1. `todo`
2. `analysis`
3. `ready_for_lead`
4. `ready_for_arch` / `ready_for_design` при необходимости
5. `ready_for_impl`
6. `in_progress`
7. `ready_for_qa`
8. `qa_review`
9. `ready_for_lead_gate`
10. `done`

Возвраты допустимы:
- `qa_review -> in_progress`
- `ready_for_lead -> analysis`
- `ready_for_impl -> analysis`
- `ready_for_lead_gate -> in_progress`
- `any -> blocked`
- `any -> system_blocked`

## 11. Bug flow

### 11.1. Когда заводить баг отдельно

Отдельный `bug artifact` обязателен, если:
- найден реальный дефект;
- дефект не сводится к мелкой правке в той же задаче;
- нужен отдельный root cause;
- дефект затрагивает acceptance;
- нужен регрессионный след.

### 11.2. Минимальный bug artifact

Должен содержать:
- symptom
- expected behavior
- actual behavior
- reproduction steps
- environment
- owner
- severity
- linked task
- root cause
- fix summary
- QA verification

### 11.3. Bug lifecycle

1. bug detected
2. bug logged
3. localization
4. fix
5. QA verification
6. lead gate
7. closed

### 11.4. Root cause обязателен

Фикс без root cause не считается завершённым процессом.

## 12. System incident flow

### 12.1. Когда это incident, а не обычный баг

Это `system incident`, если проблема ломает:
- сам процесс разработки;
- инструменты;
- агента;
- CI/CD;
- окружение;
- доступы;
- Figma MCP;
- навигацию по контексту;
- структурную согласованность автопилота.

### 12.2. Incident artifact

Минимум:
- incident id
- symptom
- trigger
- impacted tasks
- first detected by
- owner = `Stability Engineer`
- diagnosis
- fix
- recovery confirmation
- prevention action

### 12.3. Lifecycle

1. task enters `system_blocked`
2. incident created
3. `Stability Engineer` takes ownership
4. status -> `stability_fix`
5. root cause + fix
6. recovery confirmation
7. original task returns to queue

## 13. Stability Engineer playbook

### 13.1. Область ответственности

Stability Engineer чинит:
- broken local environment
- broken dev shell
- broken push/deploy path
- broken agent/tool invocation
- broken status loop
- broken skill selection
- broken context pack
- broken artifact generation
- broken secrets visibility
- broken MCP access

### 13.2. Что он не чинит по умолчанию

Не его основная зона:
- продуктовая логика;
- бизнес-решения;
- дизайн;
- feature coding, если сама система работоспособна.

### 13.3. Его артефакты

Обязательно:
- `incident.md`
- `stability-report.md`
- prevention action
- updated operational note, если проблема повторяемая

## 14. Codex CLI operating model

### 14.1. Что хранить в `AGENTS.md`

Там должны жить:
- правила конкретного проекта;
- workflow-ограничения;
- источники истины;
- process gates;
- требования к языку ответов;
- branch/push/test policy;
- правила bugfix/diagnostics;
- требования к отчётам.

### 14.2. Что хранить в skills

В skills должны жить:
- узкие специализированные workflows;
- повторяемые runbooks;
- project-specific или domain-specific процедуры;
- правила для конкретных интеграций;
- шаблоны специализированных проверок.

### 14.3. Что хранить в foundation doc

В этом master-документе должны жить:
- универсальная ролевая модель;
- универсальная status model;
- универсальные требования к артефактам;
- universal handoff/reporting/bug/incident rules;
- схема Codex-autopilot как переносимого контура.

### 14.4. Что переносить в новый проект

В новый проект нужно переносить:
- локальную копию process-структуры;
- task model;
- templates;
- project-specific `AGENTS.md`;
- project-specific skills;
- ссылки на master foundation.

## 15. Skills policy

Каждый проект должен иметь документированную политику:
- какие skills обязательны;
- какие optional;
- какие experimental;
- кто владеет обновлением skill’ов;
- как skill versioning фиксируется;
- что делать, если skill сломан.

Если skill сломан:
- задача уходит в `system_blocked`;
- владелец = `Stability Engineer`.

## 16. Context pack policy

Каждый проект должен иметь способ быстро ввести агента в контекст.

Минимальный `context pack` должен содержать:
- product summary
- current status
- sources of truth
- task board summary
- current risks
- current active wave
- current blockers
- glossary if needed

Context pack:
- не заменяет документацию;
- он только входной пакет.

## 17. Reporting policy

### 17.1. Короткий статус

Для человека:
- что сделано;
- что не сделано;
- где блокер;
- кто владелец следующего шага.

### 17.2. Полный отчёт

Для автопилота:
- decisions
- self-analysis
- evidence
- risks
- handoff

### 17.3. Customer/owner report

Отдельно можно делать более короткий human-readable отчёт:
- completed
- in progress
- blocked
- incidents
- risks
- next actions

## 18. Acceptance criteria для самого автопилота

Автопилот считается настроенным, если по документам можно:

1. Завести новый проект без внешнего трекера.
2. Создать task card, dossier и board entry.
3. Прогнать feature через Analyst -> Lead -> QA -> TeamLead.
4. Завести bug и довести до закрытия.
5. Завести system incident и вернуть задачу из `system_blocked`.
6. Понять, кто владеет blocked/status.
7. Понять, где искать решение, а где искать operational note.

## 19. Готовый шаблон вопроса к ИИ про рамки

Используй такой запрос:

```text
Опиши рамки, в которых ты работаешь в этом проекте.

Нужно:
1. Какие у тебя источники истины.
2. Какие роли и этапы процесса ты предполагаешь.
3. Какие артефакты ты обязан оставлять после себя.
4. Какая у тебя status model.
5. Как у тебя устроен handoff между агентами.
6. Кто проверяет после QA.
7. Как обрабатываются blocked и system_blocked.
8. Кто отвечает за поломки автопилота, окружения и инструментов.
9. Какие решения тебе ещё нужны от меня, чтобы процесс стал decision-complete.

Ответ дай как структуру процесса, а не как общий совет.
```

## 20. Что читать и смотреть по теме

Если нужен общий образовательный контур, изучать в таком порядке:

1. Agentic workflow design
- handoff
- task decomposition
- artifact-driven execution

2. Incident management
- root cause analysis
- postmortem structure
- operational ownership

3. Software delivery governance
- review gates
- release readiness
- acceptance criteria

4. Documentation as operational system
- ADR
- source of truth
- runbooks
- playbooks

5. Quality systems
- QA as gate
- post-QA lead review
- regression evidence

## 21. Defaults

Если проект ещё не зафиксировал свои правила, по умолчанию использовать:
- Codex CLI как агентное ядро;
- файловый task tracking;
- обязательный dossier;
- обязательный self-analysis;
- обязательный TeamLead gate после QA;
- обязательный `Stability Engineer`;
- `board.csv` как machine source of truth.

## 22. Краткий итог

Этот документ задаёт не "как писать код", а:
- как строить агентную команду;
- как вести задачи;
- как не терять решения;
- как отделять product bugs от system incidents;
- как поддерживать сам автопилот в рабочем состоянии;
- как переносить эту схему в любой другой проект.
