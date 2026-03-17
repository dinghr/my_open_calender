"""AI 助学小程序 - FastAPI 后端"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router

# 环境配置
ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true" if ENV == "development" else False

app = FastAPI(title="AI 助学小程序 API", version="0.2.0", debug=DEBUG)

# CORS - 允许前端访问
if ENV == "production":
    # 生产环境限制域名
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "https://yourdomain.com").split(",")
else:
    # 开发环境允许所有
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router)


@app.get("/")
def root():
    return {"message": "AI 助学小程序 API 运行中 🦞", "version": "0.2.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
