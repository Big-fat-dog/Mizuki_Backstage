from fastapi import FastAPI
from app.api import article,anime,diary,friends,projects,skills,timeline
from fastapi.middleware.cors import CORSMiddleware

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
    return {"message": "Hello World"}

