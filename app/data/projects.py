from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProjectCatalogItem:
    id: str | int
    title: str
    city: str
    size: str
    type: str
    description: str
    photos: tuple[str, ...]
