from fastapi import APIRouter

from app.schemas.projects import Projects
from app.utils.my_logger import logger
from app.services.github_projects import update_projects_ts
router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}}
)

@router.post("/add_projects")
async def add_project(project: Projects):
    logger.info("正在添加项目")
    try:
        update_projects_ts(project)
        logger.info(f"友链添加成功{project.title}")
    except Exception as e:
        logger.error(f"友链添加失败_{e}")
        raise