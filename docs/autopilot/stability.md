# Stability And Incidents

## Что считать system incident

Это incident, если проблема ломает не продуктовую функцию, а сам контур выполнения работы:

- broken environment;
- broken skill;
- broken status loop;
- broken board/dossier structure;
- broken local tooling/run path;
- broken integration path.

## Владелец

Владелец system incident всегда `Stability Engineer`.

## Artifact incident

Минимальный состав:

- `incident_id`
- `title`
- `symptom`
- `trigger`
- `impacted_tasks`
- `owner`
- `diagnosis`
- `root_cause`
- `fix`
- `recovery_confirmation`
- `prevention_action`
