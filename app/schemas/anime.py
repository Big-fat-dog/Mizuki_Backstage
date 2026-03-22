from app.schemas.base import Base
from pydantic import Field
from typing import Optional, Annotated, Literal, List


# 定义一个用于验证 "YYYY-MM" 格式的正则
DATE_PATTERN = r"(^\d{4}-\d{2}$|^$)"
class Anime(Base):
    title:Annotated[str,Field(min_length=1,max_length=30)]
    status:Annotated[Literal["watching","completed","planned"],Field(default="watching")]
    rating:Annotated[float,Field(ge=0,le=10)]
    cover:str
    description:str
    episodes:str
    year:str
    genre:List[str]
    studio:str
    link:str
    progress:int
    totalEpisodes:int
    startDate:Annotated[str, Field(pattern=DATE_PATTERN, description="开始日期 (YYYY-MM)")]
    endDate:Annotated[Optional[str], Field(pattern=DATE_PATTERN, default="", description="结束日期 (YYYY-MM)，空表示连载中")]