---
    title: 我的测试文章
    categories: 测试项目
    description: "这是文章描述"
    tags: ['tech', 'fastapi']
    draft: False
    published: 2026-03-17
    image: ./1.webp
    pinned: False
    licenseName: None
    ---

# APIROUTER的重要参数及含义🐧

`apirouter`对象是`fastapi`提供的一个让多文件进行接口合并的工具

具体写法如下

```py
from fastapi import APIRouter
router = APIRouter(
    prefix="/api/v1",      # 🔥 最重要：路由前缀
    tags=["users"],       # 🔥 API分组标签（Swagger文档用）
    dependencies=[],      # 全局依赖（如认证依赖）
    responses={404: {"description": "Not found"}}  # 统一响应模型
)
```

然后我们创建一个接口

```py
@router.get("/pdd")
async def fatdog():
    return {}
```

通过prefix的定义后，路由就会变成/api/v1/pdd

tags能让docs文档更加清晰

dependencies是路由组依赖（还有全局依赖和单一依赖！），在这个router接口创建的api都会执行这个依赖项