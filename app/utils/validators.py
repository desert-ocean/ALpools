import re

_DIMENSIONS_RE = re.compile(
    r"^\s*(?P<l>\d+(?:[\.,]\d+)?)\s*[xх*]\s*(?P<w>\d+(?:[\.,]\d+)?)\s*[xх*]\s*(?P<d>\d+(?:[\.,]\d+)?)\s*$",
    re.IGNORECASE,
)
_PHONE_RE = re.compile(r"^\+?[\d\s\-()]{7,20}$")
_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_dimensions(value: str) -> tuple[bool, str | None]:
    match = _DIMENSIONS_RE.match(value)
    if not match:
        return False, "Введите размеры в формате: 10x4x1.6"

    length = float(match.group("l").replace(",", "."))
    width = float(match.group("w").replace(",", "."))
    depth = float(match.group("d").replace(",", "."))

    if min(length, width, depth) <= 0:
        return False, "Размеры должны быть больше нуля."

    return True, None


def validate_phone(value: str) -> tuple[bool, str | None]:
    if not _PHONE_RE.fullmatch(value.strip()):
        return False, "Введите корректный номер телефона, например: +7 999 123-45-67"
    return True, None


def validate_email(value: str) -> tuple[bool, str | None]:
    if not _EMAIL_RE.fullmatch(value.strip()):
        return False, "Введите корректный email, например: name@example.com"
    return True, None