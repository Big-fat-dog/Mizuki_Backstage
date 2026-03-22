import re
from app.schemas.skills import Skill
from app.services.github_service import repo, branch_name
from app.utils.my_logger import logger


def get_skills_ts_content():
    """获取 skills.ts 文件内容"""
    try:
        content_file = repo.get_contents("src/data/skills.ts", ref=branch_name)
        return content_file
    except Exception as e:
        logger.error(f"获取 skills.ts 失败: {e}")
        raise


def update_skills_ts(skill: Skill) -> None:
    """将新技能添加到 GitHub 的 skills.ts 文件末尾"""

    # 1. 获取当前内容
    old_content = get_skills_ts_content()
    current_content = old_content.decoded_content.decode("utf-8")

    # 2. 精准匹配整个文件结构（关键！）
    pattern = r'^(.*?export const skillsData: Skill\[\] = \[\s*)(.*?)(\s*\];\s*)(.*)$'
    match = re.search(pattern, current_content, re.DOTALL)

    if not match:
        raise RuntimeError("未找到完整的 skills.ts 文件结构")

    # 3. 构建新技能的 TS 对象（安全转义）
    def escape_ts_string(s: str) -> str:
        """转义字符串为合法 TS 字符串"""
        return (
            s
            .replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\r', '\\r')
            .replace('\t', '\\t')
        )

    # 构建 experience 对象
    experience_str = f"{{ years: {skill.experience.years}, months: {skill.experience.months} }}"

    # 构建 projects 数组（如果存在且非空）
    projects_str = ""
    if skill.projects:
        # 过滤掉空字符串
        valid_projects = [p for p in skill.projects if p.strip()]
        if valid_projects:
            projects_list = ", ".join(f'"{escape_ts_string(p)}"' for p in valid_projects)
            projects_str = f"\n\t\tprojects: [{projects_list}],"

    # 构建 certifications 数组（如果存在且非空）
    certifications_str = ""
    if skill.certifications:
        valid_certs = [c for c in skill.certifications if c.strip()]
        if valid_certs:
            certs_list = ", ".join(f'"{escape_ts_string(c)}"' for c in valid_certs)
            certifications_str = f"\n\t\tcertifications: [{certs_list}],"

    # 构建 color 字段（如果存在）
    color_str = ""
    if skill.color:
        color_str = f'\n\t\tcolor: "{skill.color}",'

    new_entry = f"""	{{
		id: "{escape_ts_string(skill.id)}",
		name: "{escape_ts_string(skill.name)}",
		description: "{escape_ts_string(skill.description)}",
		icon: "{escape_ts_string(skill.icon)}",
		category: "{skill.category}",
		level: "{skill.level}",
		experience: {experience_str},{projects_str}{certifications_str}{color_str}
	}},"""

    # 5. 插入到数组末尾
    file_start = match.group(1)  # 包含 export interface...
    array_content = match.group(2)
    array_end = match.group(3)  # ];
    file_end = match.group(4)  # 包含所有函数...

    # 处理逗号
    if array_content.strip() and not array_content.rstrip().endswith(','):
        array_content = array_content.rstrip() + ','

    new_array_content = array_content + "\n" + new_entry

    # 6. 重组完整文件
    new_content = file_start + new_array_content + array_end + file_end

    # 7. 更新 GitHub 文件
    try:
        repo.update_file(
            path="src/data/skills.ts",
            message=f"feat: add skill - {skill.name}",
            content=new_content,
            sha=old_content.sha,
            branch=branch_name
        )
        logger.info(f"✅ 成功添加技能: {skill.name} (ID={skill.id})")
    except Exception as e:
        logger.error(f"更新 skills.ts 失败: {e}")
        raise