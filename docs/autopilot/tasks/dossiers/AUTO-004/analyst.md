# Analyst Report

## Objective

Определить безопасный scope для запуска каталога реализованных проектов и конверсии пользователя в существующий FSM заявки.

## Inputs

- Пользовательский запрос.
- `AGENTS.md`.
- `docs/autopilot/sources-of-truth.md`.
- `AUTOPILOT-FOUNDATION.md`.
- `app/handlers/menu.py`.
- `app/handlers/project_configurator.py`.
- `main.py`.

## Decisions

- Каталог реализуется отдельными слоями `data`, `keyboards`, `handlers`.
- Текущий вход в раздел по кнопке `🏗 Реализованные проекты` не меняется.
- Для конверсии используется активный `ProjectFSM` из `app/handlers/project_configurator.py`, так как он подключён в корневом `main.py`.
- Переход из карточки проекта должен сохранять `selected_project` в `FSMContext`.
- Для сценария конверсии из каталога допускается отдельная точка входа внутрь существующего `ProjectFSM` с первым вопросом про имя.

## Work Performed

- Локализован активный entrypoint приложения в `main.py`.
- Подтверждено, что текущий placeholder раздела проектов находится в `app/handlers/menu.py`.
- Подтверждено, что dormant-flow в `app/fsm/handlers.py` не подключён текущим `main.py`.
- Зафиксирован архитектурный write scope и DoD.

## Self-Analysis

Вывод: формулировка `использовать существующие состояния` требует не создавать новую FSM. Гипотеза: допустимо расширить существующий `ProjectFSM` новым шагом для имени, если это не ломает текущий сценарий configurator.

## Risks

- Возможен конфликт handlers, если router каталога будет подключён после fallback из `menu.py`.
- В каталоге используются тестовые проекты без реальных `file_id`, поэтому ветка с `media_group` будет реализована, но не покрыта реальной отправкой.

## Handoff

Передать в `Backend Bot Engineer` для реализации каталога, подключения router и интеграции с активным `ProjectFSM`.
