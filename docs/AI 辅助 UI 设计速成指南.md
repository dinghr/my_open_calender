# AI 辅助 UI 设计速成指南（Vibe Coding）

**创建日期：** 2026-03-12  
**目标：** 零基础快速达到商用级别 UI 设计能力

---

## 🎨 什么是 Vibe Coding？

**Vibe Coding** = 用 AI 辅助编程，专注于创意和方向，让 AI 处理细节实现

**核心理念：**
- 你负责"感觉"（Vibe）- 想要什么风格、什么效果
- AI 负责"实现"（Coding）- 生成代码、调整细节
- 快速迭代，不满意就让 AI 重做

---

## 🛠️ 推荐 AI 工具栈

### 第一梯队：专业 UI 生成 ⭐⭐⭐⭐⭐

| 工具 | 网址 | 特点 | 价格 |
|-----|------|------|------|
| **v0.dev** | https://v0.dev | Vercel 出品，React/Tailwind，质量最高 | 免费 + 付费 |
| **Lovable** | https://lovable.dev | 全栈生成，支持数据库 | 免费 + 付费 |
| **Bolt.new** | https://bolt.new | 一键部署，快速原型 | 免费 |
| **Create.xyz** | https://create.xyz | 组件生成，可定制 | 免费 + 付费 |

### 第二梯队：代码助手 ⭐⭐⭐⭐

| 工具 | 网址 | 特点 |
|-----|------|------|
| **Cursor** | https://cursor.com | AI 编辑器，理解上下文 |
| **Claude Code** | CLI | 命令行 AI 编程 |
| **GitHub Copilot** | IDE 插件 | 代码补全 |

### 第三梯队：设计灵感 ⭐⭐⭐

| 工具 | 网址 | 用途 |
|-----|------|------|
| **Dribbble** | https://dribbble.com | 设计灵感 |
| **Behance** | https://behance.net | 设计案例 |
| **Mobbin** | https://mobbin.com | 移动端 UI 模式 |
| **Page Flows** | https://pageflows.com | 用户流程参考 |

---

## 🚀 快速上手工作流

### 工作流 1：v0.dev 生成法（推荐）⭐

**步骤：**

```
1. 打开 https://v0.dev
2. 用英文描述你想要的界面
3. AI 生成 3 个版本
4. 选择喜欢的，点击"Use this code"
5. 复制到你的项目
6. 不满意？让 AI 调整！
```

**提示词模板：**
```
Create a [页面类型] for [产品类型] with [风格描述]

Requirements:
- Color scheme: [配色方案]
- Target users: [目标用户]
- Key features: [核心功能]
- Design style: [设计风格，如 modern, playful, minimal]
- Must include: [必须包含的元素]

Examples I like: [参考网站/应用]
```

**示例（AI 伴学小程序首页）：**
```
Create a mobile home screen for a kids learning app

Requirements:
- Color scheme: Purple gradient, warm and friendly
- Target users: K12 students and parents
- Key features: Growth tree visualization, daily tasks, progress tracking
- Design style: Playful, encouraging, not anxiety-inducing
- Must include: Animated tree, task cards with emojis, completion buttons

Design principles:
- Large touch targets for kids
- Positive reinforcement language
- No red colors for incomplete tasks
- Soft rounded corners everywhere
```

---

### 工作流 2：Bolt.new 快速原型法

**步骤：**

```
1. 打开 https://bolt.new
2. 输入完整的产品描述
3. AI 生成完整项目（前端 + 后端）
4. 在线预览和编辑
5. 一键部署或下载代码
```

**优势：** 全栈生成，适合从零开始

---

### 工作流 3：Cursor 迭代优化法

**步骤：**

```
1. 用 Cursor 打开现有项目
2. Ctrl+K 打开 AI 对话框
3. 输入改进建议
4. AI 修改代码
5. 预览效果，继续调整
```

**示例对话：**
```
用户：把这个按钮做得更可爱一些，适合小朋友使用

AI：好的，我会：
- 加大圆角（border-radius: 20px）
- 添加渐变色背景
- 增加 hover 动画
- 添加 emoji 图标

[AI 自动修改代码]
```

---

## 🎨 设计原则速成

### 1. 配色方案（不会出错的选择）

**儿童教育类：**
```
主色：#667eea（紫色）
辅色：#764ba2（深紫）
强调色：#f093fb（粉色）
背景：#f5f7fa（浅灰）
成功：#48bb78（绿色）
```

**工具类：**
```
主色：#3182ce（蓝色）
辅色：#2c5282（深蓝）
强调色：#ed8936（橙色）
背景：#f7fafc（浅灰）
成功：#48bb78（绿色）
```

**推荐工具：**
- https://coolors.co - 一键生成配色
- https://uigradients.com - 渐变色库

### 2. 字体选择

**中文：**
- 优先使用系统字体（加载快）
- 标题：PingFang SC, Microsoft YaHei
- 正文：同标题或更细字重

**英文：**
- 标题：Inter, Poppins, Montserrat
- 正文：Inter, Roboto, Open Sans

**字号规范：**
```
超大标题：32px
大标题：24px
中标题：18px
正文：16px
辅助文字：14px
小字：12px
```

### 3. 间距规范

**使用 8 的倍数：**
```
4px - 极小间距
8px - 小组件间距
16px - 标准间距
24px - 大间距
32px - 超大间距
48px - 分区间距
```

### 4. 圆角规范

```
小圆角：4px（按钮、卡片）
中圆角：8px（输入框）
大圆角：16px（卡片、弹窗）
超大圆角：24px+（儿童产品）
```

---

## 📚 推荐学习资源

### 免费教程

1. **YouTube 频道：**
   - [DesignCourse](https://youtube.com/@DesignCourse) - UI/UX 教程
   - [Flux Academy](https://youtube.com/@FluxAcademy) - 网页设计
   - [AJ&Smart](https://youtube.com/@AJSmart) - 产品设计流程

2. **中文教程：**
   - [B 站 - 设计基础](https://bilibili.com)
   - [优设网](https://uisdc.com) - 设计文章

3. **AI 编程教程：**
   - [v0.dev 官方文档](https://v0.dev/docs)
   - [Cursor 官方教程](https://cursor.com/tutorial)

### 付费课程（可选）

- [Udemy - Web Design for Beginners](https://udemy.com)
- [MasterClass - Design Thinking](https://masterclass.com)

---

## 🎯 30 天速成计划

### 第 1 周：工具熟悉
- [ ] 注册 v0.dev、Bolt.new
- [ ] 每天生成 3 个不同页面
- [ ] 学习基本提示词技巧
- [ ] 建立自己的设计灵感库

### 第 2 周：设计原则
- [ ] 学习配色理论
- [ ] 学习排版基础
- [ ] 学习间距和布局
- [ ] 临摹 5 个优秀设计

### 第 3 周：实战练习
- [ ] 为自己的项目设计首页
- [ ] 设计 3 个核心页面
- [ ] 用 AI 生成完整代码
- [ ] 集成到实际项目

### 第 4 周：优化迭代
- [ ] 收集用户反馈
- [ ] 根据反馈调整设计
- [ ] 学习交互动效
- [ ] 建立自己的组件库

---

## 💡 提示词技巧（Prompt Engineering）

### 好提示词 vs 差提示词

❌ **差：** "做一个好看的首页"
✅ **好：** "做一个儿童教育 APP 的首页，紫色渐变主题，包含成长树可视化、今日任务卡片、完成进度条，风格活泼可爱，大圆角，适合 6-12 岁儿童使用"

### 提示词公式

```
[角色] + [任务] + [具体要求] + [参考示例] + [避免事项]

示例：
你是一位专业的 UI 设计师（角色）
请设计一个学习 APP 的首页（任务）
要求：紫色主题、包含成长树、任务列表、进度追踪（具体要求）
参考：Duolingo、Khan Academy Kids（参考示例）
避免：红色、尖锐边角、复杂文字（避免事项）
```

### 迭代技巧

```
第一轮：生成基础版本
第二轮：调整配色和字体
第三轮：优化间距和布局
第四轮：添加动画和交互
第五轮：微调细节
```

---

## 🎨 可商用设计资源

### 免费图标

- [Heroicons](https://heroicons.com) - SVG 图标
- [Feather Icons](https://feathericons.com) - 简洁图标
- [IconPark](https://iconpark.oceanengine.com) - 中文图标库
- [Emoji](https://emojipedia.org) - Emoji 表情

### 免费图片

- [Unsplash](https://unsplash.com) - 高质量图片
- [Pexels](https://pexels.com) - 免费商用
- [Pixabay](https://pixabay.com) - 多种素材

### 免费插画

- [unDraw](https://undraw.co) - 开源插画
- [ManyPixels](https://manypixels.co/gallery) - 可定制插画
- [Open Peeps](https://openpeeps.com) - 手绘人物

---

## 📱 AI 伴学小程序 UI 改进建议

### 当前问题
- 界面太丑
- 不够吸引小朋友
- 缺少专业感

### 改进方向

**1. 使用 v0.dev 重新生成：**
```
提示词：
Create a mobile home screen for AI-powered kids learning companion

Key elements:
- Central: Animated growth tree (shows progress)
- Task cards with emojis and progress indicators
- Warm color scheme: purple/pink gradient
- Large, rounded buttons for kids
- Celebration animations for completed tasks
- Parent corner (hidden behind password)

Design principles:
- No anxiety-inducing elements (no red X marks, no countdown timers)
- Positive language only
- Soft shadows and rounded corners
- High contrast for readability
- Touch-friendly (minimum 44px touch targets)
```

**2. 配色方案：**
```
主色：#667eea → #764ba2（紫色渐变）
成功：#48bb78（绿色）
警告：#ed8936（橙色）
背景：#f5f7fa（浅灰）
卡片：白色 + 柔和阴影
```

**3. 字体优化：**
```
标题：PingFang SC Bold 24px
正文：PingFang SC Regular 16px
辅助：PingFang SC Light 14px
```

**4. 组件库推荐：**
- [shadcn/ui](https://ui.shadcn.com) - 现代组件
- [Chakra UI](https://chakra-ui.com) - 易用组件
- [Naive UI](https://naive-ui.com) - 中文友好

---

## 🚀 立即行动

### 5 分钟快速改进

1. 打开 https://v0.dev
2. 复制上面的提示词
3. 生成 3 个版本
4. 选择最喜欢的
5. 下载代码替换现有首页

### 1 小时深度改进

1. 用 v0.dev 生成所有核心页面
2. 统一配色方案
3. 替换所有字体
4. 优化间距和布局
5. 添加简单动画

### 1 天完整重构

1. 设计完整信息架构
2. 生成所有页面
3. 创建组件库
4. 实现交互动效
5. 测试和优化

---

## 📞 需要帮助？

**常见问题：**

Q: AI 生成的代码太复杂，看不懂怎么办？
A: 让 AI 简化，或者只复制 HTML/CSS 部分，自己写逻辑

Q: 生成的样式和预期不一样？
A: 提供更详细的提示词，包括具体颜色、间距、字体

Q: 如何保持多个页面风格一致？
A: 在提示词中指定统一的设计系统，或使用相同的组件库

---

**最后更新：** 2026-03-12  
**下一步：** 选择一个工具，开始第一次 AI 辅助设计！
