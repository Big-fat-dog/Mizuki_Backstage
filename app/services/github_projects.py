import re
from app.schemas.projects import Projects
from app.services.github_service import repo, branch_name
from app.utils.my_logger import logger


def get_projects_ts_content():
    """获取 projects.ts 文件内容"""
    try:
        content_file = repo.get_contents("src/data/projects.ts", ref=branch_name)
        return content_file
    except Exception as e:
        logger.error(f"获取 projects.ts 失败: {e}")
        raise


def update_projects_ts(project: Projects) -> None:
    """将新项目添加到 GitHub 的 projects.ts 文件末尾"""

    # 1. 获取当前内容
    old_content = get_projects_ts_content()
    current_content = old_content.decoded_content.decode("utf-8")

    # 2. 精准匹配整个文件结构
    pattern = r'^(.*?export const projectsData: Project\[\] = \[\s*)(.*?)(\s*\];\s*)(.*)$'
    match = re.search(pattern, current_content, re.DOTALL)

    if not match:
        raise RuntimeError("未找到完整的 projects.ts 文件结构")

    # 3. 构建新项目的 TS 对象（安全转义）
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

    # 构建 techStack 数组
    tech_stack_str = ", ".join(f'"{escape_ts_string(tech)}"' for tech in project.techStack)

    # 构建 tags 数组（如果存在）
    tags_str = ""
    if project.tags:
        tags_list = ", ".join(f'"{escape_ts_string(tag)}"' for tag in project.tags)
        tags_str = f"\n\t\ttags: [{tags_list}],"

    # 构建可选字段
    optional_fields = ""

    # liveDemo 字段
    if project.liveDemo:
        optional_fields += f'\n\t\tliveDemo: "{escape_ts_string(project.liveDemo)}",'

    # sourceCode 字段
    if project.sourceCode:
        optional_fields += f'\n\t\tsourceCode: "{escape_ts_string(project.sourceCode)}",'

    # visitUrl 字段
    if project.visitUrl:
        optional_fields += f'\n\t\tvisitUrl: "{escape_ts_string(project.visitUrl)}",'

    # endDate 字段
    if project.endDate:
        optional_fields += f'\n\t\tendDate: "{project.endDate}",'

    # featured 字段（只有为 True 时才添加）
    if project.featured:
        optional_fields += f"\n\t\tfeatured: true,"

    new_entry = f"""	{{
		id: "{escape_ts_string(project.id)}",
		title: "{escape_ts_string(project.title)}",
		description: "{escape_ts_string(project.description)}",
		image: "{escape_ts_string(project.image)}",
		category: "{project.category}",
		techStack: [{tech_stack_str}],
		status: "{project.status}"{optional_fields}{tags_str}
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
            path="src/data/projects.ts",
            message=f"feat: add project - {project.title}",
            content=new_content,
            sha=old_content.sha,
            branch=branch_name
        )
        logger.info(f"✅ 成功添加项目: {project.title} (ID={project.id})")
    except Exception as e:
        logger.error(f"更新 projects.ts 失败: {e}")
        raise