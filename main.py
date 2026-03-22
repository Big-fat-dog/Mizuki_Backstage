from fastapi import FastAPI
from app.api import article,anime,diary,friends,projects,skills
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发时用，生产环境限制域名
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(article.router)
app.include_router(anime.router)
app.include_router(diary.router)
app.include_router(friends.router)

app.include_router(projects.router)

app.include_router(skills.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

