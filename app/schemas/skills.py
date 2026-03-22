from typing import List, Optional, Literal
from pydantic import Field, model_validator
from app.schemas.base import Base

# 定义枚举类型，确保数据规范
CategoryType = Literal["frontend", "backend", "database", "tools", "other"]
LevelType = Literal["beginner", "intermediate", "advanced", "expert"]


# 定义经验子模型
class Experience(Base):
    years: int = Field(ge=0, description="经验年数")
    months: int = Field(ge=0, le=11, description="经验月数 (0-11)")

    # 校验器：确保月份不会超过 11，如果超过建议在前端处理或这里自动进位
    @model_validator(mode='after')
    def normalize_experience(self):
        if self.months >= 12:
            # 自动进位：例如 1年 14个月 -> 2年 2个月
            extra_years = self.months // 12
            self.years += extra_years
            self.months = self.months % 12
        return self


class Skill(Base):
    # 1. ID: 必填，建议强制小写，防止 "React" 和 "react" 重复
    id: str = Field(min_length=1, max_length=50, description="技能唯一标识符 (建议小写)")

    # 2. 名称: 必填
    name: str = Field(min_length=1, max_length=100, description="技能显示名称")

    # 3. 描述: 必填，允许较长文本
    description: str = Field(min_length=1, max_length=1000, description="技能详细描述")

    # 4. 图标: 必填，示例是 "logos:apifox-icon"，可以加正则限制格式 (prefix:name)
    icon: str = Field(min_length=1, pattern=r"^[a-z0-9-]+:[a-z0-9-]+$",
                      description="Iconify 图标标识 (如 logos:apifox-icon)")

    # 5. 分类: 严格枚举
    category: CategoryType = Field(description="技能分类")

    # 6. 水平: 严格枚举
    level: LevelType = Field(description="技能掌握程度")

    # 7. 经验: 嵌套模型
    experience: Experience = Field(description="技能经验时长")

    # 8. 相关项目: 可选列表，默认为空列表方便前端遍历
    projects: List[str] = Field(default_factory=list, description="关联的项目ID列表")

    # 9. 证书: 可选列表
    certifications: List[str] = Field(default_factory=list, description="相关证书列表")

    # 10. 颜色: 可选，必须是合法的 Hex 颜色代码 (#RRGGBB 或 #RGB)
    color: Optional[str] = Field(default=None, pattern=r"^#[0-9A-Fa-f]{3}([0-9A-Fa-f]{3})?$",
                                 description="主题颜色 (Hex 格式)")