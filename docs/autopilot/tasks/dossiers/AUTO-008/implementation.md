## Objective

Переименовать рабочий пункт расчёта в `Виртуальный конфигуратор` и удалить старый отдельный пункт-заглушку без изменения логики существующего расчётного flow.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-008.md`
- `docs/autopilot/tasks/dossiers/AUTO-008/analyst.md`
- `docs/autopilot/tasks/dossiers/AUTO-008/lead.md`
- `app/handlers/menu.py`
- `app/handlers/cost_handler.py`
- `main.py`

## Decisions

- Изменить только `app/handlers/menu.py`, поскольку именно там хранятся текст кнопок, состав reply-клавиатуры и заглушечные handlers.
- Сохранить имя константы `BTN_INDIVIDUAL_CALC`, чтобы не менять контракт между `menu.py` и `cost_handler.py`; меняется только отображаемый текст.
- Полностью удалить `BTN_POOL_TYPE` и его message-handler как мёртвый код.
- Удалить stub-handler `BTN_INDIVIDUAL_CALC` из `menu.py`, чтобы единственным owner пользовательского входа в расчёт остался `cost_handler`.

## Work Performed

- В `app/handlers/menu.py` обновлён текст `BTN_INDIVIDUAL_CALC` на `🧠 Виртуальный конфигуратор`.
- Из главного меню удалена кнопка `BTN_POOL_TYPE`.
- Из `app/handlers/menu.py` удалены константа `BTN_POOL_TYPE` и handler `choose_pool_type`, который возвращал заглушку `находится в разработке`.
- Из `app/handlers/menu.py` удалён handler `individual_calculation`, который возвращал заглушку для `BTN_INDIVIDUAL_CALC`.
- Сохранена существующая связка `cost_handler -> BTN_INDIVIDUAL_CALC`, поэтому расчётный flow запускается тем же handler без изменения FSM и бизнес-логики.

## Self-Analysis

- Вывод: переименование через существующую константу безопаснее, чем добавление новой, потому что не меняется импортный контракт.
- Не выполнялся живой e2e прогон через Telegram; функциональное подтверждение построено на анализе роутеров, поиске упоминаний и синтаксической проверке.

## Risks

- Логи `cost_handler` по-прежнему используют термин `Cost configurator`; это внутренние технические сообщения, не пользовательское поведение.
- Если пользователь ожидал удаления любых слов `configurator` из internal logs, это вне текущего scope.

## Handoff

Передать задачу `QA` для проверки отсутствия старого пункта, корректности точки входа в расчёт и чистоты поиска по коду.
