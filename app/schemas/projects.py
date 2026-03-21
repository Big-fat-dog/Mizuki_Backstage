from datetime import date

from app.schemas.base import Base
from pydantic import Field
from typing import Optional, Annotated, List, Literal


class Projects(Base):
    id: str = Field(min_length=1, max_length=50, description="项目唯一标识符")

    # 2. 标题: 限制长度
    title: Annotated[str, Field(min_length=1, max_length=100, description="项目名称")]

    # 3. 描述: 允许稍长，支持多行
    description: Annotated[str, Field(min_length=1, max_length=1000, description="项目简述")]

    # 4. 图片: 允许为空字符串。如果不为空，建议校验是否为合法 URL 或相对路径
    # 这里为了兼容 "" 和 "https://..."，使用自定义校验或宽松的正则
    image: str= Field(default="", description="项目封面图 (空字符串或 URL)")

    # 5. 分类: 可以使用 Literal 限制，或者保持 str 自由输入
    # 示例是 "web"，你可以预定义一些类别
    category: Literal["web" ,"mobile", "desktop" , "other"]

    # 6. 技术栈: 列表，自动去重并清理空白
    techStack: List[str] = Field(default_factory=list, description="使用的技术栈列表")

    # 7. 状态: 枚举值，确保数据规范
    status: Literal["completed" ,"in-progress" , "planned"] = Field(
        default="in-progress",
        description="项目状态"
    )

    # 8. 链接字段 (liveDemo, sourceCode, visitUrl)
    # 策略：允许空字符串。如果不为空，则必须是合法的 HTTP/HTTPS URL
    # Pydantic V2 的 HttpUrl 不允许空串，所以我们要用 Optional + 默认值="" 配合校验器
    liveDemo: Optional[str] = Field(default="", description="在线演示链接 (可选)")
    sourceCode: Optional[str] = Field(default="", description="源码仓库链接 (可选)")
    visitUrl: Optional[str] = Field(default="", description="前往项目链接 (可选)")

    # 9. 日期: 示例是 "2026-01-21" (YYYY-MM-DD)，直接用 date 类型自动解析
    startDate: date = Field(description="开始日期")
    endDate: Optional[date] = Field(default=None, description="结束日期 (可选，进行中可为空)")

    # 10. 是否精选
    featured: bool = Field(default=False, description="是否精选展示")

    # 11. 标签: 类似技术栈，但用于分类标记
    tags: List[str] = Field(default_factory=list, description="项目标签")