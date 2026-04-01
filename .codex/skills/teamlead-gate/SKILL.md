# TeamLead Gate

## Purpose

Выполнять контрольные gate после анализа, реализации и QA.

## Use When

- задача в `ready_for_lead`;
- задача в `ready_for_lead_gate`;
- нужно принять решение о запуске, возврате, блокировке или закрытии.

## Inputs

- dossier;
- task card;
- `docs/autopilot/task-flow.md`;
- `docs/autopilot/statuses.md`;
- `qa.md` при финальном gate.

## Workflow

1. Проверь полноту входных артефактов.
2. Проверь, нет ли скрытого scope creep.
3. Проверь, что решения соотносятся с источниками истины.
4. Проверь, что risks и self-analysis не формальны.
5. Прими решение по следующему статусу.

## Outputs

- `lead.md`;
- решение по статусу;
- уточненный handoff.
