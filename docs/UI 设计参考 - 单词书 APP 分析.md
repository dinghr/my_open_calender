# UI 设计参考 - 单词书 APP 书桌页面分析

**创建日期：** 2026-03-12  
**来源：** 用户提供的单词书 APP 截图（书桌页面）

---

## 📱 界面分析

### 整体风格
- **配色：** 薄荷绿 + 浅灰色，清爽简洁
- **布局：** 卡片式分组，信息层次清晰
- **风格：** 工具化、高效、无压力

---

## 🎨 核心设计元素分析

### 1. 顶部标签切换 ⭐⭐⭐⭐

```
单词书    短语
━━━━━
```

**特点：**
- 简洁的 Tab 切换
- 选中状态用下划线 + 颜色标识
- 未选中状态灰色

**可借鉴：**
```jsx
<div className="tab-bar">
  <button className="tab active">单词书</button>
  <button className="tab">短语</button>
</div>
```

```css
.tab-bar {
  display: flex;
  gap: 24px;
  padding: 16px;
  background: #FFFFFF;
}

.tab {
  background: none;
  border: none;
  font-size: 16px;
  color: #999999;
  padding: 8px 0;
  position: relative;
}

.tab.active {
  color: #26D9AD;
  font-weight: 600;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: #26D9AD;
  border-radius: 3px 3px 0 0;
}
```

---

### 2. 学习进度卡片 ⭐⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│ 正在学习              + 添加新书 │
│ ─────────────────────────────── │
│ [封面] 托福单词书                │
│        已完成：1740/3914 词      │
│        [████████░░░░░░░] 查看词表│
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 左侧封面图增加视觉识别
- ✅ 进度数字具体明确（1740/3914）
- ✅ 进度条 + 文字双重展示
- ✅ 右上角操作入口（添加新书）
- ✅ 右侧快捷操作（查看词表）

**可借鉴到 AI 伴学小程序：**

```jsx
<div className="learning-card">
  <div className="card-header">
    <h3 className="card-title">正在学习</h3>
    <button className="card-action">+ 添加新计划</button>
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

---

### 3. 每日任务量卡片 ⭐⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│ 每日任务量              📝 调整  │
│ ─────────────────────────────── │
│  新词：10      复习词：40       │
│                    复习词：1:4   │
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 数据清晰展示（新词 10，复习词 40）
- ✅ 比例显示（复习词 1:4）
- ✅ 右上角设置入口
- ✅ 浅绿色背景区分

**可借鉴到 AI 伴学小程序：**

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
  background: #F7FAF9; /* 浅薄荷绿背景 */
  border-radius: 12px;
  padding: 16px;
  margin: 16px;
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

### 4. 模式选择卡片 ⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│ 模式                    ⚙️ 设置 │
│ ─────────────────────────────── │
│ 复习优先 / 再认模式 / 智能出词   │
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 当前模式清晰展示
- ✅ 多个模式用斜杠分隔
- ✅ 设置入口明显

**可借鉴到 AI 伴学小程序：**

```jsx
<div className="mode-card">
  <div className="card-header">
    <h3 className="card-title">学习模式</h3>
    <button className="card-action">⚙️ 设置</button>
  </div>
  <div className="mode-tags">
    <span className="mode-tag">复习优先</span>
    <span className="mode-tag">成长模式</span>
    <span className="mode-tag">智能推荐</span>
  </div>
</div>
```

---

### 5. 功能快捷入口 ⭐⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│                                 │
│  [📚]        [📊]        [🔄]   │
│ 极速刷词   熟练度分布   重新学习 │
│                                 │
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 图标 + 文字，清晰易懂
- ✅ 三个功能水平排列
- ✅ 图标色彩区分（蓝/橙/粉）
- ✅ 点击区域大

**可借鉴到 AI 伴学小程序：**

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

### 6. 已添加内容列表 ⭐⭐⭐⭐

```
已添加单词书              容量：1/2
━━━━━━━━━━━━━━━━━━━━━━━
🈶 扇贝词书    自定义词书
```

**设计优点：**
- ✅ 标题 + 容量提示
- ✅ 已添加内容横向排列
- ✅ emoji 作为图标
- ✅ 未添加内容灰色显示

**可借鉴到 AI 伴学小程序：**

```jsx
<div className="added-content">
  <div className="section-header">
    <h3 className="section-title">已添加学习计划</h3>
    <span className="capacity">容量：2/5</span>
  </div>
  
  <div className="content-list">
    <div className="content-item active">
      🈶 成长树计划
    </div>
    <div className="content-item active">
      📚 每日阅读
    </div>
    <div className="content-item empty">
      + 添加新计划
    </div>
  </div>
</div>
```

---

### 7. 空状态插画 ⭐⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│                                 │
│         [插画]                  │
│    笔记本电脑 + 植物 + 书本      │
│                                 │
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 清新插画，无压力
- ✅ 薄荷绿配色统一
- ✅ 线条简洁
- ✅ 增加情感化设计

**可借鉴到 AI 伴学小程序：**

```jsx
<div className="empty-state">
  <div className="empty-illustration">
    {/* 可以用 SVG 或 emoji 组合 */}
    📚🌱✨
  </div>
  <p className="empty-text">
    还没有添加学习计划
  </p>
  <button className="add-button">
    + 添加第一个计划
  </button>
</div>
```

---

## 🎨 配色方案提取

### 主色调
```css
/* 薄荷绿主色 */
--primary: #26D9AD;
--primary-light: #E8F5E9;
--primary-dark: #20C997;

/* 背景色 */
--bg-white: #FFFFFF;
--bg-light: #F7FAF9;
--bg-gray: #F5F5F5;

/* 文字色 */
--text-primary: #333333;
--text-secondary: #666666;
--text-tertiary: #999999;

/* 功能色 */
--success: #48bb78;
--warning: #ed8936;
--info: #4299e1;
```

---

## 📋 AI 伴学小程序改进方案

### 首页改进（参考单词书书桌页面）

```
┌─────────────────────────────────┐
│  ← 返回        书桌             │
│ ─────────────────────────────── │
│ [学习计划]  [复习计划]          │
│ ━━━━━━                        │
│                                 │
│ 正在学习              + 添加计划 │
│ ─────────────────────────────── │
│ [🌳] 成长树 Level 5             │
│      已完成：12/48 任务   查看详情│
│      [████████░░░░░░░]          │
│                                 │
│ 每日任务量              📝 调整  │
│ ─────────────────────────────── │
│  新任务：4      复习任务：12     │
│                    比例 1:3      │
│                                 │
│ 学习模式                ⚙️ 设置  │
│ ─────────────────────────────── │
│ 复习优先 / 成长模式 / 智能推荐   │
│                                 │
│  [📚]        [📊]        [🔄]   │
│ 极速刷题   学习报告   重新学习   │
│                                 │
│ 已添加学习计划          容量:2/5 │
│ ─────────────────────────────── │
│ 🈶 成长树计划  📚 每日阅读       │
│                                 │
└─────────────────────────────────┘
```

---

## 💡 关键设计原则总结

### 1. 卡片式分组
- 每个功能模块独立卡片
- 卡片之间有明显间距
- 卡片内用分隔线区分

### 2. 数据可视化
- 具体数字展示（1740/3914）
- 进度条直观展示
- 比例显示（1:4）

### 3. 操作入口清晰
- 右上角操作按钮
- 图标 + 文字
- 颜色区分

### 4. 信息层次
- 标题 16px 粗体
- 内容 14px 常规
- 辅助信息 12px 灰色

### 5. 配色统一
- 薄荷绿主色调
- 浅绿色背景区分
- 灰色文字辅助

---

## 🚀 v0.dev 提示词

```
Create a mobile learning app dashboard screen

Design reference: Clean, minimalist educational app like Baicizhan

Key elements:
1. Top tabs: "Learning Plan" and "Review Plan"
2. Learning progress card with book cover, progress bar (1740/3914), "View Details" button
3. Daily tasks card showing "New: 4, Review: 12", ratio 1:3
4. Learning mode card with tags: "Review First / Growth Mode / Smart"
5. Quick actions: 3 icons (Study, Report, Relearn) with colored backgrounds
6. Added plans section with capacity indicator (2/5)
7. Empty state illustration at bottom

Color scheme:
- Primary: Mint green (#26D9AD)
- Background: Light mint (#F7FAF9) and white
- Text: Dark gray (#333) to light gray (#999)

Design principles:
- Card-based layout
- Clear data visualization
- Minimalist, no anxiety
- Touch-friendly buttons
```

---

## ✅ 可立即应用的改进

### 第 1 优先级（立即应用）
1. **卡片式布局** - 每个功能模块独立卡片
2. **数据具体化** - 显示具体数字（12/48 任务）
3. **进度条优化** - 加大高度，添加具体数字
4. **操作入口** - 右上角添加设置/调整按钮

### 第 2 优先级（今天完成）
5. **功能快捷入口** - 3 个彩色图标按钮
6. **学习模式展示** - 标签式展示当前模式
7. **容量提示** - 显示"容量：2/5"

### 第 3 优先级（本周完成）
8. **空状态插画** - 设计清新的空状态
9. **配色统一** - 薄荷绿主题
10. **信息层次** - 字号规范化

---

## 📊 对比分析

### 单词书 APP vs AI 伴学小程序

| 元素 | 单词书 APP | AI 伴学小程序（改进方案） |
|-----|-----------|------------------------|
| **布局** | 卡片式分组 | 卡片式分组（借鉴） |
| **进度** | 1740/3914 词 | 12/48 任务（借鉴） |
| **每日任务** | 新词 10/复习 40 | 新任务 4/复习 12（借鉴） |
| **快捷入口** | 3 个彩色图标 | 3 个彩色图标（借鉴） |
| **配色** | 薄荷绿 | 薄荷绿 + 紫色（融合） |
| **特色** | 工具化高效 | 游戏化成长（保留） |

---

## 🎯 总结

### 单词书 APP 的优点
- ✅ 卡片式布局，信息清晰
- ✅ 数据具体化，可量化
- ✅ 操作入口明显
- ✅ 配色清爽统一
- ✅ 功能快捷入口

### AI 伴学小程序的差异化
- 🌳 成长树视觉中心（保留）
- 🎮 游戏化激励（保留）
- 👨‍👩‍👧 家长参与（保留）
- 📚 多学科学习（保留）

### 最佳实践结合
> **单词书 APP 的清晰布局 + AI 伴学小程序的游戏化 = 完美体验**

---

**下一步：** 整合所有截图分析，生成完整的 UI 调整指导

**最后更新：** 2026-03-12
