from fastapi import FastAPI
from app.api import article
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发时用，生产环境限制域名
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(article.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

