## Objective

Сформировать decision-complete задачу на обновление стартовой галереи `/start` до шести фото без поломки consultation flow и reply-меню.

## Inputs

- Пользовательский запрос в текущем треде
- `AGENTS.md`
- `docs/autopilot/sources-of-truth.md`
- `AUTOPILOT-FOUNDATION.md`
- `docs/autopilot/tasks/cards/AUTO-009.md`
- `app/handlers/menu.py`
- `app/data/welcome_media.py`
- `app/keyboards/start_kb.py`

## Decisions

- Завести отдельную задачу `AUTO-010`, а не переписывать артефакты закрытой `AUTO-009`, потому что acceptance `/start` изменился.
- Оставить write-scope в `app/data/welcome_media.py` и `app/handlers/menu.py`.
- Использовать локальные файлы из `app/data/photos/`.
- Принять ограничение Telegram как факт платформы: caption можно добавить в первый media item, но inline-клавиатуру к media group привязать нельзя.
- Сохранить inline-кнопку `📞 Получить консультацию` отдельным сообщением с тем же callback `go_consult`.

## Work Performed

- Проверены текущие `/start`-обработчики в репозитории.
- Подтверждено, что рабочий welcome-flow расположен в `app/handlers/menu.py`.
- Подтверждено наличие всех файлов `project1.jpg`-`project6.jpg` в `app/data/photos/`.
- Локализован конфликт между пользовательским требованием и ограничением Telegram Bot API на inline keyboard в media group.

## Self-Analysis

- Вывод: пользовательское требование про кнопку на первом элементе галереи не может быть выполнено буквально через штатный `sendMediaGroup`.
- Гипотеза: ближайшее безопасное поведение для продукта — альбом из шести фото с caption на первом элементе и отдельное сообщение только с inline-кнопкой.

## Risks

- Если владелец продукта требует именно inline-кнопку на самом сообщении альбома, понадобится пересмотр UX, а не только правка кода.
- Live rendering альбома и отдельной кнопки зависит от Telegram-клиента и требует ручного smoke test.

## Handoff

Передать задачу в `TeamLead` для подтверждения, что ограничение Telegram и выбранный workaround допустимы для текущего scope.
