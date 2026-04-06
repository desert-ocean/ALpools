## Objective

Реализовать отправку всех шести фото в welcome-flow `/start` через `send_media_group`, сохранив caption на первом фото, consultation callback и reply-меню.

## Inputs

- `docs/autopilot/tasks/cards/AUTO-010.md`
- `docs/autopilot/tasks/dossiers/AUTO-010/analyst.md`
- `docs/autopilot/tasks/dossiers/AUTO-010/lead.md`
- `app/handlers/menu.py`
- `app/data/welcome_media.py`
- `app/keyboards/start_kb.py`

## Decisions

- Удалить зависимость от отдельного `welcome.jpg` в текущем `/start`.
- Сделать `WELCOME_GALLERY_SOURCES` единственным source of truth для welcome-альбома.
- Добавить `WELCOME_TEXT` как `caption` только к первому `InputMediaPhoto`.
- После отправки media group отправлять отдельное техническое сообщение с inline-кнопкой `📞 Получить консультацию`, используя существующий `get_welcome_keyboard()`.
- Сохранить отдельное reply-меню после welcome-flow без изменения остальных handlers.

## Work Performed

- В `app/data/welcome_media.py`:
  - расширен список `WELCOME_GALLERY_SOURCES` до `project1.jpg`-`project6.jpg`;
  - `build_welcome_media_group()` переведен на явную сборку списка `InputMediaPhoto`;
  - caption `WELCOME_TEXT` теперь назначается только первому элементу альбома.
- В `app/handlers/menu.py`:
  - удален вызов отдельного `answer_photo()` для `welcome.jpg`;
  - `send_welcome_sequence()` теперь отправляет один `answer_media_group()` из шести фото;
  - после альбома отправляется отдельное сообщение с inline-клавиатурой консультации;
  - fallback при отсутствии файла сохранен: бот отправит текст и кнопку вместо падения.
- Не менялись `go_consult`, reply-меню и остальные разделы `menu.py`.

## Self-Analysis

- Решение минимально меняет контракт welcome-flow и не трогает соседние маршруты.
- Требование про inline-кнопку на первом элементе альбома буквально невыполнимо средствами Telegram Bot API; реализован ближайший безопасный UX-вариант.
- Live-поведение в Telegram не проверялось, только код и локальная синтаксическая проверка.

## Risks

- Визуально кнопка будет отдельным сообщением под альбомом, а не частью первого media item.
- Если в будущем потребуется строго единый bubble с caption и кнопкой, придется менять продуктовый сценарий.

## Handoff

Передать задачу в `QA` на проверку состава альбома, caption первого фото, сохранения callback `go_consult`, reply-меню и локальной валидности Python-кода.
