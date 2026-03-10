"""AI 助学小程序 - FastAPI 后端"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI 助学小程序 API", version="0.1.0")

# CORS - 允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境，生产环境要限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI 助学小程序 API 运行中 🦞", "version": "0.1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

# TODO: 添加计划表 API
# TODO: 添加错题本 API
# TODO: 添加出题 API

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
