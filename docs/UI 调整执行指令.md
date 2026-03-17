# UI 调整执行指令 - AI 伴学小程序

**发送日期：** 2026-03-12  
**优先级：** P0 - 最高优先级  
**执行方式：** 直接改完，无需确认  
**预计时间：** 6 天

---

## 🎯 任务概述

**任务：** 全面重构 AI 伴学小程序的前端 UI

**参考设计：** 背单词 APP + 单词书 APP + 扇贝单词 + AI 学习详情页

**目标效果：**
- ✅ 清爽简洁，无压力（薄荷绿主题）
- ✅ 视觉层次清晰（卡片式布局）
- ✅ 交互友好（大按钮、Tab 切换）
- ✅ 可商用级别

---

## 📋 必须完成的工作

### 第 1 阶段：设计规范落档（第 1 天）

#### 1.1 创建 CSS 变量文件
**文件：** `src/styles/variables.css`

```css
:root {
  /* 主色 - 薄荷绿 */
  --primary: #26D9AD;
  --primary-hover: #20C997;
  --primary-light: #E8F5E9;
  --primary-gradient: linear-gradient(135deg, #26D9AD 0%, #20C997 100%);
  
  /* 辅助色 - 紫色 */
  --accent: #667eea;
  --accent-hover: #5a67d8;
  --accent-light: #F3E8FF;
  
  /* 背景色 */
  --bg-page: #F5F7FA;
  --bg-card: #FFFFFF;
  --bg-button: #F7FAF9;
  --bg-button-hover: #E8F5E9;
  
  /* 文字色 */
  --text-primary: #333333;
  --text-secondary: #666666;
  --text-tertiary: #999999;
  
  /* 功能色 */
  --success: #48bb78;
  --warning: #ed8936;
  --error: #f56565;
  
  /* 图标配色 */
  --icon-study: #26D9AD;
  --icon-study-bg: #E8F5E9;
  --icon-data: #64B5F6;
  --icon-data-bg: #E3F2FD;
  --icon-note: #9575CD;
  --icon-note-bg: #F3E8FF;
  --icon-settings: #FFB74D;
  --icon-settings-bg: #FFF3E0;
  --icon-review: #E57373;
  --icon-review-bg: #FCE4EC;
  
  /* 边框 */
  --border: #E0E0E0;
  --border-light: #EEEEEE;
  
  /* 圆角 */
  --rounded-sm: 4px;
  --rounded: 8px;
  --rounded-md: 12px;
  --rounded-lg: 16px;
  --rounded-xl: 20px;
  --rounded-full: 9999px;
  
  /* 间距 */
  --spacing-1: 4px;
  --spacing-2: 8px;
  --spacing-3: 12px;
  --spacing-4: 16px;
  --spacing-5: 20px;
  --spacing-6: 24px;
  
  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow: 0 2px 8px rgba(0,0,0,0.08);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
  --shadow-lg: 0 6px 16px rgba(0,0,0,0.12);
  --shadow-primary: 0 4px 12px rgba(38, 217, 173, 0.3);
  
  /* 字体 */
  --text-xs: 10px;
  --text-sm: 12px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 24px;
  --text-3xl: 32px;
  --text-4xl: 48px;
  
  /* 字重 */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

#### 1.2 创建按钮组件
**文件：** `src/components/Button/Button.jsx`

```jsx
import React from 'react';
import './Button.css';

export default function Button({
  type = 'secondary',
  children,
  icon,
  onClick,
  disabled = false,
  className = '',
  ...props
}) {
  const buttonClass = `btn btn-${type} ${className}`;
  
  return (
    <button
      className={buttonClass}
      onClick={onClick}
      disabled={disabled}
      {...props}
    >
      {icon && <span className="btn-icon">{icon}</span>}
      {children}
    </button>
  );
}
```

**按钮样式：** `src/components/Button/Button.css`
```css
/* 4 种按钮类型 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: var(--rounded-md);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 类型 A：卡片操作按钮 */
.btn-card-action {
  padding: 6px 12px;
  min-height: 32px;
  background: var(--primary-light);
  color: var(--primary);
  font-size: var(--text-base);
  border-radius: var(--rounded);
}

.btn-card-action:hover:not(:disabled) {
  background: #C8E6C9;
  transform: scale(1.05);
}

/* 类型 B：主按钮 */
.btn-primary {
  width: calc(100% - 32px);
  margin: 16px;
  padding: 16px 24px;
  min-height: 56px;
  background: var(--primary-gradient);
  color: #FFFFFF;
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  border-radius: var(--rounded-lg);
  box-shadow: var(--shadow-primary);
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(38, 217, 173, 0.4);
}

/* 类型 C：次要按钮 */
.btn-secondary {
  padding: 12px 20px;
  min-height: 44px;
  background: #FFFFFF;
  color: var(--text-secondary);
  font-size: var(--text-base);
  border: 1px solid var(--border);
  border-radius: var(--rounded-md);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--bg-button-hover);
  border-color: var(--border-light);
}

/* 类型 D：快捷操作按钮 */
.btn-quick {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: none;
  border: none;
  border-radius: var(--rounded-md);
  cursor: pointer;
}

.btn-quick .quick-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--rounded-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.btn-quick .quick-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
}
```

#### 1.3 创建卡片组件
**文件：** `src/components/Card/Card.jsx`

```jsx
import React from 'react';
import './Card.css';

export default function Card({
  children,
  className = '',
  padding = 'default',
  ...props
}) {
  const cardClass = `card card-${padding} ${className}`;
  
  return (
    <div className={cardClass} {...props}>
      {children}
    </div>
  );
}
```

**卡片样式：** `src/components/Card/Card.css`
```css
.card {
  background: var(--bg-card);
  border-radius: var(--rounded-lg);
  box-shadow: var(--shadow);
  transition: all 0.2s;
}

.card-default {
  padding: var(--spacing-6) var(--spacing-5);
  margin: var(--spacing-4);
}

.card-compact {
  padding: var(--spacing-4) var(--spacing-3);
  margin: var(--spacing-3);
}

.card:hover {
  box-shadow: var(--shadow-md);
}
```

#### 1.4 创建 Tab 组件
**文件：** `src/components/Tab/Tab.jsx`

```jsx
import React from 'react';
import './Tab.css';

export default function Tab({
  items,
  activeTab,
  onChange,
  className = '',
}) {
  return (
    <div className={`tab-bar ${className}`}>
      {items.map((item) => (
        <button
          key={item.value}
          className={`tab ${activeTab === item.value ? 'active' : ''}`}
          onClick={() => onChange(item.value)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
```

**Tab 样式：** `src/components/Tab/Tab.css`
```css
.tab-bar {
  display: flex;
  gap: 24px;
  padding: 16px;
  background: var(--bg-card);
  border-bottom: 1px solid var(--border);
}

.tab {
  background: none;
  border: none;
  font-size: var(--text-base);
  color: var(--text-tertiary);
  padding: 8px 0;
  position: relative;
  cursor: pointer;
  transition: color 0.2s;
}

.tab.active {
  color: var(--primary);
  font-weight: var(--font-semibold);
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--primary);
  border-radius: 3px 3px 0 0;
}

.tab:hover {
  color: var(--primary);
}
```

---

### 第 2 阶段：首页重构（第 2 天）

#### 2.1 更新首页布局
**文件：** `src/pages/Home/Home.jsx`

```jsx
import React, { useState } from 'react';
import Card from '../../components/Card/Card';
import Tab from '../../components/Tab/Tab';
import Button from '../../components/Button/Button';
import './Home.css';

export default function Home() {
  const [subject, setSubject] = useState('chinese');
  const streakDays = 12;
  const progress = 25;
  
  return (
    <div className="home-page">
      {/* 学科 Tab 切换 */}
      <Tab
        items={[
          { value: 'chinese', label: '语文' },
          { value: 'math', label: '数学' },
        ]}
        activeTab={subject}
        onChange={setSubject}
      />
      
      {/* 打卡统计 */}
      <Card className="streak-card">
        <div className="streak-label">已坚持学习天数 🌱</div>
        <div className="streak-number">{streakDays}</div>
      </Card>
      
      {/* 成长树 */}
      <div className="growth-tree">
        <div className="tree-emoji">🌳</div>
        <div className="tree-level">Level 5 - 茁壮成长</div>
      </div>
      
      {/* 学习进度卡片 */}
      <Card className="progress-card">
        <div className="card-header">
          <h3 className="card-title">正在学习</h3>
          <Button type="card-action">+ 添加计划</Button>
        </div>
        <div className="progress-info">
          <div>成长树 Level 5</div>
          <div className="progress-text">已完成：12/48 任务</div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: '25%' }} />
          </div>
        </div>
      </Card>
      
      {/* 每日任务卡片 */}
      <Card className="daily-task-card">
        <div className="card-header">
          <h3 className="card-title">每日任务量</h3>
          <Button type="card-action">📝 调整</Button>
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
      </Card>
      
      {/* 功能快捷入口 */}
      <div className="quick-actions">
        <Button type="quick" icon="📚" label="极速刷题" color="#E3F2FD" />
        <Button type="quick" icon="📊" label="学习报告" color="#FFF3E0" />
        <Button type="quick" icon="🔄" label="重新学习" color="#FCE4EC" />
      </div>
      
      {/* 主按钮 */}
      <Button type="primary" icon="→">
        开始今日学习
      </Button>
    </div>
  );
}
```

---

### 第 3 阶段：家长专区重构（第 3 天）

#### 3.1 创建家长专区页面
**文件：** `src/pages/ParentZone/ParentZone.jsx`

```jsx
import React from 'react';
import Card from '../../components/Card/Card';
import './ParentZone.css';

export default function ParentZone() {
  const functionGroups = [
    {
      title: '学习管理',
      functions: [
        { icon: '👨‍👩‍👧', label: '绑定管理', color: '#E8F5E9' },
        { icon: '📊', label: '学习报告', color: '#E3F2FD' },
        { icon: '📋', label: '学习计划', color: '#F3E8FF' },
        { icon: '🔑', label: '登录码', color: '#FFF3E0' },
        { icon: '📝', label: '倾向调整', color: '#FCE4EC' },
        { icon: '📚', label: '题库管理', color: '#E0F7FA' },
        { icon: '🎯', label: '目标设置', color: '#FFEBEE' },
        { icon: '⏰', label: '学习时间', color: '#F5F5F5' },
      ],
    },
    {
      title: '备课中心',
      functions: [
        { icon: '📖', label: '古诗备课', color: '#E8F5E9' },
        { icon: '✍️', label: '精读备课', color: '#E3F2FD' },
        { icon: '🔢', label: '数学备课', color: '#FFF3E0' },
        { icon: '📋', label: '备课记录', color: '#F3E8FF' },
      ],
    },
    {
      title: '系统设置',
      functions: [
        { icon: '🔒', label: '密码设置', color: '#F5F5F5' },
        { icon: '🔔', label: '通知设置', color: '#F5F5F5' },
        { icon: '🛡️', label: '隐私设置', color: '#F5F5F5' },
        { icon: '❓', label: '帮助反馈', color: '#F5F5F5' },
      ],
    },
  ];
  
  return (
    <div className="parent-zone">
      {/* 用户信息 */}
      <Card className="parent-header">
        <div className="parent-info">
          <div className="parent-avatar">👨‍👩‍👧</div>
          <div>
            <div className="parent-name">管理员</div>
            <div className="parent-subtitle">已绑定 2 个小朋友</div>
          </div>
        </div>
      </Card>
      
      {/* 功能分组 */}
      {functionGroups.map((group) => (
        <Card key={group.title} className="function-section">
          <h3 className="section-title">{group.title}</h3>
          <div className="function-grid">
            {group.functions.map((func) => (
              <button key={func.label} className="function-item">
                <div
                  className="function-icon"
                  style={{ background: func.color }}
                >
                  {func.icon}
                </div>
                <span className="function-label">{func.label}</span>
              </button>
            ))}
          </div>
        </Card>
      ))}
    </div>
  );
}
```

---

### 第 4 阶段：学习详情页（第 4 天）

#### 4.1 创建学习详情页
**文件：** `src/pages/LearningDetail/LearningDetail.jsx`

```jsx
import React, { useState } from 'react';
import Card from '../../components/Card/Card';
import Button from '../../components/Button/Button';
import './LearningDetail.css';

export default function LearningDetail({ type, content }) {
  const [showHint, setShowHint] = useState(false);
  
  return (
    <div className="learning-detail-page">
      {/* 顶部展示 */}
      <div className="detail-header">
        <h1 className="detail-title">{content.title}</h1>
        <div className="detail-meta">
          <span>{content.author}</span>
          <button className="audio-btn">🔊</button>
        </div>
      </div>
      
      {/* AI 讲解卡片 */}
      <Card className="ai-explanation-card">
        <div className="ai-icon">💡</div>
        <div className="ai-content">
          <p>{content.explanation}</p>
          <p className="example-section">来看这首诗：</p>
          <div className="poetry-content">
            {content.poetry}
          </div>
          <p className="explanation">{content.lifeAdvice}</p>
        </div>
      </Card>
      
      {/* 功能按钮行 */}
      <div className="function-buttons">
        <Button type="quick" icon="🎵" label="朗诵" />
        <Button type="quick" icon="📖" label="译文" />
        <Button type="quick" icon="✍️" label="赏析" />
        <Button type="quick" icon="📝" label="出题" />
      </div>
      
      {/* 主操作行 */}
      <div className="main-actions">
        <Button type="secondary" icon="💬">
          自由提问
        </Button>
        <Button type="primary">下一个 →</Button>
      </div>
      
      {/* AI 提示 */}
      <div className="ai-disclaimer">
        *讲解内容由 AI 生成，仅供参考
      </div>
    </div>
  );
}
```

---

### 第 5 阶段：出题页（第 5 天上午）

#### 5.1 创建出题页
**文件：** `src/pages/QuestionPractice/QuestionPractice.jsx`

```jsx
import React, { useState } from 'react';
import Card from '../../components/Card/Card';
import Button from '../../components/Button/Button';
import Tab from '../../components/Tab/Tab';
import './QuestionPractice.css';

export default function QuestionPractice() {
  const [subject, setSubject] = useState('math');
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  
  const question = {
    number: 1,
    text: '小明有 5 盒铅笔，每盒 12 支，一共有多少支铅笔？',
    options: ['A. 17', 'B. 60', 'C. 50', 'D. 70'],
    hint: '提示：每盒用乘法计算',
  };
  
  const progress = ((currentQuestionIndex + 1) / 20) * 100;
  
  return (
    <div className="practice-page">
      {/* 学科 Tab 切换 */}
      <Tab
        items={[
          { value: 'chinese', label: '语文' },
          { value: 'math', label: '数学' },
        ]}
        activeTab={subject}
        onChange={setSubject}
      />
      
      {/* 题目卡片 */}
      <Card className="question-card">
        <div className="card-header">
          <h3 className="question-title">📝 题目 #{question.number}</h3>
          <span className="question-tag">{subject}</span>
        </div>
        
        <div className="question-content">
          <p className="question-text">{question.text}</p>
        </div>
        
        <div className="options-grid">
          {question.options.map((option, index) => (
            <button
              key={index}
              className={`option-btn ${selectedAnswer === index ? 'selected' : ''}`}
              onClick={() => setSelectedAnswer(index)}
            >
              <span className="option-label">{option[0]}.</span>
              <span className="option-text">{option.slice(3)}</span>
            </button>
          ))}
        </div>
        
        <div className="card-actions">
          <Button type="secondary" icon="💡" onClick={() => setShowHint(!showHint)}>
            提示
          </Button>
          <Button type="secondary" icon="📝">
            草稿纸
          </Button>
        </div>
        
        {showHint && (
          <div className="hint-box">
            <p>{question.hint}</p>
          </div>
        )}
        
        <div className="card-navigation">
          <Button type="secondary" disabled={currentQuestionIndex === 0}>
            ← 上一题
          </Button>
          <Button type="primary">
            {currentQuestionIndex === 19 ? '提交 →' : '下一题 →'}
          </Button>
        </div>
      </Card>
      
      {/* 进度条 */}
      <div className="progress-section">
        <div className="progress-info">
          <span>进度：{currentQuestionIndex + 1}/20</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }} />
        </div>
      </div>
    </div>
  );
}
```

---

### 第 6 阶段：错题页（第 5 天下午）

#### 6.1 创建错题页
**文件：** `src/pages/WrongQuestions/WrongQuestions.jsx`

```jsx
import React, { useState } from 'react';
import Card from '../../components/Card/Card';
import Button from '../../components/Button/Button';
import Tab from '../../components/Tab/Tab';
import './WrongQuestions.css';

export default function WrongQuestions() {
  const [timeFilter, setTimeFilter] = useState('week');
  const [subjectFilter, setSubjectFilter] = useState('all');
  
  const wrongQuestions = [
    {
      id: 1,
      title: '两位数乘法',
      icon: '🔢',
      daysAgo: 3,
      text: '小明有 5 盒铅笔，每盒 12 支...',
      userAnswer: '17',
      correctAnswer: '60',
      errorReason: '概念不清',
      masteryLevel: 'reviewing',
    },
    {
      id: 2,
      title: '古诗填空',
      icon: '📖',
      daysAgo: 5,
      text: '床前明月光，疑是___',
      userAnswer: '地上下',
      correctAnswer: '地上',
      errorReason: '粗心',
      masteryLevel: 'mastered',
    },
  ];
  
  return (
    <div className="wrong-questions-page">
      {/* 时间筛选 */}
      <Tab
        items={[
          { value: 'week', label: '本周' },
          { value: 'month', label: '本月' },
          { value: 'all', label: '全部' },
        ]}
        activeTab={timeFilter}
        onChange={setTimeFilter}
      />
      
      {/* 学科筛选 */}
      <div className="filter-bar">
        <select
          className="filter-select"
          value={subjectFilter}
          onChange={(e) => setSubjectFilter(e.target.value)}
        >
          <option value="all">全部</option>
          <option value="chinese">语文</option>
          <option value="math">数学</option>
        </select>
      </div>
      
      {/* 错题列表 */}
      <div className="wrong-questions-list">
        {wrongQuestions.map((question) => (
          <Card key={question.id} className="wrong-question-card">
            <div className="card-header">
              <div className="question-info">
                <span className="question-icon">{question.icon}</span>
                <h3 className="question-title">{question.title}</h3>
              </div>
              <span className="time-ago">{question.daysAgo}天前</span>
            </div>
            
            <div className="card-divider" />
            
            <div className="question-content">
              <p className="question-text">{question.text}</p>
            </div>
            
            <div className="answer-comparison">
              <div className="answer-row wrong">
                <span className="answer-label">你的答案：</span>
                <span className="answer-text">{question.userAnswer}</span>
                <span className="answer-icon">❌</span>
              </div>
              <div className="answer-row correct">
                <span className="answer-label">正确答案：</span>
                <span className="answer-text">{question.correctAnswer}</span>
                <span className="answer-icon">✅</span>
              </div>
            </div>
            
            <div className="error-analysis">
              <div className="analysis-row">
                <span className="analysis-label">错误原因：</span>
                <span className="analysis-value">{question.errorReason}</span>
              </div>
              <div className="analysis-row">
                <span className="analysis-label">掌握程度：</span>
                <span className={`mastery-badge ${question.masteryLevel}`}>
                  {question.masteryLevel === 'mastered' ? '✅ 已掌握' : '🔄 复习中'}
                </span>
              </div>
            </div>
            
            <div className="card-actions">
              <Button type="quick" icon="📖" label="解析" />
              <Button type="quick" icon="🔄" label="举一反三" />
            </div>
            
            <div className="card-actions">
              <Button type="success" icon="✅">
                已掌握
              </Button>
              <Button type="danger" icon="🗑️">
                删除
              </Button>
            </div>
          </Card>
        ))}
      </div>
      
      {/* 统计信息 */}
      <div className="stats-footer">
        共 {wrongQuestions.length} 道错题 | 已掌握{' '}
        {wrongQuestions.filter((q) => q.masteryLevel === 'mastered').length} 道
      </div>
    </div>
  );
}
```

---

### 第 7 阶段：底部导航更新（第 6 天上午）

#### 7.1 更新底部导航
**文件：** `src/components/BottomNav/BottomNav.jsx`

```jsx
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Home, Book, BookOpen, User } from 'lucide-react';
import './BottomNav.css';

export default function BottomNav() {
  const navigate = useNavigate();
  const location = useLocation();
  
  const navItems = [
    { path: '/home', icon: Home, label: '首页' },
    { path: '/plan', icon: Book, label: '计划' },
    { path: '/wrong', icon: BookOpen, label: '错题' },
    { path: '/parent', icon: User, label: '家长' },
  ];
  
  return (
    <nav className="bottom-nav">
      {navItems.map((item) => {
        const isActive = location.pathname === item.path;
        const Icon = item.icon;
        
        return (
          <div
            key={item.path}
            className={`nav-item ${isActive ? 'active' : ''}`}
            onClick={() => navigate(item.path)}
          >
            <Icon
              size={24}
              strokeWidth={isActive ? 2 : 1.5}
              color={isActive ? '#667eea' : '#999999'}
            />
            <span className="nav-label">{item.label}</span>
          </div>
        );
      })}
    </nav>
  );
}
```

---

### 第 8 阶段：测试与优化（第 6 天下午）

#### 8.1 测试清单
- [ ] 所有页面正常显示
- [ ] 所有按钮可点击
- [ ] Tab 切换流畅
- [ ] 进度条动画流畅
- [ ] 响应式布局正常
- [ ] iOS Safari 兼容
- [ ] Android Chrome 兼容
- [ ] iPhone X 底部适配

#### 8.2 性能优化
- [ ] 图片压缩
- [ ] 代码分割
- [ ] 懒加载
- [ ] 缓存策略

---

## 📝 重要提示

### 1. CSS 变量必须统一
所有颜色、间距、圆角等必须使用 CSS 变量，**禁止硬编码**！

**错误示例：**
```css
/* ❌ 错误 */
.card {
  border-radius: 16px;
  background: #FFFFFF;
}
```

**正确示例：**
```css
/* ✅ 正确 */
.card {
  border-radius: var(--rounded-lg);
  background: var(--bg-card);
}
```

### 2. 组件必须复用
按钮、卡片、Tab 等组件必须创建为可复用组件，**禁止每个页面单独写样式**！

### 3. 设计规范必须遵守
- 圆角：16px（卡片）、12px（按钮）
- 间距：16px（卡片间距）、24px（卡片内边距）
- 字体：32px（大标题）、16px（正文）、12px（辅助文字）

### 4. 配色必须统一
所有颜色必须使用 CSS 变量，方便后期统一调整！

---

## ✅ 验收标准

### 视觉验收
- [ ] 配色统一（薄荷绿主题）
- [ ] 圆角统一（16px/12px）
- [ ] 间距统一（16px/24px）
- [ ] 图标风格统一
- [ ] 卡片样式统一

### 交互验收
- [ ] Tab 切换流畅
- [ ] 按钮点击反馈明显
- [ ] 动画流畅（transition）
- [ ] 所有按钮易点击（≥44px）

### 代码验收
- [ ] 使用 CSS 变量
- [ ] 组件可复用
- [ ] 代码规范
- [ ] 注释清晰

---

## 📞 需要帮助？

参考文档位置：
- `/home/ecs-user/my_open_calender/docs/UI 调整最终指导.md`
- `/home/ecs-user/my_open_calender/docs/按钮设计规范.md`
- `/home/ecs-user/my_open_calender/docs/家长专区页面设计.md`
- `/home/ecs-user/my_open_calender/docs/出题页与错题页卡片式设计.md`
- `/home/ecs-user/my_open_calender/docs/UI 需求变更总结.md`

---

**开始执行！** 🚀

**最后更新：** 2026-03-12  
**执行优先级：** P0 - 立即执行  
**预计完成时间：** 6 天
