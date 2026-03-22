from typing import Dict, Union
from github import Github, InputGitTreeElement
from app.core.config import settings
from app.utils.my_logger import logger
github_token = settings.GITHUB_TOKEN
repo_name = settings.REPO_NAME
branch_name = settings.BRANCH_NAME
content_path = settings.CONTENT_PATH
g = Github(github_token)
repo = g.get_repo(repo_name)
def commit_md_to_github(files:Dict[str, Union[bytes, str]]):
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

def get_all_md():
    #获取所有的博客文章文件夹
    contents= repo.get_contents("/src/content/posts")
    all_md = []
    try:
        for content in contents:
            all_md.append(content.path)
    except Exception as e:
        logger.error(f"出现错误{e}")
    return all_md

def delete_md(file_path):
    try:
        contents = repo.get_contents(file_path)
        if isinstance(contents,list):
            #如果是个目录
            logger.info(f"正在删除{file_path}里的内容,总共{len(contents)}个文件")
            for item in contents:
                if item.type == "dir":
                    delete_md(item.path)
                else:
                    #删除子文件
                    repo.delete_file(path=item.path,message=f"删除 {file_path.split('/')[-1]}",sha=item.sha)
                    logger.info(f"{item.path}删除成功")
            logger.info(f"目录{file_path}已经清空")
        else:
            #如果是个文件
            logger.info(f"{contents.path}正在被删除")
            repo.delete_file(path=file_path, message=f"删除 {file_path.split('/')[-1]}", sha=contents.sha)
            logger.info("删除成功")
    except Exception as e:
        logger.error(f"出错了！{e}")
        raise



