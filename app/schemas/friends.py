from app.schemas.base import Base
from pydantic import Field
from typing import Optional, Annotated, List
# 定义 URL 正则：必须以 http:// 或 https:// 开头
URL_PATTERN = r"^https?://.+"

class Friends(Base):
    id: int
    title:Annotated[str,Field(min_length=1,max_length=200)]
    imgurl:Annotated[str, Field(
        min_length=1,
        max_length=2000,
        pattern=URL_PATTERN,
        description="网站头像/封面链接 (需以 http/https 开头)"
    )]
    desc:Annotated[str,Field(min_length=1,max_length=200)]
    siteurl:Annotated[str, Field(
        min_length=1,
        max_length=200,
        pattern=URL_PATTERN,
        description="网站跳转链接 (需以 http/https 开头)"
    )]
    tags:Annotated[List[str], Field(
        default_factory=list,
        min_length=0,
        max_length=5,
        description="分类标签 (最多5个)"
    )]