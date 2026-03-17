from app.schemas.base import Base
from typing import Annotated, Optional, List
from datetime import date
from pydantic import Field
class Frontmatter(Base):
    title:Annotated[str,Field()]
    description:Annotated[str,Field()]
    published:Annotated[Optional[date],Field(default_factory=date.today)]#利用default_factory会在实例化时调用后面的函数，而default是创建类就调用！
    draft:Annotated[Optional[bool],Field(default=False,description="是否为草稿")]#是否为草稿
    tags:Annotated[Optional[List[str]],Field()]
    categories:Annotated[Optional[str],Field()]
    pinned:Annotated[Optional[bool],Field(default=False)]
    licenseName:Annotated[Optional[str],Field(default=None)]
    image:Annotated[Optional[str],Field(default="./1.webp")]
if __name__ == "__main__":
    print(Frontmatter.model_json_schema())