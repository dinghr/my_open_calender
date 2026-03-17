# UI 设计参考 - AI 单词学习详情页分析

**创建日期：** 2026-03-12  
**来源：** 用户提供的 AI 单词学习 APP 截图

---

## 📱 界面分析

### 整体风格
- **布局：** 卡片式，信息层次清晰
- **内容：** AI 生成详细讲解 + 例句
- **交互：** 底部功能按钮 + 下一个

---

## 🎨 核心设计元素分析

### 1. 顶部单词展示 ⭐⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│                                 │
│         refine                  │
│      /rɪ'faɪn/   🔊            │
│                                 │
│   v. 精炼，提炼；改善            │
│                                 │
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 大字号单词（居中）
- ✅ 音标 + 发音按钮
- ✅ 中文释义清晰
- ✅ 留白充足，不拥挤

**可借鉴到 AI 伴学小程序（古诗学习）：**

```jsx
<div className="word-header">
  <h1 className="word-title">静夜思</h1>
  <div className="word-meta">
    <span className="word-pinyin">Táng · Lǐ Bái</span>
    <button className="word-audio">🔊</button>
  </div>
  <div className="word-translation">
    唐代 · 李白
  </div>
</div>
```

**CSS 样式：**
```css
.word-header {
  text-align: center;
  padding: 32px 16px;
  background: #FFFFFF;
}

.word-title {
  font-size: 32px;
  font-weight: bold;
  color: #333333;
  margin-bottom: 12px;
}

.word-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 16px;
}

.word-pinyin {
  font-size: 16px;
  color: #666666;
  font-family: monospace;
}

.word-audio {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
}

.word-translation {
  font-size: 16px;
  color: #666666;
}
```

---

### 2. AI 讲解卡片 ⭐⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│  💡  'Refine'意味着提炼或改进，  │
│      通常用于提升技巧或工艺。    │
│      在追求完美的过程中，        │
│      'refine'是必不可少的一步。  │
│                                 │
│      来看这个例句：              │
│      He spent years to refine    │
│      his craft and become a      │
│      master artist.              │
│                                 │
│      （他花了多年时间来完善自己  │
│      的技艺，成为了一位艺术大    │
│      师。）                      │
│                                 │
│      在生活中，记得需要'refine' │
│      自己，让自己逐渐变得更卓    │
│      越！                        │
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 圆角卡片，柔和友好
- ✅ AI 图标（💡）增加识别度
- ✅ 详细讲解 + 例句 + 翻译
- ✅ 生活化建议，增加情感
- ✅ 行距舒适，易阅读

**可借鉴到 AI 伴学小程序（古诗讲解/家长备课）：**

```jsx
<div className="ai-explanation-card">
  <div className="ai-icon">💡</div>
  <div className="ai-content">
    <p>
      《静夜思》是唐代诗人李白创作的一首五言绝句，
      表达了诗人在寂静的月夜思念家乡的情感。
    </p>
    <p className="example-section">
      来看这首诗：
    </p>
    <p className="poetry-content">
      床前明月光，<br/>
      疑是地上霜。<br/>
      举头望明月，<br/>
      低头思故乡。
    </p>
    <p className="explanation">
      诗人通过明月这个意象，表达了对家乡的深深思念。
      在生活中，当我们看到月亮时，也会想起远方的亲人和朋友。
      记得珍惜与家人在一起的时光哦！
    </p>
  </div>
</div>
```

**CSS 样式：**
```css
.ai-explanation-card {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 24px 20px;
  margin: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  position: relative;
}

.ai-icon {
  position: absolute;
  top: 16px;
  left: 16px;
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.ai-content {
  margin-top: 20px;
  font-size: 15px;
  line-height: 1.8;
  color: #333333;
}

.ai-content p {
  margin-bottom: 12px;
}

.example-section {
  font-weight: 600;
  color: #667eea;
  margin-top: 20px;
}

.poetry-content {
  background: #F7FAF9;
  padding: 16px;
  border-radius: 8px;
  margin: 12px 0;
  font-family: "KaiTi", "楷体", serif;
  font-size: 16px;
  line-height: 2;
}

.explanation {
  color: #666666;
  margin-top: 16px;
}
```

---

### 3. 底部功能按钮 ⭐⭐⭐⭐⭐

```
┌─────────────────────────────────┐
│                                 │
│  [❓ 谐音] [🌳 词根] [📄 例句] [📝 出题] │
│                                 │
│  [💬 自由提问]   [下一个 →]     │
│                                 │
└─────────────────────────────────┘
```

**设计优点：**
- ✅ 4 个功能按钮，整齐排列
- ✅ 图标 + 文字，清晰易懂
- ✅ 自由提问 + 下一个，主次要分明
- ✅ 薄荷绿"下一个"按钮，引导行动

**可借鉴到 AI 伴学小程序（古诗学习）：**

```jsx
<div className="bottom-actions">
  {/* 功能按钮行 */}
  <div className="function-buttons">
    <button className="function-btn">
      <span className="btn-icon">🎵</span>
      <span className="btn-label">朗诵</span>
    </button>
    
    <button className="function-btn">
      <span className="btn-icon">📖</span>
      <span className="btn-label">译文</span>
    </button>
    
    <button className="function-btn">
      <span className="btn-icon">✍️</span>
      <span className="btn-label">赏析</span>
    </button>
    
    <button className="function-btn">
      <span className="btn-icon">📝</span>
      <span className="btn-label">出题</span>
    </button>
  </div>
  
  {/* 主操作行 */}
  <div className="main-actions">
    <button className="action-btn-secondary">
      <span className="btn-icon">💬</span>
      <span className="btn-label">自由提问</span>
    </button>
    
    <button className="action-btn-primary">
      <span className="btn-label">下一个 →</span>
    </button>
  </div>
</div>
```

**CSS 样式：**
```css
.bottom-actions {
  background: #FFFFFF;
  padding: 16px;
  padding-bottom: max(16px, env(safe-area-inset-bottom));
}

.function-buttons {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 16px;
}

.function-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 12px 8px;
  background: #F7FAF9;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.function-btn:hover {
  background: #E8F5E9;
}

.btn-icon {
  font-size: 20px;
}

.btn-label {
  font-size: 12px;
  color: #666666;
  font-weight: 500;
}

.main-actions {
  display: flex;
  gap: 12px;
}

.action-btn-secondary {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 20px;
  background: #FFFFFF;
  border: 1px solid #E0E0E0;
  border-radius: 12px;
  font-size: 15px;
  color: #666666;
  cursor: pointer;
}

.action-btn-primary {
  flex: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 14px 20px;
  background: linear-gradient(135deg, #26D9AD 0%, #20C997 100%);
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 600;
  color: #FFFFFF;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(38, 217, 173, 0.3);
}
```

---

### 4. 底部 AI 提示 ⭐⭐⭐

```
*问答内容由 AI 生成
```

**设计优点：**
- ✅ 小字提示，透明度高
- ✅ 告知用户内容来源
- ✅ 管理用户预期

**可借鉴：**
```jsx
<div className="ai-disclaimer">
  *讲解内容由 AI 生成，仅供参考
</div>
```

```css
.ai-disclaimer {
  text-align: center;
  font-size: 12px;
  color: #999999;
  padding: 12px;
  margin-top: 8px;
}
```

---

## 🎨 AI 伴学小程序应用场景

### 场景 1：古诗学习详情页

```
┌─────────────────────────────────┐
│  ← 返回                         │
│                                 │
│         静夜思                  │
│      唐代 · 李白    🔊          │
│                                 │
│  ┌───────────────────────────┐  │
│  │ 💡 《静夜思》是唐代诗人李  │  │
│  │    白创作的一首五言绝句，  │  │
│  │    表达了诗人在寂静的月夜  │  │
│  │    思念家乡的情感。        │  │
│  │                           │  │
│  │    来看这首诗：            │  │
│  │    床前明月光，            │  │
│  │    疑是地上霜。            │  │
│  │    举头望明月，            │  │
│  │    低头思故乡。            │  │
│  │                           │  │
│  │    诗人通过明月这个意象，  │  │
│  │    表达了对家乡的深深思念。│  │
│  │    在生活中，当我们看到月  │  │
│  │    亮时，也会想起远方的亲  │  │
│  │    人和朋友。              │  │
│  └───────────────────────────┘  │
│                                 │
│  [🎵 朗诵][📖 译文][✍️ 赏析][📝 出题] │
│                                 │
│  [💬 自由提问]   [下一个 →]     │
│                                 │
│  *讲解内容由 AI 生成             │
└─────────────────────────────────┘
```

---

### 场景 2：数学题解析页

```
┌─────────────────────────────────┐
│  ← 返回                         │
│                                 │
│    两位数乘法应用题              │
│         📝                      │
│                                 │
│  ┌───────────────────────────┐  │
│  │ 💡 这道题考查的是两位数乘  │  │
│  │    法的应用。解题关键是理  │  │
│  │    解"每盒"的含义，确定用  │  │
│  │    乘法计算。              │  │
│  │                           │  │
│  │    解题步骤：              │  │
│  │    1. 理解题意：5 盒铅笔    │  │
│  │    2. 每盒 12 支             │  │
│  │    3. 用乘法：5 × 12 = 60  │  │
│  │                           │  │
│  │    易错点：                │  │
│  │    容易把"每盒"理解成加法，│  │
│  │    记住"每"通常用乘法哦！  │  │
│  └───────────────────────────┘  │
│                                 │
│  [📖 解析][📝 练习][💡 提示][🎯 举一反三] │
│                                 │
│  [💬 自由提问]   [下一题 →]     │
│                                 │
│  *解析内容由 AI 生成             │
└─────────────────────────────────┘
```

---

### 场景 3：家长备课详情页

```
┌─────────────────────────────────┐
│  ← 返回                         │
│                                 │
│    古诗《静夜思》备课            │
│         👨‍👩‍👧                    │
│                                 │
│  ┌───────────────────────────┐  │
│  │ 💡 这是给家长的备课建议：  │  │
│  │                           │  │
│  │    背景故事：              │  │
│  │    李白在异乡看到明月，    │  │
│  │    想起了远方的家乡和亲人。│  │
│  │                           │  │
│  │    如何引导小朋友：        │  │
│  │    1. 先让小朋友读一遍      │  │
│  │    2. 问问他看到了什么画面  │  │
│  │    3. 一起想象月亮下的场景  │  │
│  │                           │  │
│  │    常见错误：              │  │
│  │    "疑"容易读错，注意是二声│  │
│  └───────────────────────────┘  │
│                                 │
│  [📖 背景][🎯 引导][⚠️ 错误][📝 练习] │
│                                 │
│  [💬 自由提问]   [下一课 →]     │  │
│                                 │
│  *备课内容由 AI 生成             │
└─────────────────────────────────┘
```

---

## 🎨 配色方案提取

### 主色调
```css
/* 背景色 */
--bg-page: #F5F7FA;
--bg-card: #FFFFFF;
--bg-button: #F7FAF9;
--bg-button-hover: #E8F5E9;

/* 主色 */
--primary: #26D9AD;
--primary-gradient: linear-gradient(135deg, #26D9AD 0%, #20C997 100%);

/* 辅助色 */
--accent: #667eea;
--accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* 文字色 */
--text-primary: #333333;
--text-secondary: #666666;
--text-tertiary: #999999;
--text-accent: #667eea;

/* 边框 */
--border: #E0E0E0;
```

---

## 📋 设计规范总结

### 1. 页面结构
```
顶部展示区（单词/古诗/题目）
    ↓
AI 讲解卡片（圆角 16px）
    ↓
功能按钮行（4 个）
    ↓
主操作行（自由提问 + 下一个）
    ↓
AI 提示（小字）
```

### 2. 间距规范
```
顶部展示区：padding 32px 16px
AI 卡片：margin 16px，padding 24px 20px
功能按钮：gap 8px，margin-bottom 16px
主操作：gap 12px
底部：padding 16px
```

### 3. 圆角规范
```
AI 卡片：border-radius 16px
功能按钮：border-radius 12px
主按钮：border-radius 12px
```

### 4. 字体规范
```
标题：32px bold
副标题：16px regular
正文：15px，line-height 1.8
按钮文字：12px medium / 15px 600
提示文字：12px regular
```

---

## 🚀 v0.dev 提示词

```
Create a mobile learning detail screen for kids learning app

Design reference: AI-powered vocabulary learning app

Key elements:
1. Top: Large title (古诗 title/单词), subtitle (author/pronunciation), audio button 🔊
2. AI explanation card:
   - Round icon (💡) in top-left corner
   - Detailed explanation with examples
   - Comfortable line-height (1.8)
   - Embedded content area (poetry/example sentence)
   - Life advice at the end
3. Function buttons row: 4 buttons with icons (朗诵，译文，赏析，出题)
4. Main actions row: "自由提问" (secondary) + "下一个 →" (primary, mint green)
5. Small disclaimer: "*讲解内容由 AI 生成"

Color scheme:
- Background: Light gray (#F5F7FA)
- Cards: White with soft shadow
- Primary button: Mint green gradient (#26D9AD to #20C997)
- Function buttons: Light background (#F7FAF9)
- Text: Dark gray (#333) to light gray (#999)

Design principles:
- Clean, spacious layout
- AI-powered content
- Clear hierarchy
- Touch-friendly buttons
- Educational, friendly tone
```

---

## ✅ 可立即应用的改进

### 第 1 优先级（立即应用）
1. **AI 讲解卡片样式** - 圆角 16px，AI 图标，详细讲解
2. **功能按钮行** - 4 个按钮，图标 + 文字
3. **主操作行** - 自由提问（次要）+ 下一个（主要）
4. **AI 提示** - 底部小字提示

### 第 2 优先级（今天完成）
5. **顶部展示区** - 大标题，副标题，发音按钮
6. **配色统一** - 薄荷绿主题
7. **间距规范** - 统一 padding/margin

### 第 3 优先级（本周完成）
8. **应用场景扩展** - 数学题解析、家长备课
9. **动画效果** - 卡片出现动画
10. **交互优化** - hover 状态，点击反馈

---

## 📊 对比分析

### AI 单词学习 vs AI 伴学小程序

| 元素 | AI 单词学习 | AI 伴学小程序（改进方案） |
|-----|-----------|------------------------|
| **顶部** | 单词 + 音标 + 释义 | 古诗 + 作者 + 朗诵（借鉴） |
| **AI 卡片** | 详细讲解 + 例句 | 详细讲解 + 诗句（借鉴） |
| **功能按钮** | 4 个（谐音/词根/例句/出题） | 4 个（朗诵/译文/赏析/出题） |
| **主操作** | 自由提问 + 下一个 | 自由提问 + 下一个（借鉴） |
| **AI 提示** | *问答内容由 AI 生成 | *讲解内容由 AI 生成（借鉴） |

---

## 🎯 总结

### AI 单词学习的优点
- ✅ AI 讲解卡片，详细友好
- ✅ 功能按钮清晰（4 个）
- ✅ 主次要操作分明
- ✅ AI 提示透明
- ✅ 间距舒适，易阅读

### AI 伴学小程序的差异化
- 📚 多学科（语文/数学）
- 🌳 成长树游戏化
- 👨‍👩‍👧 家长备课
- 🎨 薄荷绿主题

### 最佳实践结合
> **AI 单词学习的讲解卡片 + AI 伴学小程序的多学科 = 完美体验**

---

**下一步：** 整合所有截图分析，更新最终 UI 调整指导

**最后更新：** 2026-03-12
