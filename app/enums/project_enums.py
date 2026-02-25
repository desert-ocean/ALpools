from enum import Enum


class ProjectStatus(str, Enum):
    draft = "draft"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class ProjectStep(str, Enum):
    start = "start"
    general_info = "general_info"
    geometry = "geometry"
    review = "review"
    completed = "completed"


class ProjectType(str, Enum):
    pool = "pool"
    fountain = "fountain"
    pond = "pond"