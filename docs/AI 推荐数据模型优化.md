# AI 伴学小程序 - AI 推荐数据模型优化

**创建日期：** 2026-03-12  
**目标：** 确保所有数据可被 AI 高效读取，支持精准推荐

---

## 🎯 AI 推荐所需数据维度

### 推荐算法输入
```python
# 学生画像
student_profile = {
    "grade": 3,                    # 年级
    "age": 9,                      # 年龄
    "learning_style": "visual",    # 学习风格（视觉/听觉/动手）
    "weak_points": ["乘法", "古诗背诵"],  # 薄弱知识点
    "strong_points": ["加法", "识字"],    # 优势知识点
    "error_patterns": ["粗心", "概念不清"], # 错误模式
}

# 学习历史
learning_history = {
    "completed_questions": [...],   # 已完成题目
    "wrong_questions": [...],       # 错题记录
    "learning_time": {...},         # 学习时间分布
    "progress_trend": {...},        # 进步趋势
}

# 上下文
context = {
    "date": "2026-03-12",
    "time_of_day": "evening",
    "days_since_last_review": 3,
    "upcoming_exam": False,
    "parent_adjustments": [...],    # 家长调整倾向
}
```

### 推荐算法输出
```python
recommendation = {
    "questions": [...],             # 推荐题目列表
    "reason": "基于错题举一反三",    # 推荐理由
    "priority": "high",             # 优先级
    "estimated_time": 15,           # 预计用时（分钟）
    "difficulty_match": 0.85,       # 难度匹配度
}
```

---

## 📊 数据表 AI 优化清单

### ✅ 已优化的表

#### 1. students - 学生表
**AI 用途：** 构建学生画像

| 字段 | AI 用途 |
|-----|--------|
| grade | 推荐对应年级的题目 |
| birthday | 计算年龄，推荐适龄内容 |
| created_at | 计算使用时长，判断新老用户 |

**建议新增：**
```python
# 学习风格（可选，家长填写）
learning_style = Column(String(20))  # visual, auditory, kinesthetic

# 学习目标（可选，家长填写）
learning_goals = Column(JSON)  # ["提高计算速度", "加强古诗背诵"]

# 特殊需求（可选）
special_needs = Column(JSON)  # {"dyslexia": False, "adhd": False}
```

---

#### 2. question_bank - 题库表 ⭐ 核心
**AI 用途：** 题目特征提取，匹配推荐

| 字段 | AI 用途 | 优化建议 |
|-----|--------|---------|
| subject | 学科分类 | ✅ 已枚举 |
| grade | 年级匹配 | ✅ |
| unit | 单元关联 | ✅ |
| knowledge_point | 知识点标签 | ⚠️ 建议改为 JSON 数组 |
| question_type | 题型分类 | ✅ 已枚举 |
| content | 题目内容 | ⚠️ 需结构化 |
| difficulty | 难度匹配 | ✅ |
| error_rate | 易错度筛选 | ✅ |

**优化建议：**

```python
# 知识点标签改为数组，支持多标签
knowledge_points = Column(JSON)  # ["两位数乘法", "进位", "应用题"]

# 题目内容结构化
content = Column(JSON)  # {
                        #   "text": "题目文本",
                        #   "options": ["A", "B", "C", "D"],  # 选择题
                        #   "images": ["url1", "url2"],       # 图片
                        #   "audio": "url",                    # 音频（语文）
                        #   "video": "url"                     # 视频
                        # }

# 答案结构化
answer = Column(JSON)  # {
                       #   "answer": "A",
                       #   "answer_text": "60 支",
                       #   "explanation": "5×12=60",
                       #   "steps": ["步骤 1", "步骤 2"]
                       # }

# 解析结构化
analysis = Column(JSON)  # {
                         #   "knowledge_analysis": "考查两位数乘法",
                         #   "common_mistakes": ["容易用加法", "忘记进位"],
                         #   "solving_strategy": "先理解题意，确定运算方法",
                         #   "extension": "可以扩展为除法题"
                         # }

# 新增：AI 分析特征（用于推荐）
ai_features = Column(JSON)  # {
                            #   "skills": ["乘法运算", "理解题意"],
                            #   "cognitive_level": "application",  # 认知层次
                            #   "estimated_time_seconds": 120,
                            #   "similarity_vector": [...]  # 向量嵌入（未来）
                            # }
```

---

#### 3. wrong_questions - 错题表 ⭐ 核心
**AI 用途：** 薄弱点分析，举一反三

| 字段 | AI 用途 | 优化建议 |
|-----|--------|---------|
| wrong_reason | 错误模式分析 | ✅ 已枚举 |
| mastered | 掌握度追踪 | ✅ |
| review_count | 复习频率 | ✅ |
| similar_questions | 举一反三 | ✅ |

**优化建议：**

```python
# 新增：错误详细分析
error_analysis = Column(JSON)  # {
                               #   "error_type": "calculation",  # 错误类型
                               #   "error_step": 2,              # 第几步出错
                               #   "misconception": "混淆加法和乘法",
                               #   "suggested_review": ["乘法概念", "应用题理解"]
                               # }

# 新增：掌握度评分
mastery_score = Column(Float)  # 0-1，AI 计算的掌握度

# 新增：推荐优先级
recommendation_priority = Column(Float)  # 0-1，AI 计算的推荐优先级

# 优化：相似题生成策略
similar_strategy = Column(JSON)  # {
                                 #   "strategy": "vary_numbers",  # 变式策略
                                 #   "params": {"operator": "same", "numbers": "different"},
                                 #   "generated_questions": [...]
                                 # }
```

---

#### 4. learning_records - 学习记录表
**AI 用途：** 学习行为分析

**优化建议：**

```python
# 新增：用时
time_spent_seconds = Column(Integer)  # 答题用时（秒）

# 新增：尝试次数
attempt_count = Column(Integer, default=1)  # 尝试次数

# 新增：AI 评分
ai_score = Column(Float)  # AI 评分（0-100）

# 新增：行为数据
behavior_data = Column(JSON)  # {
                              #   "hints_used": 2,          # 使用提示次数
                              #   "paused_count": 3,        # 暂停次数
                              #   "edited_count": 1,        # 修改答案次数
                              #   "confidence": "medium"    # 学生自信度
                              # }
```

---

#### 5. vocabulary - 生字库
**AI 用途：** 识字量分析，分级阅读推荐

**优化建议：**

```python
# 新增：字频数据
frequency_rank = Column(Integer)  # 常用字排名（1-3500）

# 新增：部首笔画
radical = Column(String(20))      # 部首
stroke_count = Column(Integer)    # 笔画数

# 新增：组词示例
word_examples = Column(JSON)      # ["学生", "学习", "学校"]

# 新增：AI 分析
ai_features = Column(JSON)        # {
                                  #   "difficulty": 2,
                                  #   "similarity_to_known": 0.8,
                                  #   "recommended_context": "在学校场景中"
                                  # }
```

---

#### 6. poetry_memory - 古诗记忆
**AI 用途：** 记忆曲线追踪，复习提醒

**优化建议：**

```python
# 新增：古诗元数据
poetry_metadata = Column(JSON)  # {
                                #   "dynasty": "唐",
                                #   "author": "李白",
                                #   "lines": 4,
                                #   "characters": 20,
                                #   "theme": "思乡",
                                #   "difficulty": 2
                                # }

# 优化：记忆强度计算
memory_strength = Column(Float)  # 使用艾宾浩斯曲线计算

# 新增：复习历史
review_history = Column(JSON)    # [
                                 #   {"date": "2026-03-10", "result": "correct"},
                                 #   {"date": "2026-03-08", "result": "wrong"}
                                 # ]
```

---

#### 7. growth_tree - 成长树
**AI 用途：** 激励机制，学习动力分析

**优化建议：**

```python
# 新增：成就记录
achievements = Column(JSON)  # [
                             #   {"id": "first_7_days", "unlocked_at": "..."},
                             #   {"id": "math_master", "unlocked_at": "..."}
                             # ]

# 新增：学习 streak
streak_days = Column(Integer, default=0)  # 连续学习天数

# 新增：动力分析
motivation_analysis = Column(JSON)  # {
                                    #   "trend": "increasing",
                                    #   "best_time": "evening",
                                    #   "preferred_subject": "math"
                                    # }
```

---

#### 8. knowledge_points - 知识点表
**AI 用途：** 知识图谱构建，依赖关系分析

**优化建议：**

```python
# 新增：前置知识点
prerequisites = Column(JSON)  # ["加法", "乘法概念"]

# 新增：后续知识点
next_steps = Column(JSON)     # ["除法", "混合运算"]

# 新增：知识图谱向量
knowledge_vector = Column(JSON)  # 知识图谱嵌入向量（用于相似度计算）

# 新增：常见错误模式
common_error_patterns = Column(JSON)  # [
                                      #   {"pattern": "看错符号", "frequency": 0.3},
                                      #   {"pattern": "忘记进位", "frequency": 0.5}
                                      # ]
```

---

## 🧠 AI 推荐算法数据结构

### 推荐请求格式
```python
class RecommendationRequest:
    student_id: str
    context: {
        "date": str,
        "time_of_day": str,
        "available_time_minutes": int,
        "parent_adjustments": list,
    }
    preferences: {
        "subjects": list,           # ["chinese", "math"]
        "exclude_topics": list,     # 排除的主题
        "focus_areas": list,        # 重点加强的领域
    }
```

### 推荐结果格式
```python
class RecommendationResult:
    questions: list[{
        "question_id": str,
        "type": str,                # "daily_question", "review", "similar"
        "subject": str,
        "knowledge_points": list,
        "difficulty": int,
        "estimated_time": int,
        "reason": str,              # 推荐理由
        "priority": float,          # 0-1
    }]
    daily_plan: {
        "chinese": {...},
        "math": {...},
        "estimated_total_time": int,
    }
    review_reminders: list[{
        "type": str,                # "poetry", "vocabulary", "wrong_question"
        "content_id": str,
        "urgency": float,           # 0-1
        "last_reviewed": str,
    }]
```

---

## 📈 AI 特征工程

### 学生特征向量
```python
student_features = {
    # 基础特征
    "grade": 3,
    "age_months": 108,
    "usage_days": 30,
    
    # 学科能力
    "chinese_level": 0.75,      # 0-1
    "math_level": 0.60,
    
    # 知识点掌握
    "knowledge_mastery": {
        "乘法": 0.8,
        "古诗": 0.5,
        "识字": 0.9,
    },
    
    # 学习习惯
    "avg_daily_time": 25,       # 分钟
    "completion_rate": 0.85,
    "preferred_time": "evening",
    
    # 错误模式
    "error_patterns": {
        "careless": 0.3,
        "concept_unclear": 0.5,
        "method_wrong": 0.2,
    },
    
    # 进步趋势
    "trend_7days": 0.15,        # 近 7 天进步率
    "trend_30days": 0.35,
}
```

### 题目特征向量
```python
question_features = {
    # 基础特征
    "subject": "math",
    "grade": 3,
    "difficulty": 2,
    "error_rate": 0.45,
    
    # 知识点
    "knowledge_points": ["两位数乘法", "进位"],
    "knowledge_difficulty": 0.6,
    
    # 题型
    "question_type": "application",
    "has_image": False,
    "has_options": False,
    
    # 认知层次
    "cognitive_level": "application",  # recall, understand, apply, analyze
    
    # 语义向量（未来）
    "embedding_vector": [0.1, 0.2, ...],  # 512 维向量
}
```

---

## 🔧 数据库索引优化

### 推荐查询高频字段

```sql
-- 学生相关查询
CREATE INDEX idx_student_grade ON students(grade);
CREATE INDEX idx_student_created ON students(created_at);

-- 题库查询
CREATE INDEX idx_question_subject_grade ON question_bank(subject, grade);
CREATE INDEX idx_question_knowledge ON question_bank(knowledge_point);
CREATE INDEX idx_question_difficulty ON question_bank(difficulty);
CREATE INDEX idx_question_error_rate ON question_bank(error_rate);
CREATE INDEX idx_question_status ON question_bank(status);

-- 错题查询
CREATE INDEX idx_wrong_student ON wrong_questions(student_id);
CREATE INDEX idx_wrong_mastered ON wrong_questions(mastered);
CREATE INDEX idx_wrong_reason ON wrong_questions(wrong_reason);
CREATE INDEX idx_wrong_date ON wrong_questions(wrong_date);

-- 学习记录查询
CREATE INDEX idx_learning_student_date ON learning_records(student_id, date);
CREATE INDEX idx_learning_type ON learning_records(type);

-- 古诗记忆查询
CREATE INDEX idx_poetry_student ON poetry_memory(student_id);
CREATE INDEX idx_poetry_next_review ON poetry_memory(next_review_at);
CREATE INDEX idx_poetry_status ON poetry_memory(status);

-- 生字查询
CREATE INDEX idx_vocabulary_student ON vocabulary(student_id);
CREATE INDEX idx_vocabulary_status ON vocabulary(status);
```

---

## 📝 实施建议

### 阶段一：立即优化
1. ✅ 添加知识点 JSON 数组字段
2. ✅ 结构化 content/answer/analysis
3. ✅ 添加 AI 特征字段
4. ✅ 创建高频查询索引

### 阶段二：数据积累
1. ⬜ 开始收集学习行为数据
2. ⬜ 积累题目作答统计
3. ⬜ 建立学生进步趋势

### 阶段三：AI 模型
1. ⬜ 训练题目难度预测模型
2. ⬜ 训练学生能力评估模型
3. ⬜ 实现个性化推荐算法
4. ⬜ 生成题目/学生向量嵌入

---

## 🎯 推荐场景示例

### 场景 1：每日一题推荐
```
输入：学生 ID + 日期 + 可用时间
处理：
1. 查询学生年级、学科进度
2. 查询近期错题（薄弱点）
3. 查询课程进度（同步学习）
4. 查询记忆曲线（需复习的古诗/生字）
5. AI 综合评分，选择最优题目
输出：语文 1 题 + 数学 1 题 + 推荐理由
```

### 场景 2：举一反三推荐
```
输入：错题 ID
处理：
1. 分析错题原因
2. 提取知识点
3. 题库中搜索相似题（知识点相同，数字/场景不同）
4. 按难度递进排序
输出：3-5 道相似题，由易到难
```

### 场景 3：复习提醒
```
输入：学生 ID + 日期
处理：
1. 查询古诗记忆曲线（next_review_at <= 今日）
2. 查询生字复习（review_count < 3 且 last_reviewed > 7 天前）
3. 查询错题复习（mastered = false 且 wrong_date > 3 天前）
输出：复习清单，按优先级排序
```

---

*文档创建：2026-03-12*
