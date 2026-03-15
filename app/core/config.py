from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    GITHUB_TOKEN:str
    REPO_NAME:str
    BRANCH_NAME:str="main"
    CONTENT_PATH:str="src/content/spec"

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # 不区分大小写
    )
settings = Settings()