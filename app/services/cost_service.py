import re
from typing import Any

_DIMENSIONS_RE = re.compile(
    r"^\s*(?P<l>\d+(?:[\.,]\d+)?)\s*[xх*]\s*(?P<w>\d+(?:[\.,]\d+)?)\s*[xх*]\s*(?P<d>\d+(?:[\.,]\d+)?)\s*$",
    re.IGNORECASE,
)


def build_cost_payload(answers: dict[str, Any]) -> dict[str, Any]:
    payload = dict(answers)
    dimensions = str(payload.get("dimensions", "")).strip()
    match = _DIMENSIONS_RE.match(dimensions)

    if not match:
        payload["volume"] = None
        return payload

    length = float(match.group("l").replace(",", "."))
    width = float(match.group("w").replace(",", "."))
    depth = float(match.group("d").replace(",", "."))

    payload["volume"] = round(length * width * depth, 2)
    return payload
