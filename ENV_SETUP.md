# 环境配置与启动指南

## 📋 一、环境文件说明

项目已配置两套环境：

### 开发环境 (.env.development)
```bash
VITE_APP_ENV=development
VITE_DB_PATH=/home/ecs-user/my_open_calender/data/dev.db
VITE_API_BASE_URL=http://localhost:3001/api
```

### 生产环境 (.env.production)
```bash
VITE_APP_ENV=production
VITE_DB_PATH=/home/ecs-user/my_open_calender/data/prod.db
VITE_API_BASE_URL=https://api.yourdomain.com/api
```

---

## 🚀 二、启动命令

### 前端开发服务器
```bash
# 开发环境
npm run dev

# 生产构建
npm run build
```

### 后端数据库服务
```bash
# 开发环境（使用 dev.db）
npm run db:dev

# 生产环境（使用 prod.db）
npm run db:prod

# 快捷方式
npm run server      # 等同于 db:dev
npm run server:prod # 等同于 db:prod
```

### 同时启动前后端
```bash
# 终端 1 - 启动数据库服务
npm run db:dev

# 终端 2 - 启动前端
npm run dev
```

---

## 📊 三、数据库文件位置

开发环境和生产环境的数据库完全隔离：

```
/home/ecs-user/my_open_calender/data/
├── dev.db    # 开发环境数据库
└── prod.db   # 生产环境数据库
```

---

## ⚙️ 四、API 接口

### 健康检查
```bash
curl http://localhost:3001/health
```

响应：
```json
{
  "status": "ok",
  "environment": "development",
  "database": "/home/ecs-user/my_open_calender/data/dev.db",
  "timestamp": "2026-03-14T02:15:00.000Z"
}
```

### 环境信息
```bash
curl http://localhost:3001/env
```

### 管理员 API
```bash
# 获取 AI 模型列表
curl http://localhost:3001/api/admin/models

# 切换 AI 模型
curl -X PUT http://localhost:3001/api/admin/models/1 \
  -H "Content-Type: application/json" \
  -d '{"is_active": true}'

# 获取系统设置
curl http://localhost:3001/api/admin/settings
```

---

## 🔐 五、管理员入口

### 访问方式
1. 进入家长页面
2. 点击顶部的"⚙️ 管理员后台"卡片
3. 进入管理面板

### 默认账号
- 用户名：`admin`
- 密码：`admin123`

⚠️ **重要：** 生产环境请修改默认密码！

---

## 📱 六、移动端适配

管理员页面已完全适配移动端：

- ✅ 响应式布局（< 768px 自动切换）
- ✅ 底部导航栏（移动端专属）
- ✅ 触摸友好的按钮尺寸
- ✅ 安全的底部间距（适配 iPhone 刘海屏）

---

## 🗄️ 七、数据库表结构

### 核心表
| 表名 | 说明 |
|------|------|
| users | 用户账号（家长/管理员） |
| children | 孩子信息 |
| points | 积分等级 |
| dinosaurs | 恐龙成长数据 |
| tasks | 学习任务 |
| wrong_questions | 错题本 |
| reading_records | 阅读记录 |

### 管理表
| 表名 | 说明 |
|------|------|
| ai_models | AI 模型配置 |
| settings | 系统设置 |

---

## 🔧 八、常见问题

### Q1: 如何切换环境？
```bash
# 开发环境
NODE_ENV=development npm run db:dev

# 生产环境
NODE_ENV=production npm run db:prod
```

### Q2: 数据库在哪里？
```
开发：/home/ecs-user/my_open_calender/data/dev.db
生产：/home/ecs-user/my_open_calender/data/prod.db
```

### Q3: 如何修改管理员密码？
直接编辑数据库：
```sql
UPDATE users SET password = '新密码' WHERE username = 'admin';
```

### Q4: 如何备份数据？
```bash
# 开发环境
cp data/dev.db data/dev.db.backup

# 生产环境
cp data/prod.db data/prod.db.backup.$(date +%Y%m%d)
```

---

**最后更新：** 2026-03-14 02:15
