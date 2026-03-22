from fastapi import APIRouter

from app.schemas.timeline import TimelineEvent
from app.utils.my_logger import logger
from app.services.github_timeline import update_timeline_ts
router = APIRouter(
    prefix="/timeline",
    tags=["timeline"],
    responses={404: {"description": "Not found"}}
)

@router.post("/add_timeline")
async def add_skill(timeline: TimelineEvent):
    logger.info("正在添加技能")
    try:
        update_timeline_ts(timeline)
    except Exception as e:
        logger.error(f"技能添加失败_{e}")
        raise