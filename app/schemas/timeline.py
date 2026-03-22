from typing import List, Optional, Literal
from datetime import date
from pydantic import  Field, field_validator
import re
from app.schemas.base import Base
# 定义枚举类型
EventType = Literal["education", "work", "project", "achievement"]
LinkType = Literal["website", "github", "document", "video", "other"]


# 定义链接子模型
class EventLink(Base):
    label: str = Field(min_length=1, max_length=50, description="链接显示名称")
    url: str = Field(min_length=1, description="链接地址")
    type: LinkType = Field(default="website", description="链接类型")

    # 校验 URL 格式
    @field_validator('url', mode='before')
    @classmethod
    def validate_url_format(cls, v):
        if not v:
            raise ValueError("URL 不能为空")
        # 简单的协议头检查，或者使用 HttpUrl(v) 进行严格检查
        if not re.match(r"^https?://", v):
            raise ValueError(f"URL 必须以 http:// 或 https:// 开头，当前值：{v}")
        return v


class TimelineEvent(Base):
    # 1. ID: 必填，唯一标识
    id: str = Field(min_length=1, max_length=100, description="事件唯一标识符")

    # 2. 标题: 必填
    title: str = Field(min_length=1, max_length=200, description="事件标题")

    # 3. 描述: 必填，支持较长文本
    description: str = Field(min_length=1, max_length=2000, description="详细描述")

    # 4. 类型: 严格枚举
    type: EventType = Field(description="事件类型")

    # 5. 开始日期: 必填，自动解析 "YYYY-MM-DD"
    startDate: date = Field(description="开始日期")

    # 6. 结束日期: 可选。如果为 None 或空字符串，表示“至今”
    endDate: Optional[date] = Field(default=None, description="结束日期 (为空表示进行中)")

    # 7. 地点: 可选
    location: Optional[str] = Field(default=None, max_length=200, description="地点")

    # 8. 组织/机构: 可选
    organization: Optional[str] = Field(default=None, max_length=200, description="组织或机构名称")

    # 9. 职位/角色: 可选
    position: Optional[str] = Field(default=None, max_length=200, description="职位或角色")

    # 10. 技能列表: 可选，默认空列表
    skills: List[str] = Field(default_factory=list, description="相关技能列表")

    # 11. 成就列表: 可选，默认空列表
    achievements: List[str] = Field(default_factory=list, description="成就或成果列表")

    # 12. 链接列表: 可选，默认空列表，元素为 EventLink 对象
    links: List[EventLink] = Field(default_factory=list, description="相关链接")

    # 13. 图标: 可选，Iconify 格式
    icon: Optional[str] = Field(default=None, pattern=r"^[a-z0-9-]+:[a-z0-9-]+$", description="Iconify 图标")

    # 14. 颜色: 可选，Hex 格式
    color: Optional[str] = Field(default=None, pattern=r"^#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?$", description="主题颜色")

    # 15. 是否精选: 可选，默认 False
    featured: bool = Field(default=False, description="是否特色展示")