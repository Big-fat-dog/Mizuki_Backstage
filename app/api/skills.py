from fastapi import APIRouter

from app.schemas.skills import Skill
from app.utils.my_logger import logger
from app.services.github_skill import update_skills_ts
router = APIRouter(
    prefix="/skills",
    tags=["skills"],
    responses={404: {"description": "Not found"}}
)

@router.post("/add_skill")
async def add_skill(skill: Skill):
    logger.info("正在添加技能")
    try:
        update_skills_ts(skill)
        logger.info(f"技能添加成功{skill.name}")
    except Exception as e:
        logger.error(f"技能添加失败_{e}")
        raise