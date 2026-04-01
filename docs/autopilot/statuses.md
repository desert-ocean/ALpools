# Status Model

## Основные статусы

- `todo`
- `analysis`
- `ready_for_lead`
- `ready_for_arch`
- `ready_for_impl`
- `in_progress`
- `ready_for_qa`
- `qa_review`
- `ready_for_lead_gate`
- `done`
- `canceled`

## Проблемные статусы

- `blocked`
- `system_blocked`
- `stability_fix`

## Разрешенные переходы

- `todo -> analysis`
- `analysis -> ready_for_lead`
- `ready_for_lead -> analysis`
- `ready_for_lead -> ready_for_arch`
- `ready_for_lead -> ready_for_impl`
- `ready_for_arch -> ready_for_impl`
- `ready_for_impl -> in_progress`
- `in_progress -> ready_for_qa`
- `ready_for_qa -> qa_review`
- `qa_review -> in_progress`
- `qa_review -> ready_for_lead_gate`
- `ready_for_lead_gate -> in_progress`
- `ready_for_lead_gate -> done`
- `any -> blocked`
- `any -> system_blocked`
- `system_blocked -> stability_fix`
- `stability_fix -> ready_for_impl`
- `stability_fix -> in_progress`
- `any -> canceled`
