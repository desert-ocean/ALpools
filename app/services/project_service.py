from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.project import Project
from app.enums.project_enums import ProjectStatus, ProjectStep


class ProjectNotFoundError(ValueError):
    pass


class ProjectService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_draft(self, user_id: int) -> Project:
        project = Project(user_id=user_id, status=ProjectStatus.draft, current_step=ProjectStep.start)
        self.session.add(project)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def get_active_project(self, user_id: int) -> Project | None:
        stmt = (
            select(Project)
            .where(
                Project.user_id == user_id,
                Project.status == ProjectStatus.draft,
                Project.is_deleted.is_(False),
            )
            .order_by(Project.created_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, project_id: UUID) -> Project:
        stmt = select(Project).where(Project.id == project_id, Project.is_deleted.is_(False))
        result = await self.session.execute(stmt)
        project = result.scalar_one_or_none()
        if project is None:
            raise ProjectNotFoundError(f"Project {project_id} not found")
        return project

    async def update_field(self, project_id: UUID, field: str, value: object) -> Project:
        project = await self.get_by_id(project_id)
        if not hasattr(project, field):
            raise ValueError(f"Unknown field: {field}")
        setattr(project, field, value)
        project.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def update_many(self, project_id: UUID, values: dict[str, object]) -> Project:
        project = await self.get_by_id(project_id)
        for field, value in values.items():
            if not hasattr(project, field):
                raise ValueError(f"Unknown field: {field}")
            setattr(project, field, value)
        project.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def set_step(self, project_id: UUID, step: ProjectStep) -> Project:
        project = await self.get_by_id(project_id)
        project.current_step = step
        project.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def set_status(self, project_id: UUID, status: ProjectStatus) -> Project:
        project = await self.get_by_id(project_id)
        project.status = status
        project.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(project)
        return project

    async def soft_delete(self, project_id: UUID) -> Project:
        project = await self.get_by_id(project_id)
        project.is_deleted = True
        project.status = ProjectStatus.cancelled
        project.updated_at = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(project)
        return project
