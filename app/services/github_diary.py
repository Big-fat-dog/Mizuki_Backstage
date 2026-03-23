import re
from app.schemas.diary import Diary
from app.services.github_service import repo, branch_name
from app.utils.my_logger import logger


def get_diary_ts_content():
    """获取 diary.ts 文件内容"""
    try:
        content_file = repo.get_contents("src/data/diary.ts", ref=branch_name)
        return content_file
    except Exception as e:
        logger.error(f"获取 diary.ts 失败: {e}")
        raise


def extract_max_id(diary_content: str) -> int:
    """从现有日记中提取最大 ID"""
    id_pattern = r'id:\s*(\d+)'
    ids = [int(match) for match in re.findall(id_pattern, diary_content)]
    return max(ids) if ids else 0


def update_diary_ts(diary: Diary) -> None:
    """将新日记添加到 GitHub 的 diary.ts 文件末尾"""

    # 1. 获取当前内容
    old_content = get_diary_ts_content()
    current_content = old_content.decoded_content.decode("utf-8")

    # 2. 精准匹配整个文件结构
    pattern = r'^(.*?const diaryData: DiaryItem\[\] = \[\s*)(.*?)(\s*\];\s*)(.*)$'
    match = re.search(pattern, current_content, re.DOTALL)

    if not match:
        raise RuntimeError("未找到完整的 diary.ts 文件结构")

    # 3. 计算新 ID
    new_id = extract_max_id(current_content) + 1

    # 4. 构建新日记的 TS 对象（安全转义）
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

    # 构建 images 数组（如果存在）
    images_str = ""
    if diary.images:
        image_list = ", ".join(f'"{escape_ts_string(img)}"' for img in diary.images)
        images_str = f"\n\t\timages: [{image_list}],"

    new_entry = f"""	{{
		id: {new_id},
		content: "{escape_ts_string(diary.content)}",
		date: "{diary.date}",{images_str}
	}},"""

    # 5. 插入到数组末尾
    file_start = match.group(1)  # 包含 export interface...
    array_content = match.group(2)
    array_end = match.group(3)  # ];
    file_end = match.group(4)  # 包含所有函数和 export default...

    # 处理逗号
    if array_content.strip() and not array_content.rstrip().endswith(','):
        array_content = array_content.rstrip() + ','

    new_array_content = array_content + "\n" + new_entry

    # 6. 重组完整文件
    new_content = file_start + new_array_content + array_end + file_end

    # 7. 更新 GitHub 文件
    try:
        repo.update_file(
            path="src/data/diary.ts",
            message=f"feat: add diary - {new_id}",
            content=new_content,
            sha=old_content.sha,
            branch=branch_name
        )
        logger.info(f"✅ 成功添加日记: ID={new_id}")
    except Exception as e:
        logger.error(f"更新 diary.ts 失败: {e}")
        raise