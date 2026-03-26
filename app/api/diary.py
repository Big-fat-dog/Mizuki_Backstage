from fastapi import APIRouter, UploadFile, File
from app.schemas.diary import Diary
from app.utils.my_logger import logger
from app.services.github_diary import update_diary_ts,add_diary_image
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
@router.post("/add_diary_cover")
async def add_cover(cover: UploadFile=File(...)):
    logger.info(f"收到日记请求 cover {cover.filename}")
    add_diary_image(cover)
    return {"msg": "success"}