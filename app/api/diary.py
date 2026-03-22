from fastapi import APIRouter
from app.schemas.diary import Diary
from app.utils.my_logger import logger
from app.services.github_diary import update_diary_ts
router = APIRouter(
    prefix="/diary",
    tags=["diary"],
    responses={404: {"description": "Not found"}}
)
@router.post("/add_diary")
async def add_diary(diary: Diary):
    logger.info(f"add diary: {diary.id}")
    try:
        update_diary_ts(diary)
        return {'msg':"success"}
    except Exception as e:
        logger.error(f"上传日记出错！——{e}")
        raise
