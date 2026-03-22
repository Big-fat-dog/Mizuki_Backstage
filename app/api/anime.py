from fastapi import APIRouter
from app.services.github_anime import update_anime_ts
from app.schemas.anime import Anime
from app.utils.my_logger import logger

router = APIRouter(
    prefix="/anime",
    tags=["anime"],
    responses={404: {"description": "Not found"}}
)

@router.post("add_anime")
async def add_anime(anime: Anime):
    logger.info(f"收到番剧请求 {anime.title}")
    update_anime_ts(anime)
    return {"msg": "success"}