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

    new_entry = f"""	{{
    	title: "{escape_ts_string(anime.title)}",
    	status: "{anime.status}",
    	rating: {anime.rating},
    	cover: "{escape_ts_string(anime.cover)}",
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