# AI 助学小程序 🎓

一个面向家长和孩子的智能学习计划工具。

## 核心功能

- 📅 **智能计划表** - 每日/每周/每月计划，自然语言调整
- 💬 **通知解析** - QQ 群老师通知自动提取任务
- 📝 **每日出题** - 语数英 + 错题 + 拓展，针对性练习
- 📸 **错题本** - 拍照上传，AI 分析讲解
- 👨‍👩‍👧 **家长辅助** - 知识点解析 + 讲解话术

## 技术栈

| 模块 | 技术 |
|------|------|
| 前端 | Vue 3 + TypeScript + Vite |
| UI | Naive UI |
| 后端 | Python FastAPI |
| 数据库 | SQLite → PostgreSQL |
| AI | 通义千问 API |

## 开发状态

🚧 MVP 开发中...

## 本地开发

```bash
# 前端
cd frontend && npm install && npm run dev

# 后端
cd backend && pip install -r requirements.txt && uvicorn main:app --reload
```

## 学习路径

本项目同时是一个学习项目，帮助开发者掌握：
- Vue 3 前端开发
- FastAPI 后端开发
- 全栈项目实践
