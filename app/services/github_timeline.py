import re
from app.schemas.timeline import TimelineEvent
from app.services.github_service import repo, branch_name
from app.utils.my_logger import logger


def get_timeline_ts_content():
    """获取 timeline.ts 文件内容"""
    try:
        content_file = repo.get_contents("src/data/timeline.ts", ref=branch_name)
        return content_file
    except Exception as e:
        logger.error(f"获取 timeline.ts 失败: {e}")
        raise


def update_timeline_ts(event: TimelineEvent) -> None:
    """将新时间线事件添加到 GitHub 的 timeline.ts 文件末尾"""

    # 1. 获取当前内容
    old_content = get_timeline_ts_content()
    current_content = old_content.decoded_content.decode("utf-8")

    # 2. 精准匹配整个文件结构（关键！）
    pattern = r'^(.*?export const timelineData: TimelineItem\[\] = \[\s*)(.*?)(\s*\];\s*)(.*)$'
    match = re.search(pattern, current_content, re.DOTALL)

    if not match:
        raise RuntimeError("未找到完整的 timeline.ts 文件结构")

    # 3. 构建新时间线事件的 TS 对象（安全转义）
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

    # 构建可选字段
    optional_fields = ""

    # 字符串字段：允许空字符串，只跳过 None
    if event.location is not None:
        optional_fields += f'\n\t\tlocation: "{escape_ts_string(event.location)}",'
    if event.organization is not None:
        optional_fields += f'\n\t\torganization: "{escape_ts_string(event.organization)}",'
    if event.position is not None:
        optional_fields += f'\n\t\tposition: "{escape_ts_string(event.position)}",'

    # 日期字段
    if event.endDate is not None:
        optional_fields += f'\n\t\tendDate: "{event.endDate}",'

    # skills 数组（如果存在且非空）
    if event.skills:
        valid_skills = [s for s in event.skills if s.strip()]
        if valid_skills:
            skills_list = ", ".join(f'"{escape_ts_string(s)}"' for s in valid_skills)
            optional_fields += f"\n\t\tskills: [{skills_list}],"

    # achievements 数组（如果存在且非空）
    if event.achievements:
        valid_achievements = [a for a in event.achievements if a.strip()]
        if valid_achievements:
            achievements_list = ", ".join(f'"{escape_ts_string(a)}"' for a in valid_achievements)
            optional_fields += f"\n\t\tachievements: [{achievements_list}],"

    # links 数组（如果存在且非空）
    links_str = ""
    if event.links:
        links_entries = []
        for link in event.links:
            link_entry = f'{{ name: "{escape_ts_string(link.label)}", url: "{escape_ts_string(link.url)}", type: "{link.type}" }}'
            links_entries.append(link_entry)
        if links_entries:
            links_list = ",\n\t\t\t".join(links_entries)
            links_str = f"\n\t\tlinks: [\n\t\t\t{links_list}\n\t\t],"

    # icon 字段
    if event.icon is not None:
        optional_fields += f'\n\t\ticon: "{escape_ts_string(event.icon)}",'

    # color 字段
    if event.color is not None:
        optional_fields += f'\n\t\tcolor: "{event.color}",'

    # featured 字段（只有为 True 时才添加）
    if event.featured:
        optional_fields += f"\n\t\tfeatured: true,"

    new_entry = f"""	{{
		id: "{escape_ts_string(event.id)}",
		title: "{escape_ts_string(event.title)}",
		description: "{escape_ts_string(event.description)}",
		type: "{event.type}",
		startDate: "{event.startDate}",{optional_fields}{links_str}
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
            path="src/data/timeline.ts",
            message=f"feat: add timeline event - {event.title}",
            content=new_content,
            sha=old_content.sha,
            branch=branch_name
        )
        logger.info(f"✅ 成功添加时间线事件: {event.title} (ID={event.id})")
    except Exception as e:
        logger.error(f"更新 timeline.ts 失败: {e}")
        raise