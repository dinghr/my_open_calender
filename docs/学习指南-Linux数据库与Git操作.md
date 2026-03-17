# 📚 学习指南 - Linux 数据库与 Git 操作

**更新时间：** 2026-03-18  
**适用对象：** 项目开发者/运维人员

---

## 第一部分：SQLite 数据库操作

### 1.1 查看数据库文件

```bash
# 进入项目目录
cd ~/my_open_calender

# 查看数据库文件
ls -lh data/

# 输出示例：
# total 456K
# -rw-r--r-- 1 ecs-user ecs-user 160K Mar 12 09:12 app.db
# -rw-r--r-- 1 ecs-user ecs-user 216K Mar 18 07:33 dev.db
# -rw-r--r-- 1 ecs-user ecs-user  60K Mar 14 02:18 development.db
```

**说明：**
- `ls -lh` - 以人类可读格式显示文件大小
- `.db` 文件就是 SQLite 数据库文件
- 文件大小会随数据增长而增大

---

### 1.2 使用 sqlite3 命令行工具

#### 进入交互模式

```bash
# 打开开发数据库
sqlite3 data/dev.db

# 打开生产数据库（需要权限）
sqlite3 data/prod.db
```

**进入后看到的提示：**
```
SQLite version 3.31.1 2020-01-27 19:55:54
Enter ".help" for usage hints.
sqlite>
```

#### 常用命令

```sql
-- 查看所有表
.tables

-- 查看表结构
.schema students
.schema users

-- 查看建表语句
.schema

-- 退出
.quit
```

**示例输出：**
```
sqlite> .tables
books               learning_records    students
growth_tree         login_codes         teacher_advices
invite_links        points_records      user_student_bindings
knowledge_points    question_bank       users
learning_plan       reading_records     vocabulary
wrong_questions     wish_list
```

---

### 1.3 执行 SQL 查询

#### SELECT 查询

```bash
# 一行命令查询（适合简单查询）
sqlite3 data/dev.db "SELECT * FROM students;"

# 格式化输出（列模式）
sqlite3 -header -column data/dev.db "SELECT * FROM students;"

# 输出示例：
# id           name  grade  birthday    created_at
# -----------  ----  -----  ----------  -------------------
# student-001  小明   3      2020-01-01  2026-03-18 07:33:45
# student-002  小红   5      2018-01-01  2026-03-18 07:33:45
```

#### 常用查询示例

```sql
-- 1. 查询所有学生
SELECT * FROM students;

-- 2. 查询特定年级的学生
SELECT * FROM students WHERE grade = 3;

-- 3. 查询学生姓名和年级
SELECT name, grade FROM students;

-- 4. 统计学生数量
SELECT COUNT(*) FROM students;

-- 5. 按年级分组统计
SELECT grade, COUNT(*) as count FROM students GROUP BY grade;

-- 6. 查询绑定关系（多表联查）
SELECT 
    s.name as student_name,
    u.nickname as parent_name,
    b.relation,
    b.status
FROM user_student_bindings b
JOIN students s ON b.student_id = s.id
JOIN users u ON b.user_id = u.id;

-- 7. 查询学生的学习记录
SELECT 
    s.name,
    lr.type,
    lr.subject,
    lr.status,
    lr.date
FROM learning_records lr
JOIN students s ON lr.student_id = s.id
WHERE s.id = 'student-001'
ORDER BY lr.date DESC
LIMIT 10;

-- 8. 查询积分排名
SELECT 
    s.name,
    SUM(pr.points) as total_points
FROM points_records pr
JOIN students s ON pr.student_id = s.id
GROUP BY s.id
ORDER BY total_points DESC;
```

---

### 1.4 执行数据操作

#### INSERT 插入数据

```sql
-- 插入新学生
INSERT INTO students (id, name, grade, birthday, created_at)
VALUES ('student-003', '小刚', 4, '2019-05-15', datetime('now'));

-- 插入新家长
INSERT INTO users (id, nickname, role, created_at)
VALUES ('parent-002', '测试妈妈', 'parent', datetime('now'));

-- 创建绑定关系
INSERT INTO user_student_bindings 
(id, user_id, student_id, relation, status, created_at)
VALUES 
('binding-002', 'parent-002', 'student-003', 'mother', 'approved', datetime('now'));
```

#### UPDATE 更新数据

```sql
-- 更新学生年级
UPDATE students SET grade = 4 WHERE id = 'student-001';

-- 更新绑定状态
UPDATE user_student_bindings 
SET status = 'approved', approved_at = datetime('now')
WHERE id = 'binding-001';

-- 增加积分
INSERT INTO points_records 
(id, student_id, points, source, description, created_at)
VALUES 
('points-001', 'student-001', 50, 'bonus', '奖励积分', datetime('now'));
```

#### DELETE 删除数据

```sql
-- 删除测试数据（谨慎使用！）
DELETE FROM students WHERE id = 'student-003';

-- 删除所有测试积分记录
DELETE FROM points_records WHERE source = 'bonus';
```

**⚠️ 警告：** 生产环境慎用 DELETE！建议先备份：
```bash
cp data/prod.db data/prod.db.backup.$(date +%Y%m%d)
```

---

### 1.5 实用技巧

#### 导出查询结果

```bash
# 导出为 CSV
sqlite3 -header -csv data/dev.db "SELECT * FROM students;" > students.csv

# 导出为 JSON（需要 jq）
sqlite3 -json data/dev.db "SELECT * FROM students;" | jq .

# 导出为 HTML
sqlite3 -html data/dev.db "SELECT * FROM students;" > students.html
```

#### 备份数据库

```bash
# 简单复制（推荐）
cp data/dev.db data/dev.db.backup

# 压缩备份
tar -czf data/dev.db.backup.$(date +%Y%m%d).tar.gz data/dev.db

# SQLite 内置备份
sqlite3 data/dev.db ".backup 'data/dev.db.backup'"
```

#### 恢复数据库

```bash
# 从备份恢复
cp data/dev.db.backup data/dev.db

# 从 SQL 文件恢复
sqlite3 data/dev.db < backup.sql
```

#### 查看数据库信息

```sql
-- 查看数据库大小
SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();

-- 查看表大小
SELECT 
    name,
    pgsize - unused as 'size',
    round(100.0 * (pgsize - unused) / total_size, 1) as '% of total'
FROM dbstat
JOIN (SELECT sum(pgsize) as total_size FROM dbstat)
ORDER BY size DESC;

-- 查看索引
SELECT name, tbl_name FROM sqlite_master WHERE type='index';
```

---

## 第二部分：Git 分支操作

### 2.1 查看分支

```bash
# 查看本地分支
git branch

# 输出示例：
# * dev
#   main
#   prod

# 查看所有分支（包括远程）
git branch -a

# 输出示例：
# * dev
#   main
#   prod
#   remotes/origin/dev
#   remotes/origin/main
#   remotes/origin/prod

# 查看分支详细信息
git branch -v

# 输出示例：
# * dev  43ffc34 feat: 添加生产环境部署配置
#   main 881d0d0 feat: 添加 dev/prod 环境分离配置
#   prod 43ffc34 feat: 添加生产环境部署配置
```

**说明：**
- `*` 表示当前所在分支
- `remotes/origin/` 表示远程分支
- 后面的数字是最近一次提交的哈希值

---

### 2.2 切换分支

```bash
# 切换到 dev 分支
git checkout dev

# 切换到 prod 分支
git checkout prod

# 切换到 main 分支
git checkout main

# 创建并切换到新分支
git checkout -b feature/new-feature
```

**⚠️ 注意：** 切换分支前确保当前工作区是干净的：
```bash
# 查看是否有未提交的修改
git status

# 如果有修改，可以：
# 1. 提交修改
git add -A && git commit -m "保存修改"

# 2. 或者暂存修改
git stash

# 切换分支后再恢复
git stash pop
```

---

### 2.3 查看分支历史

```bash
# 查看最近 5 次提交
git log --oneline -5

# 输出示例：
# 43ffc34 feat: 添加生产环境部署配置
# 881d0d0 feat: 添加 dev/prod 环境分离配置
# c8fcb46 feat: 完成 Phase 1 基础功能开发
# 58ed23f Initial commit

# 查看图形化历史
git log --oneline --graph --all -10

# 查看某个分支的历史
git log prod --oneline -5

# 查看两个分支的差异
git log dev..prod --oneline  # dev 有但 prod 没有的提交
git log prod..dev --oneline  # prod 有但 dev 没有的提交
```

---

### 2.4 分支合并

```bash
# 在 main 分支合并 dev
git checkout main
git merge dev

# 在 prod 分支合并 dev
git checkout prod
git merge dev

# 如果有冲突，解决后：
git add <冲突文件>
git commit -m "解决合并冲突"
```

---

### 2.5 推送分支到远程

```bash
# 推送当前分支
git push origin dev

# 推送所有分支
git push --all origin

# 查看远程仓库
git remote -v

# 输出示例：
# origin  https://github.com/dinghr/my_open_calender.git (fetch)
# origin  https://github.com/dinghr/my_open_calender.git (push)
```

---

## 第三部分：实战练习

### 练习 1：查看开发数据库

```bash
cd ~/my_open_calender

# 1. 查看数据库文件
ls -lh data/

# 2. 查看所有表
sqlite3 data/dev.db ".tables"

# 3. 查看学生数据
sqlite3 -header -column data/dev.db "SELECT * FROM students;"

# 4. 查看绑定关系
sqlite3 -header -column data/dev.db "
SELECT 
    s.name as student,
    u.nickname as parent,
    b.relation,
    b.status
FROM user_student_bindings b
JOIN students s ON b.student_id = s.id
JOIN users u ON b.user_id = u.id;
"
```

---

### 练习 2：Git 分支操作

```bash
cd ~/my_open_calender

# 1. 查看当前分支
git branch

# 2. 查看所有分支
git branch -a

# 3. 切换到 dev 分支
git checkout dev

# 4. 查看 dev 分支历史
git log --oneline -5

# 5. 切换到 prod 分支
git checkout prod

# 6. 查看 prod 分支历史
git log --oneline -5

# 7. 比较 dev 和 prod 的差异
git log dev..prod --oneline
git log prod..dev --oneline
```

---

### 练习 3：数据库查询实战

```bash
cd ~/my_open_calender

# 1. 统计有多少个学生
sqlite3 data/dev.db "SELECT COUNT(*) as student_count FROM students;"

# 2. 查看每个学生的积分
sqlite3 -header -column data/dev.db "
SELECT 
    s.name,
    SUM(pr.points) as total_points
FROM students s
LEFT JOIN points_records pr ON s.id = pr.student_id
GROUP BY s.id;
"

# 3. 查看学生的学习记录类型分布
sqlite3 -header -column data/dev.db "
SELECT 
    type,
    COUNT(*) as count
FROM learning_records
GROUP BY type;
"

# 4. 查看阅读记录
sqlite3 -header -column data/dev.db "
SELECT 
    s.name,
    b.title,
    rr.status,
    rr.progress
FROM reading_records rr
JOIN students s ON rr.student_id = s.id
JOIN books b ON rr.book_id = b.id;
"
```

---

## 第四部分：常见问题

### Q1: sqlite3 命令不存在？

```bash
# 安装 sqlite3
sudo apt update
sudo apt install -y sqlite3
```

---

### Q2: 数据库文件权限不足？

```bash
# 查看权限
ls -l data/dev.db

# 修改权限
chmod 644 data/dev.db

# 修改所有者
chown ecs-user:ecs-user data/dev.db
```

---

### Q3: Git 分支冲突怎么办？

```bash
# 1. 查看冲突文件
git status

# 2. 编辑冲突文件，解决冲突标记
# <<<<<<< HEAD
# 你的修改
# =======
# 对方的修改
# >>>>>>> dev

# 3. 标记为解决
git add <冲突文件>

# 4. 完成合并
git commit -m "解决合并冲突"
```

---

### Q4: 如何查看数据库修改历史？

SQLite 本身不记录修改历史，建议：
1. 使用 Git 管理数据库 schema 变更
2. 重要操作前备份数据库
3. 使用触发器记录审计日志

---

### Q5: 生产环境能直接操作数据库吗？

**不建议！** 应该：
1. 通过 API 接口操作
2. 如需直接操作，先备份
3. 在测试环境验证后再操作生产
4. 记录所有手动操作

---

## 第五部分：安全提示

### ⚠️ 数据库操作安全

1. **生产环境谨慎操作**
   - 操作前备份：`cp prod.db prod.db.backup`
   - 使用事务：`BEGIN; ... COMMIT;`
   - 先 SELECT 确认再 DELETE/UPDATE

2. **权限控制**
   - 数据库文件权限：644
   - 目录权限：755
   - 生产数据库限制访问用户

3. **敏感数据**
   - 不要明文存储密码
   - 不要直接暴露用户隐私
   - 日志中脱敏处理

---

### ⚠️ Git 操作安全

1. **不要提交敏感信息**
   - .env 文件
   - 密码、密钥
   - 数据库文件

2. **分支保护**
   - main/prod分支设置保护
   - 需要 Pull Request 合并
   - 需要 Code Review

3. **提交信息规范**
   - 使用有意义的提交信息
   - 遵循约定式提交规范

---

*完成本指南后，你应该能够：*
- ✅ 查看和查询 SQLite 数据库
- ✅ 执行基本的 SQL 操作
- ✅ 查看和切换 Git 分支
- ✅ 理解分支管理和合并
- ✅ 安全地操作数据库和代码

*下一步：阅读《安全配置学习指南》*
