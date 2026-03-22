from fastapi import APIRouter

from app.schemas.friends import Friends
from app.utils.my_logger import logger
from app.services.github_friends import update_friends_ts
router = APIRouter(
    prefix="/friends",
    tags=["friends"],
    responses={404: {"description": "Not found"}}
)

@router.post("/add_friends")
async def add_friend(friend:Friends):
    logger.info("正在添加友链")
    try:
        update_friends_ts(friend)
        logger.info(f"友链添加成功{friend}")
    except Exception as e:
        logger.error(f"友链添加失败_{e}")
        raise