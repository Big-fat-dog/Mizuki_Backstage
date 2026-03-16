from typing import Dict, Union
from github import Github, InputGitTreeElement
from app.core.config import settings
from app.utils.my_logger import logger
def commit_md_to_github(files:Dict[str, Union[bytes, str]]):
    github_token=settings.GITHUB_TOKEN
    repo_name=settings.REPO_NAME
    branch_name=settings.BRANCH_NAME
    content_path=settings.CONTENT_PATH
    g=Github(github_token)
    repo=g.get_repo(repo_name)
    try:
        ref = repo.get_git_ref(f"heads/{branch_name}")
        latest_commit = repo.get_git_commit(ref.object.sha)
        base_tree = repo.get_git_tree(latest_commit.sha)
    except Exception as e:
        logger.error(f"获取分支 {branch_name} 失败: {e}")
        raise RuntimeError(f"无法访问分支 {branch_name}")
    # 3. 创建所有文件的 blob
    blobs = []
    for rel_path, content in files.items():
        # 构建 GitHub 上的完整路径
        full_path = f"{content_path}/{rel_path}".replace("\\", "/")  # 确保用 /

        if isinstance(content, str):
            # 文本文件：UTF-8 编码
            blob = repo.create_git_blob(content, "utf-8")
            mode = "100644"  # 普通文件
        else:
            # 二进制文件：转成十六进制字符串
            hex_content = content.hex()
            blob = repo.create_git_blob(hex_content, "utf-8")
            mode = "100644"

        element = InputGitTreeElement(
            path=full_path,
            mode="100644",  # 普通文件
            type="blob",  # 文件类型（blob = 文件，tree = 目录）
            sha=blob.sha  # 已创建的 blob 的 SHA
        )
        blobs.append(element)

    # 4. 创建新的 tree（基于旧 tree + 新文件）
    try:
        new_tree = repo.create_git_tree(blobs, base_tree)
    except Exception as e:
        logger.error(f"创建 Git Tree 失败: {e}")
        raise RuntimeError("无法创建文件树")

    # 5. 创建新 commit
    new_commit = repo.create_git_commit(
        message=f"feat: add article {list(files.keys())[0].split('/')[0]}",
        tree=new_tree,
        parents=[latest_commit]
    )

    # 6. 更新分支指向新 commit
    try:
        ref.edit(sha=new_commit.sha)
        logger.info(f"成功提交 {len(files)} 个文件到 {branch_name}")
    except Exception as e:
        logger.error(f"更新分支失败: {e}")
        raise RuntimeError("提交成功但分支未更新！")
