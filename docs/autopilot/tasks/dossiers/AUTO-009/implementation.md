## Objective

Реализовать welcome-сценарий `/start` для рабочего menu-router с основным фото, фиксированным текстом, inline-кнопкой консультации и галереей `MediaGroup`, не ломая существующие handlers и reply-меню.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-009.md`
- `docs/autopilot/tasks/dossiers/AUTO-009/analyst.md`
- `app/handlers/menu.py`
- `app/data/photos/welcome.jpg`
- `app/data/photos/project1.jpg`
- `app/data/photos/project2.jpg`
- `app/data/photos/project3.jpg`

## Decisions

- Создать `app/data/welcome_media.py` как единый модуль со стартовым текстом и источниками изображений.
- Поддержать в data-модуле как локальные файлы, так и URL/file_id через единый resolver, чтобы реализация не была жестко привязана только к filesystem.
- Создать `app/keyboards/start_kb.py` с единственной inline-кнопкой `📞 Получить консультацию`.
- В `app/handlers/menu.py` добавить `send_welcome_sequence()` и переиспользовать существующий callback `go_consult`.
- Оставить existing reply keyboard отдельным сообщением после welcome-flow, чтобы сохранить текущую навигацию и существующие текстовые handlers.
- Добавить fallback на текстовый welcome без фото, если файловый asset отсутствует, чтобы бот не падал при missing media.

## Work Performed

- Добавлен модуль `app/data/welcome_media.py` с:
  - `WELCOME_TEXT` в точном виде из запроса;
  - `WELCOME_PHOTO_SOURCE`;
  - `WELCOME_GALLERY_SOURCES`;
  - helper-функциями для `FSInputFile` и `InputMediaPhoto`.
- Добавлен модуль `app/keyboards/start_kb.py` с inline-кнопкой `📞 Получить консультацию` и callback `go_consult`.
- Обновлен `app/handlers/menu.py`:
  - добавлен `logger`;
  - добавлена функция `send_welcome_sequence()`;
  - `/start` теперь отправляет основное фото с caption и inline-кнопкой;
  - затем отправляет `MediaGroup` без текста;
  - затем показывает существующее меню разделов отдельным сообщением.
- Осознанно не менялись `app/main.py` и `app/fsm/handlers.py`, чтобы не вмешиваться в отдельный FSM-flow черновика проекта.
- Выполнена локальная синтаксическая проверка командой `python -m py_compile app/handlers/menu.py app/data/welcome_media.py app/keyboards/start_kb.py main.py`.

## Self-Analysis

- Решение минимально-инвазивно: существующие callback-обработчики консультации, документы, контакты и fallback не менялись.
- Дополнительное сообщение `Разделы бота доступны ниже:` добавлено, потому что у `MediaGroup` нельзя повесить reply-клавиатуру, а без этого старт ломал бы доступ к существующему menu-driven UX.
- Runtime-поведение Telegram клиента не проверялось live; верификация ограничена код-ревью и синтаксической проверкой.

## Risks

- Если пользователь ожидает, что после `/start` будет только один message bubble, текущая реализация сознательно отправляет три шага: welcome-photo, gallery, меню.
- При запуске через альтернативный entrypoint `app/main.py` welcome-flow не задействован.

## Handoff

Передать задачу в `QA` на проверку точности текста, маршрутизации callback `go_consult`, состава `MediaGroup`, сохранения reply-меню и отсутствия синтаксических ошибок.
