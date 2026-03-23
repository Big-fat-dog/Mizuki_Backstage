from fastapi import UploadFile
import uuid
import os
from pathlib import PurePosixPath
from app.services.github_service import repo,branch_name
import re
from app.utils.my_logger import logger
def get_anime_ts_content():
    """获取 anime.ts 文件内容"""
    try:
        content_file = repo.get_contents("src/data/anime.ts", ref=branch_name)
        return content_file
    except Exception as e:
        logger.error(f"获取 anime.ts 失败: {e}")
        raise


def update_anime_ts(anime) -> None:
    """直接修改 GitHub 上的 anime.ts 文件"""
    # 1. 获取当前内容
    old_content = get_anime_ts_content()
    current_content = get_anime_ts_content().decoded_content.decode("utf-8")

    # 2. 精准定位
    pattern = r'^(.*?const localAnimeList: AnimeItem\[\] = \[\s*)(.*?)(\s*\];\s*)(.*)$'
    match = re.search(pattern, current_content, re.DOTALL)

    if not match:
        raise RuntimeError("未找到完整的 anime.ts 结构")

    # 3. 构建新番剧的 TS 对象（安全转义）
    def escape_ts_string(s: str) -> str:
        """转义字符串为合法 TS 字符串"""
        return (
            s
            .replace('\\', '\\\\')  # 先转义反斜杠
            .replace('"', '\\"')
            .replace('\n', '\\n')
            .replace('\r', '\\r')
            .replace('\t', '\\t')
        )

    # 构建 genre 数组字符串
    genre_str = ", ".join(f'"{g}"' for g in anime.genre)
    mycover=f"/assets/anime/{anime.cover}"
    new_entry = f"""	{{
    	title: "{escape_ts_string(anime.title)}",
    	status: "{anime.status}",
    	rating: {anime.rating},
    	cover: "{escape_ts_string(mycover)}",
    	description: "{escape_ts_string(anime.description)}",
    	episodes: "{escape_ts_string(anime.episodes)}",
    	year: "{anime.year}",
    	genre: [{genre_str}],
    	studio: "{escape_ts_string(anime.studio)}",
    	link: "{escape_ts_string(anime.link)}",
    	progress: {anime.progress},
    	totalEpisodes: {anime.totalEpisodes},
    	startDate: "{anime.startDate}",
    	endDate: "{escape_ts_string(anime.endDate)}",
    }},"""
    #处理封面！

    # 4. 插入到数组末尾
    file_start = match.group(1)  # 包含 export type...
    array_content = match.group(2)
    array_end = match.group(3)  # ];
    file_end = match.group(4)  # 包含 export default...

    # 处理逗号
    if array_content.strip() and not array_content.rstrip().endswith(','):
        array_content = array_content.rstrip() + ','

    new_array_content = array_content + "\n" + new_entry

    # 5. 重组完整文件（关键！）
    new_content = file_start + new_array_content + array_end + file_end

    # 6. 更新 GitHub
    try:
        repo.update_file(
            path="src/data/anime.ts",
            message=f"feat: add anime - {anime.title}",
            content=new_content,
            sha=old_content.sha,
            branch=branch_name
        )
        logger.info(f"✅ 成功添加番剧: {anime.title}")
    except Exception as e:
        logger.error(f"处理番剧失败！{e}")


def sanitize_filename(filename: str) -> str:
    """
    安全化文件名：
    - 去掉路径（防 ../）
    - 中文/特殊字符 → 转成英文描述 or UUID
    - 统一小写
    - 保留合法扩展名
    """
    if not filename.strip():
        raise ValueError("文件名为空")

    # 1. 只取 basename（防路径穿越）
    safe_name = PurePosixPath(filename).name

    # 2. 分离扩展名
    stem, ext = os.path.splitext(safe_name)
    ext = ext.lower()

    # 3. 如果 stem 包含非 ASCII 字符（如中文），替换为描述+UUID
    if not re.match(r'^[a-zA-Z0-9._\- ]+$', stem):
        # 你可以自定义前缀，比如 "anime_cover"
        stem = f"anime_cover_{uuid.uuid4().hex[:8]}"

    # 4. 清理 stem：只保留字母数字和连字符
    stem = re.sub(r'[^a-zA-Z0-9]', '-', stem)
    stem = re.sub(r'-+', '-', stem).strip('-')

    return f"{stem}{ext}"

def add_cover(cover:UploadFile):
    if cover.filename.lower().strip() and cover.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
        logger.info(f"正在上传图片{cover}")
        original_name = cover.filename
        if not original_name:
            logger.error("文件名为空")
            raise ValueError("文件名为空")

        # 校验扩展名（小写）
        ext = os.path.splitext(original_name)[1].lower()
        if ext not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
            logger.error(f"不支持的文件格式: {ext}")
            raise ValueError(f"不支持的格式: {ext}")

        # 生成安全文件名
        safe_filename = sanitize_filename(original_name)
        logger.info(f"原文件名: {original_name} → 安全文件名: {safe_filename}")
        cover.file.seek(0)  # 确保从头读（防御性编程）
        content = cover.file.read()
        try:
            repo.create_file(
                path=f"public/assets/anime/{cover.filename}",
                content=content,
                message=f"feat: add anime cover - {cover.filename}",
                branch=branch_name
            )
            logger.info("成功添加！😋")
        except Exception as e:
            logger.error(f"添加失败——{e}")
            raise
    else:
        logger.error(f"输入文件格式不正确！")
        raise