import json
from pathlib import Path
from typing import Any

from app.data.projects import ProjectCatalogItem

BASE_DIR = Path(__file__).resolve().parents[2]
PROJECTS_PATH = BASE_DIR / "data" / "projects.json"
PROJECT_REQUIRED_FIELDS = {"id", "title", "city", "size", "type", "description", "photos"}


def _ensure_storage_exists() -> None:
    PROJECTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not PROJECTS_PATH.exists():
        PROJECTS_PATH.write_text("[]", encoding="utf-8")


def _normalize_project_id(project_id: str | int) -> str:
    return str(project_id)


def _sanitize_photos(photos: list[str] | tuple[str, ...] | None) -> list[str]:
    return [str(photo).strip() for photo in photos or [] if str(photo).strip()]


def _project_from_dict(raw_project: dict[str, Any]) -> ProjectCatalogItem:
    return ProjectCatalogItem(
        id=raw_project["id"],
        title=str(raw_project["title"]).strip(),
        city=str(raw_project["city"]).strip(),
        size=str(raw_project["size"]).strip(),
        type=str(raw_project["type"]).strip(),
        description=str(raw_project["description"]).strip(),
        photos=tuple(_sanitize_photos(raw_project.get("photos"))),
    )


def _sanitize_project_payload(project: dict[str, Any]) -> dict[str, Any] | None:
    if not PROJECT_REQUIRED_FIELDS.issubset(project):
        return None

    return {
        "id": project["id"],
        "title": str(project["title"]).strip(),
        "city": str(project["city"]).strip(),
        "size": str(project["size"]).strip(),
        "type": str(project["type"]).strip(),
        "description": str(project["description"]).strip(),
        "photos": _sanitize_photos(project.get("photos")),
    }


def _find_project_index(payload: list[dict[str, Any]], project_id: str | int) -> int | None:
    normalized_id = _normalize_project_id(project_id)
    for index, item in enumerate(payload):
        if _normalize_project_id(item.get("id", "")) == normalized_id:
            return index
    return None


def load_projects() -> list[dict[str, Any]]:
    _ensure_storage_exists()

    raw_content = PROJECTS_PATH.read_text(encoding="utf-8").strip()
    if not raw_content:
        save_projects([])
        return []

    try:
        payload = json.loads(raw_content)
    except json.JSONDecodeError:
        save_projects([])
        return []

    if not isinstance(payload, list):
        save_projects([])
        return []

    valid_projects: list[dict[str, Any]] = []
    for item in payload:
        if not isinstance(item, dict):
            continue
        sanitized = _sanitize_project_payload(item)
        if sanitized is None:
            continue
        valid_projects.append(sanitized)

    if len(valid_projects) != len(payload):
        save_projects(valid_projects)

    return valid_projects


def save_projects(data: list[dict[str, Any]]) -> None:
    _ensure_storage_exists()
    with PROJECTS_PATH.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def get_all_projects() -> tuple[ProjectCatalogItem, ...]:
    return tuple(_project_from_dict(project) for project in load_projects())


def get_project_by_id(id: str | int) -> ProjectCatalogItem | None:
    normalized_id = _normalize_project_id(id)
    for project in get_all_projects():
        if _normalize_project_id(project.id) == normalized_id:
            return project
    return None


def add_project(project: dict[str, Any]) -> ProjectCatalogItem:
    payload = load_projects()
    numeric_ids = [item["id"] for item in payload if isinstance(item.get("id"), int)]
    next_id = max(numeric_ids, default=0) + 1

    new_project = _sanitize_project_payload(
        {
            "id": next_id,
            "title": project.get("title", ""),
            "city": project.get("city", ""),
            "size": project.get("size", ""),
            "type": project.get("type", project.get("project_type", "")),
            "description": project.get("description", ""),
            "photos": project.get("photos", []),
        }
    )
    if new_project is None:
        raise ValueError("Project payload is invalid")

    payload.append(new_project)
    save_projects(payload)
    return _project_from_dict(new_project)


def delete_project(id: str | int) -> ProjectCatalogItem | None:
    payload = load_projects()
    project_index = _find_project_index(payload, id)
    if project_index is None:
        return None

    project = payload.pop(project_index)
    save_projects(payload)
    return _project_from_dict(project)


def update_project(id: str | int, data: dict[str, Any]) -> ProjectCatalogItem | None:
    payload = load_projects()
    project_index = _find_project_index(payload, id)
    if project_index is None:
        return None

    project = dict(payload[project_index])
    for field, value in data.items():
        target_field = "type" if field == "project_type" else field
        if target_field not in PROJECT_REQUIRED_FIELDS or target_field == "id":
            continue
        if target_field == "photos":
            project[target_field] = _sanitize_photos(value)
        else:
            project[target_field] = str(value).strip()

    sanitized = _sanitize_project_payload(project)
    if sanitized is None:
        return None

    payload[project_index] = sanitized
    save_projects(payload)
    return _project_from_dict(sanitized)
