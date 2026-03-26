import re
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.schemas.article import Frontmatter
from app.services.github_service import commit_md_to_github,get_all_md,delete_md
from typing import Annotated
from app.utils.my_logger import logger
router = APIRouter(
    prefix="/article",
    tags=["article"],
    responses={404: {"description": "Not found"}}
)
frontmatter_schema = Frontmatter.model_json_schema()

@router.post("/upload")
async def upload(frontmatter_json: Annotated[str,Form(alias="frontmatter",json_schema_extra={
                "example": {
                    "title": "我的文章",
                    "description": "这是描述",
                    "tags": ["tech", "astro"],
                    "published": "2026-03-17",
                    "draft": False,
                    "categories": "教程",
                    "pinned": True,
                    "licenseName": "MIT",
                    "image": "./1.webp"
                },
                "format": "json-string"
            })],slug:Annotated[str,Form(description="文件夹名称")],
        image:Annotated[list[UploadFile], File(multiple=True,media_type="multipart/form-data",description="Multiple files as UploadFile")]=[],
        md_file:UploadFile=File(...),
        cover:UploadFile=File(...)
                 ):
    pth = "/article/upload"
    frontmatter = Frontmatter.model_validate_json(frontmatter_json)
    logger.info(f"{pth}接口：收到请求{md_file.filename}，正在读取")
    front = f"""---
title: {frontmatter.title}
category: {frontmatter.category}
description: "{frontmatter.description}"
tags: {frontmatter.tags}
draft: {frontmatter.draft}
published: {frontmatter.published.isoformat() if frontmatter.published else "null"}
image: {frontmatter.image}
pinned: {frontmatter.pinned}
licenseName: {frontmatter.licenseName}
---\n\n"""
    if not slug:
        logger.info(f"{pth}接口：没有上传文件名")
        slug = f"post-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    else:
        # 🔥 关键：安全校验 slug！
        slug = slug.strip().lower()
        # 1. 只允许字母、数字、连字符
        if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$", slug):
            logger.error(f"{pth}接口：文件名错误！包含非法字符")
            raise HTTPException(
                status_code=400,
                detail="slug 只能包含小写字母、数字、连字符，且不能以连字符开头/结尾"
            )

        # 2. 长度限制
        if len(slug) < 3 or len(slug) > 60:
            logger.error(f"{pth}接口：文件名错误！长度错误")
            raise HTTPException(
                status_code=400,
                detail="slug 长度必须在 3-60 个字符之间"
            )
        # === 1. 校验并读取 Markdown ===
    logger.info(f"{pth}接口：开始处理文件")
    if not md_file.filename.endswith(".md"):
        logger.error(f"{pth}接口：拒绝非法文件{md_file.filename}")
        raise HTTPException(status_code=400, detail="正文必须是 .md 文件！")
    original_md = (await md_file.read()).decode("utf-8")
    new_md = front+original_md
    files_to_commit = {f"{slug}/index.md": new_md}
    if not cover.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
        logger.error(f"{pth}接口：{cover.filename}不规范！")
        raise HTTPException(status_code=400, detail="封面必须是图片文件 (.png, .jpg, .webp)!")
    cover_content = await cover.read()
    target_filename = "1.webp"
    target_path =f"{slug}/{target_filename}"
    # D. 存入字典
    files_to_commit[target_path] = cover_content
    for i in image:
        if not i.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
            logger.error(f"{pth}接口：{i.filename}，上传图片不规范")
            raise HTTPException(status_code=400, detail="必须是图片文件 (.png, .jpg, .webp)!")
        img = await i.read()
        target_path = f"{slug}/{i.filename}"
        files_to_commit[target_path] = img
    logger.info(f"{pth}接口：文件处理成功，开始上传至github")
    commit_md_to_github(files_to_commit)
    logger.info(f"{pth}接口：上传完毕")
    return {"msg":"success"}

@router.get("/get_all_articles")
async def get_all_articles():
    contents = get_all_md()
    return {
        "data": contents,
    }

@router.post("/delete_article")
async def delete_article(file_path):
    if file_path.startswith("src/content/posts"):
        delete_md(file_path)
    else:
        raise HTTPException(status_code=404)
    return {"msg":"success"}



