from fastapi import FastAPI
from app.api import article,anime,diary,friends,projects,skills,timeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import webbrowser
import threading
import uvicorn
import time
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发时用，生产环境限制域名
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(article.router,prefix="/api")
app.include_router(anime.router,prefix="/api")
app.include_router(diary.router,prefix="/api")
app.include_router(friends.router,prefix="/api")

app.include_router(projects.router,prefix="/api")

app.include_router(skills.router,prefix="/api")
app.include_router(timeline.router,prefix="/api")



@app.get("/")
async def root():
    return FileResponse("main.html")


def open_browser():
    """
    在另一个线程中等待服务器启动，然后打开浏览器
    """
    # 等待 1.5 秒，确保 uvicorn 已经启动并监听端口
    time.sleep(1.5)

    # 打开本地地址
    # 注意：这里访问的是 http://127.0.0.1:8000，而不是直接打开 file://...
    # 这样前端才能通过 fetch/axios 请求到你的后端 API
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    print("🚀 正在启动服务并打开前端页面...")

    # 启动一个线程专门负责打开浏览器，避免阻塞主程序
    threading.Thread(target=open_browser, daemon=True).start()

    # 启动 FastAPI 服务
    # host="127.0.0.1" 保证安全，port=8000 是默认端口
    uvicorn.run(app, host="127.0.0.1", port=8000)