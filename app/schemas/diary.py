from app.schemas.base import Base
from pydantic import Field
from typing import Optional, Annotated,List


class Diary(Base):
    id:int
    content: Annotated[str, Field(min_length=1, max_length=2000, description="日记内容")]
    date:Annotated[str,Field(description="日记时间 (ISO 8601)")]
    images:Annotated[Optional[List[str]],Field(default=[])]