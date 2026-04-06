from pathlib import Path

from aiogram.types import FSInputFile, InputMediaPhoto

WELCOME_TEXT = (
    "👋 Добро пожаловать в ALpools!\n"
    "Мы  инженерная компания с более чем 10-летним опытом в проектировании и реализации сложных технических систем.\n"
    "🏊 Бассейны  это отдельное направление нашей работы, в котором мы применяем накопленную экспертизу в гидравлике, водоподготовке, автоматизации и управлении.\n"
    "За годы работы мы реализовали проекты различного масштаба  от частных бассейнов до коммерческих объектов.\n"
    "🔧 Мы проектируем системы, которые работают годами без проблем.\n"
    "💡 В боте вы можете:\n"
    " рассчитать стоимость бассейна\n"
    " подобрать конфигурацию под свои задачи\n"
    " посмотреть реализованные проекты\n"
    "👇 Выберите, с чего начать:"
)

PHOTOS_DIR = Path(__file__).resolve().parent / "photos"

# Источник может быть локальным файлом, URL или Telegram file_id.
WELCOME_GALLERY_SOURCES: tuple[str | Path, ...] = (
    PHOTOS_DIR / "project1.jpg",
    PHOTOS_DIR / "project2.jpg",
    PHOTOS_DIR / "project3.jpg",
    PHOTOS_DIR / "project4.jpg",
    PHOTOS_DIR / "project5.jpg",
    PHOTOS_DIR / "project6.jpg",
)


def _resolve_photo_source(source: str | Path) -> str | FSInputFile:
    if isinstance(source, Path):
        if not source.exists():
            raise FileNotFoundError(source)
        return FSInputFile(source)
    return source


def build_welcome_media_group() -> list[InputMediaPhoto]:
    media_group: list[InputMediaPhoto] = []
    for index, source in enumerate(WELCOME_GALLERY_SOURCES):
        media_group.append(
            InputMediaPhoto(
                media=_resolve_photo_source(source),
                caption=WELCOME_TEXT if index == 0 else None,
            )
        )
    return media_group
