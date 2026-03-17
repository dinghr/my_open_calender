# UI 调整最终指导 - 整合所有设计参考

**发送给 Claude 的开发指令**  
**日期：** 2026-03-12  
**优先级：** P0 - 立即执行  
**版本：** v2.0（整合版）

---

## 🎯 调整目标

综合参考 **背单词 APP** 和 **单词书 APP** 的设计优点，优化 AI 伴学小程序的前端 UI：

**参考 APP：**
1. 背单词 APP - 打卡天数、大按钮、底部导航
2. 单词书 APP - 卡片布局、数据展示、Tab 切换

**目标效果：**
- ✅ 清爽简洁，无压力（薄荷绿主题）
- ✅ 视觉层次清晰（卡片式布局）
- ✅ 交互友好（大按钮、Tab 切换）
- ✅ 可商用级别

---

## 📱 必须调整的核心元素

### 1. 底部导航栏 ⭐⭐⭐⭐⭐

**参考背单词 APP：**
```
📖      📺      ✨      🪐      😊
单词    课程    AI 学    发现    我的
```

**简化为 4 个 Tab：**
```
🏠        📋        📕        👨‍👩‍👧
首页      计划      错题      家长
```

**实现代码：**
```jsx
import { Home, Book, BookOpen, User } from 'lucide-react';

<nav className="bottom-nav">
  <div className="nav-item active">
    <Home size={24} strokeWidth={2} color="#667eea" />
    <span className="nav-label">首页</span>
  </div>
  <div className="nav-item">
    <Book size={24} strokeWidth={1.5} color="#999999" />
    <span className="nav-label">计划</span>
  </div>
  <div className="nav-item">
    <BookOpen size={24} strokeWidth={1.5} color="#999999" />
    <span className="nav-label">错题</span>
  </div>
  <div className="nav-item">
    <User size={24} strokeWidth={1.5} color="#999999" />
    <span className="nav-label">家长</span>
  </div>
</nav>
```

**CSS 样式：**
```css
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #FFFFFF;
  border-top: 1px solid #E0E0E0;
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  padding-bottom: max(8px, env(safe-area-inset-bottom));
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 60px;
  cursor: pointer;
}

.nav-label {
  font-size: 10px;
  color: #999999;
  font-weight: 500;
}

.nav-item.active .nav-label {
  color: #667eea;
  font-weight: 600;
}
```

---

### 2. 学科 Tab 切换 ⭐⭐⭐⭐⭐ 新增

**参考单词书 APP 的"单词书/短语"切换：**
```
单词书    短语
━━━━━
```

**应用到 AI 伴学小程序：**
```
语文    数学    英语
━━━━━
```

**实现代码：**
```jsx
<div className="subject-tabs">
  <button className="tab active">语文</button>
  <button className="tab">数学</button>
  <button className="tab">英语</button>
</div>
```

**CSS 样式：**
```css
.subject-tabs {
  display: flex;
  gap: 24px;
  padding: 16px;
  background: #FFFFFF;
  border-bottom: 1px solid #E0E0E0;
}

.tab {
  background: none;
  border: none;
  font-size: 16px;
  color: #999999;
  padding: 8px 0;
  position: relative;
  cursor: pointer;
  transition: color 0.2s;
}

.tab.active {
  color: #26D9AD;
  font-weight: 600;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 3px;
  background: #26D9AD;
  border-radius: 3px 3px 0 0;
}
```

**应用场景：**
- 每日任务页面（语文/数学切换）
- 错题本页面（语文/数学切换）
- 学习报告页面（语文/数学切换）

---

### 3. 打卡天数统计 ⭐⭐⭐⭐⭐ 新增

**参考背单词 APP：**
```
已坚持学习天数 💗
   114
```

**实现代码：**
```jsx
<div className="streak-counter">
  <div className="streak-label">已坚持学习天数 🌱</div>
  <div className="streak-number">12</div>
</div>
```

**CSS 样式：**
```css
.streak-counter {
  text-align: center;
  padding: 20px;
  background: linear-gradient(180deg, #E0F7FA 0%, #FFFFFF 100%);
  border-radius: 16px;
  margin: 16px;
}

.streak-label {
  font-size: 14px;
  color: #666666;
  margin-bottom: 8px;
}

.streak-number {
  font-size: 48px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

---

### 4. 学习进度卡片 ⭐⭐⭐⭐⭐ 新增

**参考单词书 APP：**
```
┌─────────────────────────────────┐
│ 正在学习              + 添加新书 │
│ ─────────────────────────────── │
│ [封面] 托福单词书                │
│        已完成：1740/3914 词      │
│        [████████░░░░░░░] 查看词表│
└─────────────────────────────────┘
```

**应用到 AI 伴学小程序：**
```jsx
<div className="learning-card">
  <div className="card-header">
    <h3 className="card-title">正在学习</h3>
    <button className="card-action">+ 添加计划</button>
  </div>
  
  <div className="card-content">
    <div className="book-info">
      <div className="book-cover">🌳</div>
      <div className="book-details">
        <div className="book-name">成长树 Level 5</div>
        <div className="book-progress">
          已完成：12/48 任务
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{width: '25%'}} />
        </div>
      </div>
      <button className="book-action">查看详情</button>
    </div>
  </div>
</div>
```

**CSS 样式：**
```css
.learning-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 16px;
  margin: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
}

.card-action {
  background: #E8F5E9;
  border: none;
  color: #26D9AD;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}
```

---

### 5. 每日任务卡片 ⭐⭐⭐⭐⭐ 新增

**参考单词书 APP：**
```
┌─────────────────────────────────┐
│ 每日任务量              📝 调整  │
│ ─────────────────────────────── │
│  新词：10      复习词：40       │
│                    复习词：1:4   │
└─────────────────────────────────┘
```

**应用到 AI 伴学小程序：**
```jsx
<div className="daily-task-card">
  <div className="card-header">
    <h3 className="card-title">每日任务量</h3>
    <button className="card-action">📝 调整</button>
  </div>
  
  <div className="task-stats">
    <div className="stat-item">
      <span className="stat-label">新任务</span>
      <span className="stat-value">4</span>
    </div>
    <div className="stat-item">
      <span className="stat-label">复习任务</span>
      <span className="stat-value">12</span>
    </div>
    <div className="stat-item">
      <span className="stat-label">复习比例</span>
      <span className="stat-value">1:3</span>
    </div>
  </div>
</div>
```

**CSS 样式：**
```css
.daily-task-card {
  background: #F7FAF9;
  border-radius: 12px;
  padding: 16px;
  margin: 16px;
}

.task-stats {
  display: flex;
  justify-content: space-around;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-label {
  font-size: 12px;
  color: #999999;
}

.stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #333333;
}
```

---

### 6. 进度条设计 ⭐⭐⭐⭐⭐

**参考两个 APP 的共同点：**
- 高度 8px（清晰可见）
- 渐变色填充
- 百分比显示
- 正向激励文案

**实现代码：**
```jsx
<div className="progress-container">
  <div className="progress-header">
    <span className="progress-label">今日任务进度</span>
    <span className="progress-percent">25%</span>
  </div>
  
  <div className="progress-bar">
    <div className="progress-fill" style={{ width: '25%' }} />
  </div>
  
  <div className="progress-footer">
    <span className="progress-completed">已完成 1/4</span>
    <span className="progress-status">进行中</span>
  </div>
</div>
```

**CSS 样式：**
```css
.progress-container {
  background: #FFFFFF;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  margin: 16px;
}

.progress-bar {
  height: 8px;
  background: #E0E0E0;
  border-radius: 4px;
  overflow: hidden;
  margin: 8px 0;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.progress-footer {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.progress-status {
  color: #26D9AD;
  font-weight: 600;
}
```

---

### 7. 大按钮设计 ⭐⭐⭐⭐⭐

**参考背单词 APP：**
```
┌──────────────────────────┐
│   → 开始学习             │
│        (大按钮)           │
└──────────────────────────┘
```

**实现代码：**
```jsx
<button className="action-button">
  <span className="button-icon">→</span>
  <span className="button-text">开始今日学习</span>
</button>
```

**CSS 样式：**
```css
.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: calc(100% - 32px);
  margin: 16px;
  padding: 16px 24px;
  background: linear-gradient(135deg, #26D9AD 0%, #20C997 100%);
  color: #FFFFFF;
  border: none;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(38, 217, 173, 0.3);
  transition: all 0.3s ease;
  min-height: 56px;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(38, 217, 173, 0.4);
}
```

---

### 8. 功能按钮统一设计 ⭐⭐⭐⭐⭐ 新增

**参考单词书 APP 的"添加新书"按钮：**
```
正在学习              + 添加新书
```

**设计特点：**
- ✅ 右上角操作入口
- ✅ 图标 + 文字
- ✅ 浅绿色背景
- ✅ 圆角 8px
- ✅ 点击区域适中

**统一所有功能按钮的设计：**

#### 8.1 卡片右上角操作按钮
```jsx
<div className="card-header">
  <h3 className="card-title">正在学习</h3>
  <button className="card-action">+ 添加计划</button>
</div>
```

```css
.card-action {
  background: #E8F5E9;
  border: none;
  color: #26D9AD;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-action:hover {
  background: #C8E6C9;
  transform: scale(1.05);
}
```

#### 8.2 统一按钮类型

**类型 A：卡片操作按钮（右上角）**
```css
/* 浅绿背景 + 深绿文字 */
.btn-card-action {
  background: #E8F5E9;
  color: #26D9AD;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
}

/* 使用场景：
- + 添加计划
- 📝 调整
- ⚙️ 设置
- 📋 词表
- 查看详情
*/
```

**类型 B：主按钮（大按钮）**
```css
/* 薄荷绿渐变 + 白色文字 */
.btn-primary {
  background: linear-gradient(135deg, #26D9AD 0%, #20C997 100%);
  color: #FFFFFF;
  padding: 16px 24px;
  border-radius: 16px;
  font-size: 18px;
  font-weight: 600;
  min-height: 56px;
  box-shadow: 0 4px 12px rgba(38, 217, 173, 0.3);
}

/* 使用场景：
- 开始今日学习
- 确认提交
- 下一步
*/
```

**类型 C：次要按钮**
```css
/* 白色背景 + 灰色边框 */
.btn-secondary {
  background: #FFFFFF;
  color: #666666;
  border: 1px solid #E0E0E0;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
}

/* 使用场景：
- 明天再做
- 取消
- 换一首
*/
```

**类型 D：快捷操作按钮（图标 + 文字）**
```css
/* 彩色背景 + 图标 */
.btn-quick {
  background: #E3F2FD; /* 根据功能变色 */
  color: #666666;
  padding: 16px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

/* 使用场景：
- 极速刷题
- 学习报告
- 重新学习
*/
```

#### 8.3 按钮使用规范

| 按钮类型 | 使用场景 | 尺寸 | 颜色 |
|---------|---------|------|------|
| **卡片操作** | 右上角小按钮 | 6x12px | 浅绿背景 |
| **主按钮** | 主要行动号召 | ≥56px 高 | 薄荷绿渐变 |
| **次要按钮** | 次要操作 | 12x20px | 白色边框 |
| **快捷操作** | 功能入口 | 48x48px 图标 | 彩色背景 |

#### 8.4 按钮文案规范

**卡片操作按钮：**
- ✅ "+ 添加计划"
- ✅ "📝 调整"
- ✅ "⚙️ 设置"
- ✅ "📋 词表"
- ✅ "查看详情"

**主按钮：**
- ✅ "开始今日学习"
- ✅ "继续成长之旅"
- ✅ "确认提交"

**次要按钮：**
- ✅ "明天再做"
- ✅ "换一首"
- ✅ "取消"

**快捷操作：**
- ✅ "极速刷题"
- ✅ "学习报告"
- ✅ "重新学习"

---

### 9. 出题页卡片式设计 ⭐⭐⭐⭐⭐ 新增

**参考 AI 学习详情页的卡片式设计：**

**页面结构：**
```
学科 Tab → 题目卡片 → 进度条
```

**题目卡片内容：**
```jsx
<div className="question-card">
  <div className="card-header">
    <h3>📝 题目 #1</h3>
    <span className="tag">数学</span>
  </div>
  
  <div className="question-content">
    <p>小明有 5 盒铅笔，每盒 12 支...</p>
  </div>
  
  <div className="options-grid">
    <button className="option">A. 17</button>
    <button className="option">B. 60</button>
    <button className="option">C. 50</button>
    <button className="option">D. 70</button>
  </div>
  
  <div className="card-actions">
    <button>💡 提示</button>
    <button>📝 草稿纸</button>
  </div>
  
  <div className="card-navigation">
    <button>← 上一题</button>
    <button className="primary">下一题 →</button>
  </div>
</div>
```

**CSS 样式：**
```css
.question-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 24px 20px;
  margin: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin: 20px 0;
}

.option {
  padding: 16px;
  background: #F7FAF9;
  border: 2px solid #E0E0E0;
  border-radius: 12px;
  text-align: left;
}

.option.selected {
  background: #E8F5E9;
  border-color: #26D9AD;
}
```

---

### 10. 错题页卡片式设计 ⭐⭐⭐⭐⭐ 新增

**参考 AI 学习详情页的卡片式设计：**

**页面结构：**
```
时间筛选 → 学科筛选 → 错题卡片列表
```

**错题卡片内容：**
```jsx
<div className="wrong-question-card">
  <div className="card-header">
    <h3>🔢 两位数乘法</h3>
    <span>3 天前</span>
  </div>
  
  <div className="card-divider" />
  
  <div className="question-content">
    <p>小明有 5 盒铅笔...</p>
  </div>
  
  <div className="answer-comparison">
    <div className="answer-row wrong">
      <span>你的答案：</span>
      <span>17</span>
      <span>❌</span>
    </div>
    <div className="answer-row correct">
      <span>正确答案：</span>
      <span>60</span>
      <span>✅</span>
    </div>
  </div>
  
  <div className="error-analysis">
    <div>错误原因：概念不清</div>
    <div>掌握程度：🔄 复习中</div>
  </div>
  
  <div className="card-actions">
    <button>📖 解析</button>
    <button>🔄 举一反三</button>
  </div>
  
  <div className="card-actions">
    <button className="success">✅ 已掌握</button>
    <button className="danger">🗑️ 删除</button>
  </div>
</div>
```

**CSS 样式：**
```css
.wrong-question-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 20px;
  margin: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.answer-comparison {
  background: #F7FAF9;
  border-radius: 12px;
  padding: 16px;
  margin: 16px 0;
}

.answer-row.wrong {
  border-bottom: 1px solid #E0E0E0;
}

.mastery-badge.mastered {
  background: #E8F5E9;
  color: #26D9AD;
}

.mastery-badge.reviewing {
  background: #FFF3E0;
  color: #FFB74D;
}
```

---

### 11. 功能快捷入口 ⭐⭐⭐⭐⭐

**参考单词书 APP：**
```
[📚]        [📊]        [🔄]
极速刷词   熟练度分布   重新学习
```

**应用到 AI 伴学小程序：**
```jsx
<div className="quick-actions">
  <button className="action-item">
    <div className="action-icon" style={{background: '#E3F2FD'}}>
      📚
    </div>
    <span className="action-label">极速刷题</span>
  </button>
  
  <button className="action-item">
    <div className="action-icon" style={{background: '#FFF3E0'}}>
      📊
    </div>
    <span className="action-label">学习报告</span>
  </button>
  
  <button className="action-item">
    <div className="action-icon" style={{background: '#FCE4EC'}}>
      🔄
    </div>
    <span className="action-label">重新学习</span>
  </button>
</div>
```

**CSS 样式：**
```css
.quick-actions {
  display: flex;
  justify-content: space-around;
  padding: 24px 16px;
  background: #FFFFFF;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  cursor: pointer;
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.action-label {
  font-size: 12px;
  color: #666666;
}
```

---

## 🎨 配色方案（整合版）

```css
:root {
  /* 背景渐变 - 薄荷绿主题 */
  --bg-gradient-start: #E0F7FA;
  --bg-gradient-end: #FFFFFF;
  
  /* 主色调 - 薄荷绿 */
  --primary: #26D9AD;
  --primary-hover: #20C997;
  --primary-light: #E8F5E9;
  
  /* 辅助色 - 紫色（保留品牌色） */
  --accent: #667eea;
  --accent-hover: #5a67d8;
  --accent-light: #F3E8FF;
  
  /* 文字色 */
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  
  /* 功能色 */
  --success: #48bb78;
  --warning: #ed8936;
  --error: #f56565;
  
  /* 边框和背景 */
  --border: #E0E0E0;
  --card-bg: #FFFFFF;
  --card-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
```

---

## 🎯 实施步骤（13 步，约 3 小时）

### 第 1 步：更新配色方案（10 分钟）
- [ ] 修改 CSS 变量
- [ ] 更新背景渐变
- [ ] 测试颜色对比度

### 第 2 步：添加学科 Tab 切换（15 分钟）
- [ ] 创建 Tab 组件
- [ ] 实现切换逻辑
- [ ] 添加选中状态动画

### 第 3 步：优化底部导航（15 分钟）
- [ ] 统一图标风格
- [ ] 简化为 4 个 Tab
- [ ] 优化选中状态
- [ ] 添加 iPhone X 适配

### 第 4 步：添加打卡统计（15 分钟）
- [ ] 创建打卡计数器组件
- [ ] 添加渐变背景
- [ ] 大数字展示

### 第 5 步：重构学习进度卡片（20 分钟）
- [ ] 卡片式布局
- [ ] 添加封面图
- [ ] 具体数字展示（12/48）
- [ ] 添加操作入口

### 第 6 步：重构每日任务卡片（20 分钟）
- [ ] 浅绿色背景
- [ ] 数据清晰展示
- [ ] 添加调整入口
- [ ] 比例显示

### 第 7 步：优化进度条（15 分钟）
- [ ] 加大高度（8px）
- [ ] 添加百分比显示
- [ ] 优化文案（正向激励）
- [ ] 添加动画过渡

### 第 8 步：统一功能按钮设计（20 分钟）
- [ ] 定义 4 种按钮类型
- [ ] 创建按钮组件
- [ ] 统一按钮样式
- [ ] 统一按钮文案
- [ ] 添加 hover/active 状态

### 第 9 步：重新设计主按钮（10 分钟）
- [ ] 加大按钮尺寸（≥56px）
- [ ] 使用薄荷绿渐变
- [ ] 添加箭头图标
- [ ] 优化 hover/active 状态

### 第 10 步：重新设计主按钮（10 分钟）
- [ ] 加大按钮尺寸（≥56px）
- [ ] 使用薄荷绿渐变
- [ ] 添加箭头图标
- [ ] 优化 hover/active 状态

### 第 11 步：添加功能快捷入口（15 分钟）
- [ ] 3 个彩色图标按钮
- [ ] 图标 + 文字
- [ ] 彩色背景区分

### 第 12 步：出题页卡片式设计（20 分钟）
- [ ] 题目卡片（圆角 16px）
- [ ] 选项网格（2x2）
- [ ] 功能按钮（提示、草稿纸）
- [ ] 导航按钮（上一题、下一题）
- [ ] 进度条展示

### 第 13 步：错题页卡片式设计（20 分钟）
- [ ] 错题卡片（圆角 16px）
- [ ] 答案对比（你的 vs 正确）
- [ ] 错误分析（原因 + 掌握度）
- [ ] 功能按钮（解析、举一反三、已掌握、删除）
- [ ] 统计信息

### 第 14 步：整体优化（15 分钟）
- [ ] 统一圆角规范
- [ ] 统一阴影规范
- [ ] 优化字体大小
- [ ] 优化间距
- [ ] 测试可访问性

**总计：** 约 150 分钟（2.5 小时）

---

## ✅ 验收标准

### 视觉验收
- [ ] 配色清爽，薄荷绿主题
- [ ] 图标风格统一（线性图标）
- [ ] 学科 Tab 清晰可见
- [ ] 卡片层次分明
- [ ] 进度条清晰（8px 高）
- [ ] 按钮足够大（≥56px）

### 交互验收
- [ ] Tab 切换流畅
- [ ] 所有按钮易点击
- [ ] hover/active 状态明显
- [ ] 动画流畅（transition）
- [ ] 底部导航切换流畅

### 文案验收
- [ ] 使用正向激励语言
- [ ] 无焦虑性表达（"进行中"）
- [ ] 数据具体化（12/48）
- [ ] 字体大小适合阅读

### 兼容性验收
- [ ] iOS Safari 正常
- [ ] Android Chrome 正常
- [ ] iPhone X 底部适配
- [ ] 横屏模式正常

---

## 📝 完整页面示例

```jsx
import React, { useState } from 'react';
import { Home, Book, BookOpen, User } from 'lucide-react';

export default function LearningAppHome() {
  const [activeTab, setActiveTab] = useState('home');
  const [subject, setSubject] = useState('chinese');
  const streakDays = 12;
  const progress = 25;
  
  return (
    <div className="app-container">
      {/* 学科 Tab 切换 */}
      <div className="subject-tabs">
        <button 
          className="tab active"
          onClick={() => setSubject('chinese')}
        >
          语文
        </button>
        <button 
          className="tab"
          onClick={() => setSubject('math')}
        >
          数学
        </button>
      </div>
      
      {/* 打卡统计 */}
      <div className="streak-counter">
        <div className="streak-label">已坚持学习天数 🌱</div>
        <div className="streak-number">{streakDays}</div>
      </div>
      
      {/* 成长树 */}
      <div className="growth-tree">
        <div className="tree-emoji">🌳</div>
        <div className="tree-level">Level 5 - 茁壮成长</div>
      </div>
      
      {/* 学习进度卡片 */}
      <div className="learning-card">
        <div className="card-header">
          <h3 className="card-title">正在学习</h3>
          <button className="card-action">+ 添加计划</button>
        </div>
        <div className="card-content">
          <div className="book-info">
            <div className="book-cover">🌳</div>
            <div className="book-details">
              <div className="book-name">成长树 Level 5</div>
              <div className="book-progress">
                已完成：12/48 任务
              </div>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: '25%' }} />
              </div>
            </div>
            <button className="book-action">查看详情</button>
          </div>
        </div>
      </div>
      
      {/* 每日任务卡片 */}
      <div className="daily-task-card">
        <div className="card-header">
          <h3 className="card-title">每日任务量</h3>
          <button className="card-action">📝 调整</button>
        </div>
        <div className="task-stats">
          <div className="stat-item">
            <span className="stat-label">新任务</span>
            <span className="stat-value">4</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">复习任务</span>
            <span className="stat-value">12</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">复习比例</span>
            <span className="stat-value">1:3</span>
          </div>
        </div>
      </div>
      
      {/* 功能快捷入口 */}
      <div className="quick-actions">
        <button className="action-item">
          <div className="action-icon" style={{background: '#E3F2FD'}}>
            📚
          </div>
          <span className="action-label">极速刷题</span>
        </button>
        <button className="action-item">
          <div className="action-icon" style={{background: '#FFF3E0'}}>
            📊
          </div>
          <span className="action-label">学习报告</span>
        </button>
        <button className="action-item">
          <div className="action-icon" style={{background: '#FCE4EC'}}>
            🔄
          </div>
          <span className="action-label">重新学习</span>
        </button>
      </div>
      
      {/* 主按钮 */}
      <button className="action-button">
        <span className="button-icon">→</span>
        <span className="button-text">开始今日学习</span>
      </button>
      
      {/* 底部导航 */}
      <nav className="bottom-nav">
        <div className="nav-item active" onClick={() => setActiveTab('home')}>
          <Home size={24} strokeWidth={2} color="#667eea" />
          <span className="nav-label">首页</span>
        </div>
        <div className="nav-item" onClick={() => setActiveTab('plan')}>
          <Book size={24} strokeWidth={1.5} color="#999999" />
          <span className="nav-label">计划</span>
        </div>
        <div className="nav-item" onClick={() => setActiveTab('wrong')}>
          <BookOpen size={24} strokeWidth={1.5} color="#999999" />
          <span className="nav-label">错题</span>
        </div>
        <div className="nav-item" onClick={() => setActiveTab('parent')}>
          <User size={24} strokeWidth={1.5} color="#999999" />
          <span className="nav-label">家长</span>
        </div>
      </nav>
    </div>
  );
}
```

---

## 🎨 设计资源

### 图标库
- **Lucide React:** https://lucide.dev
- **Heroicons:** https://heroicons.com
- **Feather Icons:** https://feathericons.com

### 配色工具
- **Coolors:** https://coolors.co
- **UI Gradients:** https://uigradients.com

### 灵感参考
- **背单词 APP 截图**（已提供）
- **单词书 APP 截图**（已提供）
- **Dribbble:** https://dribbble.com
- **Mobbin:** https://mobbin.com

---

## 📞 需要帮助？

**常见问题：**

Q: Tab 切换怎么做动画？
A: 使用 CSS transition，添加 `transition: all 0.2s`

Q: 图标库怎么安装？
A: `npm install lucide-react` 或 `npm install @heroicons/react`

Q: 渐变色怎么调？
A: 使用 CSS 变量，方便统一修改

Q: 卡片阴影太重怎么办？
A: 调整 `box-shadow` 的透明度，如 `rgba(0,0,0,0.08)`

---

**最后更新：** 2026-03-12  
**执行优先级：** P0 - 立即执行  
**预计时间：** 2.5 小时

**完成后请发送截图确认！** ✅
