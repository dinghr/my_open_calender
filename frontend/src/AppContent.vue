<template>
  <div class="app-container">
    <!-- 内容区域 -->
    <div class="main-content">
      <!-- 首页 -->
      <div v-show="activeTab === 'home'" class="page-content">
        <!-- AI 欢迎语卡片 -->
        <div class="ai-welcome-card">
          <div class="welcome-header">
            <div class="welcome-avatar">{{ currentChild.gender === 'girl' ? '👧' : '👦' }}</div>
            <div class="welcome-text">
              <div class="welcome-greeting">🌟 早上好，{{ currentChild.nickname }}！</div>
              <div class="welcome-message">{{ aiWelcomeMessage }}</div>
            </div>
          </div>
          <div class="welcome-interests" v-if="currentChild.hobbies">
            <n-tag 
              v-for="(hobby, index) in currentChild.hobbies.split(' · ')" 
              :key="index"
              size="small"
              type="info"
              round>
              {{ hobby }}
            </n-tag>
          </div>
        </div>

        <!-- 恐龙组件引用 -->
        <Spinosaurus
          ref="spinosaurusRef"
          :level="spinosaurus.level"
          :attack="spinosaurus.attack"
          :defense="spinosaurus.defense"
          :streak-days="spinosaurus.streakDays"
          :exp-percent="spinosaurus.expPercent"
          :exp-to-next="spinosaurus.expToNext"
        />

        <!-- 积分与等级 - 紧凑版带星星月亮太阳 -->
        <PointsLevel :points="points" />

        <!-- 今日任务卡片区域 - 单任务卡片滑动切换 -->
        <div class="task-section">
          <div class="task-progress">
            <span class="progress-label">📋 今日任务</span>
            <n-tag type="info" size="small">{{ completedCount }}/{{ todayTasks.length }}</n-tag>
          </div>

          <div class="task-carousel">
            <TransitionGroup name="task-slide">
              <!-- 当前任务卡片 -->
              <div v-if="currentTask" :key="currentTask.id" class="task-card-large">
                <div class="task-icon-large">{{ currentTask.icon }}</div>
                <div class="task-subject-tag" :class="currentTask.subject">{{ currentTask.subjectLabel }}</div>
                <div class="task-title-large">{{ currentTask.title }}</div>
                <div class="task-content-large">{{ currentTask.content }}</div>

                <div class="task-actions">
                  <n-button
                    class="skip-btn"
                    size="large"
                    round
                    @click="skipTask"
                  >
                    ⏭️ 下次一定
                  </n-button>
                  <n-button
                    type="success"
                    size="large"
                    round
                    @click="completeTask"
                  >
                    ✅ 完成
                  </n-button>
                </div>
              </div>

              <!-- 所有任务完成提示 -->
              <div v-else key="done" class="task-complete">
                <div class="complete-icon">🎉</div>
                <div class="complete-title">太棒了！</div>
                <div class="complete-desc">今日任务已全部完成</div>
                <div class="complete-stats">
                  <span class="stat">{{ completedCount }} 项任务</span>
                  <span class="stat">+{{ completedCount * 5 }} 攻击力</span>
                  <span class="stat">+{{ completedCount * 15 }} 积分</span>
                </div>
              </div>
            </TransitionGroup>
          </div>

          <!-- 任务进度指示器 -->
          <div class="task-indicators">
            <span
              v-for="(task, index) in todayTasks"
              :key="task.id"
              class="indicator"
              :class="{
                active: index === currentTaskIndex && !task.skipped,
                completed: task.completed,
                skipped: task.skipped
              }"
            />
          </div>
        </div>
      </div>

      <!-- 计划页 -->
      <div v-show="activeTab === 'plan'" class="page-content">
        <h2 style="margin-bottom: 20px; color: #333;">📅 我的计划</h2>

        <!-- 学校课表 -->
        <n-card title="🏫 学校课表" size="medium" style="margin-bottom: 15px;">
          <template #header-extra>
            <n-button text type="primary" @click="handleClick('查看完整课表')">查看完整课表 →</n-button>
          </template>
          <div class="book-list">
            <n-tag v-for="book in todayBooks" :key="book" type="info">{{ book }}</n-tag>
          </div>
          <n-text depth="3" style="margin-top: 12px; display: block;">
            今日课程：语文 → 数学 → 英语 → 美术
          </n-text>
          <n-text type="success" style="margin-top: 4px; display: block;">
            放学时间：15:30
          </n-text>
        </n-card>

        <!-- 课后安排 -->
        <n-card title="🏠 课后安排" size="medium" style="margin-bottom: 15px;">
          <n-space vertical>
            <div v-for="activity in afterSchoolActivities" :key="activity.time" class="activity-item" :style="{ background: activity.color }">
              <span>{{ activity.icon }} {{ activity.time }} {{ activity.name }}</span>
              <n-tag v-if="activity.location" size="small" type="success">{{ activity.location }}</n-tag>
            </div>
          </n-space>
        </n-card>

        <!-- 每日一练打印 -->
        <DailyPractice :student-id="currentStudentId" />
      </div>

      <!-- 阅读页 -->
      <div v-show="activeTab === 'reading'" class="page-content">
        <h2 style="margin-bottom: 20px; color: #333;">📚 阅读专区</h2>

        <!-- 阅读的重要性 -->
        <div class="reading-tip">
          <div class="tip-header">
            <span style="font-size: 24px;">💡</span>
            <span style="font-weight: 600; color: #5b21b6;">为什么要阅读？</span>
          </div>
          <p>阅读可以带你去任何想去的地方！📚 每一本书都是一扇窗户，让你看见更大的世界。坚持阅读，你的知识会像魔法一样增长，积分也会越来越多哦！✨</p>
        </div>

        <!-- 阅读统计 -->
        <n-card class="reading-stats" size="medium" style="margin-bottom: 15px;">
          <template #header>
            <span class="stats-title">📊 本月阅读</span>
            <span class="stats-value">12,580 字</span>
          </template>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-value">5</div>
              <div class="stat-label">已读完</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">2</div>
              <div class="stat-label">在读中</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">+280</div>
              <div class="stat-label">获得积分</div>
            </div>
          </div>
        </n-card>

        <!-- 我的图书馆 -->
        <n-card title="📖 我的图书馆" size="medium" style="margin-bottom: 15px;">
          <template #header-extra>
            <n-button text type="primary">查看全部 →</n-button>
          </template>

          <!-- 正在阅读 -->
          <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: #666; margin-bottom: 8px;">🔥 正在阅读</div>
            <div class="book-row">
              <div v-for="book in readingBooks" :key="book.id" class="book-card" @click="openBookDetail(book)">
                <div class="book-cover" :style="{ background: book.color }">{{ book.icon }}</div>
                <n-tag size="small" type="warning">读中</n-tag>
                <div class="book-title">{{ book.title }}</div>
              </div>
            </div>
          </div>

          <!-- 待读书架 -->
          <div style="margin-bottom: 12px;">
            <div style="font-size: 12px; color: #666; margin-bottom: 8px;">📚 待读书架</div>
            <div class="book-row">
              <div v-for="book in pendingBooks" :key="book.id" class="book-card-small">
                <div class="book-cover-small" :style="{ background: book.color }">{{ book.icon }}</div>
                <div class="book-title-small">{{ book.title }}</div>
              </div>
            </div>
          </div>
        </n-card>

        <!-- 学富五车 -->
        <n-card title="🏆 学富五车" size="medium" style="margin-bottom: 15px;">
          <template #header-extra>
            <n-button text type="primary">查看全部 →</n-button>
          </template>
          <div class="achievement-stats">
            <div class="achievement-item">
              <div class="achievement-value">5</div>
              <div class="achievement-label">已读本书</div>
            </div>
            <div class="achievement-item">
              <div class="achievement-value">12,580</div>
              <div class="achievement-label">已读字数</div>
            </div>
          </div>
          <div class="cart-animation">
            🚶🛒📚📚📚📚📚
          </div>
        </n-card>

        <!-- 共享图书馆 -->
        <n-card title="📚 共享图书馆" size="medium" style="margin-bottom: 15px;">
          <template #header-extra>
            <n-button text type="primary">进入书库 →</n-button>
          </template>
          <div class="shared-stats">
            <div class="shared-item">
              <div class="shared-value">128</div>
              <div class="shared-label">推荐好书</div>
            </div>
            <div class="shared-item">
              <div class="shared-value">45</div>
              <div class="shared-label">可借阅</div>
            </div>
            <div class="shared-item">
              <div class="shared-value">89</div>
              <div class="shared-label">书友在读</div>
            </div>
          </div>
        </n-card>

        <!-- 书友阅读榜 -->
        <n-card title="🏆 书友阅读榜" size="medium" style="margin-bottom: 15px;">
          <template #header-extra>
            <n-button text type="primary">完整榜单 →</n-button>
          </template>
          <n-list>
            <n-list-item v-for="(ranker, index) in readingRankers" :key="ranker.id">
              <n-space align="center">
                <span class="rank-medal">{{ getMedal(index) }}</span>
                <span>{{ ranker.gender === 'girl' ? '👧' : '👦' }}</span>
                <span>{{ ranker.name }}</span>
                <n-text depth="3">{{ ranker.words }}字</n-text>
                <n-tag v-if="index === 0" size="small" type="warning">⭐本周之星</n-tag>
              </n-space>
            </n-list-item>
          </n-list>
        </n-card>

        <!-- 书友推荐 -->
        <n-card title="💝 书友推荐" size="medium" style="margin-bottom: 15px;">
          <template #header-extra>
            <n-button text type="primary">更多 →</n-button>
          </template>
          <div class="recommend-card">
            <div class="recommend-cover">🧙</div>
            <div class="recommend-info">
              <div class="recommend-title">《哈利·波特与魔法石》</div>
              <div class="recommend-meta">
                <n-rate :value="4.9" readonly size="small" />
                <span>23人推荐</span>
                <n-tag size="small" type="info">📖可借阅</n-tag>
              </div>
              <div class="recommend-readers">👧👦 小芳、小明 等5人读过</div>
              <n-button text type="primary" size="small">查看 3 条读后感 →</n-button>
            </div>
          </div>
        </n-card>

        <!-- 我的书架管理 -->
        <n-card title="📖 我的书架管理" size="medium">
          <template #header-extra>
            <n-button text type="primary">管理 →</n-button>
          </template>
          <n-space>
            <n-tag type="success">3 推荐</n-tag>
            <n-tag type="info">2 可借阅</n-tag>
            <n-tag type="warning">1 借出中</n-tag>
          </n-space>
        </n-card>
      </div>

      <!-- 错题本 -->
      <div v-show="activeTab === 'wrong'" class="page-content">
        <h2 style="margin-bottom: 20px; color: #333;">📕 错题本</h2>

        <!-- 错题统计 -->
        <n-card size="medium" style="margin-bottom: 15px;">
          <div class="wrong-stats">
            <div class="wrong-stat">
              <div class="wrong-value">12</div>
              <div class="wrong-label">本周错题</div>
            </div>
            <div class="wrong-stat">
              <div class="wrong-value success">5</div>
              <div class="wrong-label">已掌握</div>
            </div>
            <div class="wrong-stat">
              <div class="wrong-value warning">7</div>
              <div class="wrong-label">待复习</div>
            </div>
          </div>
          <n-space style="margin-top: 15px;">
            <n-tag type="info" style="cursor: pointer;">全部</n-tag>
            <n-tag style="cursor: pointer;">粗心</n-tag>
            <n-tag style="cursor: pointer;">概念不清</n-tag>
            <n-tag style="cursor: pointer;">方法错误</n-tag>
          </n-space>
        </n-card>

        <!-- 错题列表 -->
        <n-card v-for="question in wrongQuestions" :key="question.id" size="medium" style="margin-bottom: 15px;">
          <template #header>
            <n-space>
              <n-tag :type="question.subject === 'math' ? 'error' : 'info'">
                {{ question.subject === 'math' ? '🔢' : '📖' }}
              </n-tag>
              <span>{{ question.title }}</span>
            </n-space>
          </template>
          <div class="question-content">
            <p><strong>题目：</strong>{{ question.question }}</p>
            <p><strong>你的答案：</strong><n-text type="error">{{ question.userAnswer }} ❌</n-text></p>
            <p><strong>正确答案：</strong><n-text type="success">{{ question.correctAnswer }} ✅</n-text></p>
            <div class="error-reason">
              <strong>错误原因：</strong>{{ question.reason }}
            </div>
          </div>
          <template #footer>
            <n-space>
              <n-button size="small">🔄 加入复习</n-button>
              <n-button size="small" type="success">✅ 标记掌握</n-button>
            </n-space>
          </template>
        </n-card>

        <n-button type="primary" block>🖨️ 打印错题</n-button>
      </div>

      <!-- AI 出题 -->
      <div v-show="activeTab === 'ai'" class="page-content">
        <AIQuestionGen />
      </div>

      <!-- 家长专区 -->
      <div v-show="activeTab === 'parent'" class="page-content parent-zone">
        <!-- 管理员面板 -->
        <AdminDashboard v-if="activeTab === 'admin'" />
        
        <!-- 家长信息 + 切换孩子 融合卡片 -->
        <div class="parent-profile-card">
          <div class="parent-header">
            <div class="parent-left">
              <div class="parent-avatar">
                <span class="avatar-icon">{{ parentProfile.avatar }}</span>
              </div>
              <div class="parent-info">
                <div class="parent-name">{{ parentProfile.nickname }}</div>
                <div class="parent-id">ID: {{ parentProfile.id }}</div>
              </div>
            </div>
            <div class="parent-right" @click="openChildSwitch">
              <div class="switch-child-label">👶 当前孩子</div>
              <div class="current-child-info">
                <span class="child-avatar-small">{{ currentChild.gender === 'girl' ? '👧' : '👦' }}</span>
                <span class="child-name-small">{{ currentChild.nickname }}</span>
                <span class="switch-hint">切换 ›</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 分组菜单 - 扇贝风格4列网格 -->
        <div v-for="group in menuGroups" :key="group.title" class="menu-group-card">
          <div class="menu-group-header">{{ group.title }}</div>
          <div class="menu-grid-4">
            <div
              v-for="item in group.items"
              :key="item.action"
              class="menu-item-compact"
              @click="handleMenuAction(item.action)"
            >
              <div class="menu-icon-circle" :class="item.iconClass">
                <span class="icon-emoji">{{ item.icon }}</span>
              </div>
              <div class="menu-name">{{ item.title }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <BottomNav :active-key="activeTab" @change="handleNavChange" />

    <!-- 奖励商城弹窗 -->
    <RewardShop v-model:show="showRewardShop" :points="points" @exchange="handleExchange" />

    <!-- 商量奖励弹窗 -->
    <DiscussReward
      v-model:show="showDiscuss"
      :wishes="wishes"
      :parent-reply="parentReply"
      @add-wish="handleAddWish"
    />

    <!-- 智能录入弹窗 -->
    <SmartUpload
      v-model:show="showSmartUpload"
      :type="uploadType"
      @confirm="handleUploadConfirm"
    />



    <!-- 小朋友切换弹窗 -->
    <ChildSwitchModal
      v-model:show="showChildSwitch"
      :children="childrenList"
      :current-child-id="currentChild.id"
      @select="selectChild"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  NCard, NButton, NSpace, NTag,
  NList, NListItem, NText, NRate, useMessage
} from 'naive-ui'
import BottomNav from './components/BottomNav.vue'
import Spinosaurus from './components/Spinosaurus.vue'
import PointsLevel from './components/PointsLevel.vue'
import RewardShop from './components/RewardShop.vue'
import DiscussReward from './components/DiscussReward.vue'
import SmartUpload from './components/SmartUpload.vue'
import ChildSwitchModal from './components/ChildSwitchModal.vue'
import DailyPractice from './components/DailyPractice.vue'
import AIQuestionGen from './components/AIQuestionGen.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import { bindingApi } from './api'

const message = useMessage()

// 导航状态
const activeTab = ref('home')

// 恐龙组件引用
const spinosaurusRef = ref<InstanceType<typeof Spinosaurus> | null>(null)

// 小朋友信息
const currentChild = reactive({
  id: 'e756948a-b945-412f-b969-80cc326abe64',
  nickname: '乐乐',
  gender: 'girl',
  grade: '三年级',
  age: 8,
  hobbies: '🎨画画 · 📚阅读 · 🎵钢琴'
})

const currentStudentId = ref('e756948a-b945-412f-b969-80cc326abe64')

// 棘龙数据
const spinosaurus = reactive({
  level: 5,
  attack: 128,
  defense: 86,
  streakDays: 12,
  expPercent: 70,
  expToNext: 30
})

// 积分数据
const points = ref(520)

// 今日任务数据（单任务卡片滑动式）
const todayTasks = ref([
  {
    id: 1,
    icon: '📖',
    subject: 'chinese',
    subjectLabel: '语文',
    title: '古诗：静夜思',
    content: '床前明月光，\n疑是地上霜。\n举头望明月，\n低头思故乡。',
    completed: false,
    skipped: false
  },
  {
    id: 2,
    icon: '🔢',
    subject: 'math',
    subjectLabel: '数学',
    title: '口算：加法',
    content: '25 + 37 = ?\n\n提示：先算个位，再算十位',
    completed: false,
    skipped: false
  },
  {
    id: 3,
    icon: '📚',
    subject: 'reading',
    subjectLabel: '阅读',
    title: '精读：春天来了',
    content: '阅读课文，找出好词好句，\n并思考作者为什么喜欢春天。',
    completed: false,
    skipped: false
  },
  {
    id: 4,
    icon: '✍️',
    subject: 'writing',
    subjectLabel: '写字',
    title: '易错字练习：乘',
    content: '注意笔画顺序：\n撇、横、竖、横、竖、竖。',
    completed: false,
    skipped: false
  },
])

// 当前任务索引
const currentTaskIndex = ref(0)

// 完成任务数量
const completedCount = computed(() => todayTasks.value.filter(t => t.completed).length)

// 当前任务（排除已跳过的任务）
const currentTask = computed(() => {
  // 找到第一个未完成且未跳过的任务
  for (let i = 0; i < todayTasks.value.length; i++) {
    const task = todayTasks.value[i]
    if (task && !task.completed && !task.skipped) {
      currentTaskIndex.value = i
      return task
    }
  }
  return null
})

// 跳过任务
const skipTask = () => {
  const task = currentTask.value
  if (!task) return

  task.skipped = true
  message.info(`跳过「${task.title}」，下次再来吧～`)
}

// 完成任务
const completeTask = () => {
  const task = currentTask.value
  if (!task || task.completed) return

  task.completed = true
  spinosaurus.attack += 5
  points.value += 15

  // 触发恐龙成长动画
  if (spinosaurusRef.value) {
    spinosaurusRef.value.growUp(5)
  }

  message.success(`完成任务「${task.title}」！攻击力 +5，积分 +15`)
}

// 计划页数据
const todayBooks = ref(['语文书', '数学书', '英语书', '美术工具包'])
const afterSchoolActivities = ref([
  { time: '16:00', name: '点心时间', icon: '🍎', color: '#f8f9fa', location: '' },
  { time: '16:30', name: '作业时间', icon: '📚', color: '#e3f2fd', location: '预计 1h' },
  { time: '18:00', name: '每日一练', icon: '📖', color: '#f3e5f5', location: '语文+数学' },
  { time: '18:30', name: '晚餐', icon: '🍽️', color: '#fff3e0', location: '' },
  { time: '19:30', name: '美术课', icon: '🎨', color: '#e8f5e9', location: '📍 少年宫' },
  { time: '21:00', name: '洗漱睡觉', icon: '🌙', color: '#fce4ec', location: '' },
])

// 阅读页数据
const readingBooks = ref([
  { id: 1, title: '小王子', icon: '👑', color: 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%)' },
  { id: 2, title: '西游记', icon: '🐵', color: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' },
])

const pendingBooks = ref([
  { id: 3, title: '安徒生', icon: '🧜‍♀️', color: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' },
  { id: 4, title: '十万个', icon: '🔬', color: 'linear-gradient(135deg, #10b981 0%, #059669 100%)' },
  { id: 5, title: '伊索', icon: '🦊', color: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' },
  { id: 6, title: '格林', icon: '🏰', color: 'linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)' },
])

const readingRankers = ref([
  { id: 1, name: '小芳', gender: 'girl', words: '15,200' },
  { id: 2, name: '小明', gender: 'boy', words: '12,500' },
  { id: 3, name: '小红', gender: 'girl', words: '11,800' },
  { id: 4, name: '小刚', gender: 'boy', words: '9,600' },
])

// 错题数据
const wrongQuestions = ref([
  {
    id: 1,
    subject: 'math',
    title: '两位数乘法',
    question: '小明有 5 盒铅笔，每盒 12 支，一共有多少支？',
    userAnswer: '5 + 12 = 17（支）',
    correctAnswer: '5 × 12 = 60（支）',
    reason: '概念不清 - 混淆了加法和乘法的用法'
  },
  {
    id: 2,
    subject: 'chinese',
    title: '古诗填空',
    question: '床前明月光，疑是____霜。',
    userAnswer: '地上下',
    correctAnswer: '地上',
    reason: '粗心 - 多写了一个字'
  }
])

// 绑定数据
const bindings = ref<any[]>([])

// 奖励相关
const showRewardShop = ref(false)
const showDiscuss = ref(false)

// 智能录入相关
const showSmartUpload = ref(false)
const uploadType = ref<'wrong' | 'material' | 'book'>('wrong')



// 小朋友切换相关
const showChildSwitch = ref(false)
const childrenList = ref([
  {
    id: 'e756948a-b945-412f-b969-80cc326abe64',
    nickname: '乐乐',
    gender: 'girl' as const,
    grade: '三年级',
    age: 8,
    textbook: '人教版',
    hobbies: '🎨画画 · 📚阅读 · 🎵钢琴'
  },
  {
    id: 'another-child-id',
    nickname: '小明',
    gender: 'boy' as const,
    grade: '一年级',
    age: 6,
    textbook: '北师大版',
    hobbies: '🧱乐高 · ⚽足球 · 🎮游戏'
  }
])

// AI 欢迎语
const aiWelcomeMessage = computed(() => {
  const hour = new Date().getHours()
  const timeGreeting = hour < 12 ? '早上好' : hour < 18 ? '下午好' : '晚上好'
  
  const hobbies = currentChild.hobbies.split(' · ')
  const randomHobby = hobbies[Math.floor(Math.random() * hobbies.length)]
  
  const messages = [
    `今天也是充满希望的一天！${currentChild.nickname}要继续加油哦～`,
    `相信${currentChild.nickname}今天也能学到很多新知识！`,
    `每一天的努力，都会让${currentChild.nickname}变得更棒！`,
    `${timeGreeting}！${currentChild.nickname}准备好开始今天的学习了吗？`,
    `学习就像${randomHobby}一样，越练习越厉害！加油！`,
  ]
  
  return messages[Math.floor(Math.random() * messages.length)]
})

const wishes = ref([
  { id: 1, icon: '🎢', content: '想去游乐园玩一天', status: 'approved' },
  { id: 2, icon: '🎮', content: '想要一套乐高积木', status: 'pending' },
  { id: 3, icon: '🐱', content: '想养一只小猫', status: 'pending' },
])
const parentReply = ref('亲爱的宝贝，游乐园的事情爸爸答应你啦！攒够 500 积分我们就去。乐高积木妈妈觉得不错，可以作为期中考试的奖励哦～ 小猫的事情我们周末开家庭会议讨论吧！🥰')

// 家长专区数据
const parentProfile = reactive({
  nickname: '妈妈',
  id: '123456',
  streakDays: 45,
  points: 2340,
  avatar: '👤'
})

const menuGroups = [
  {
    title: '📚 学习管理',
    items: [
      { icon: '📕', title: '错题本', action: 'wrongQuestions', iconClass: 'icon-red' },
      { icon: '📝', title: '学习计划', action: 'plan', iconClass: 'icon-blue' },
      { icon: '📊', title: '学习报告', action: 'report', iconClass: 'icon-purple' },
      { icon: '📖', title: '阅读记录', action: 'reading', iconClass: 'icon-teal' },
    ]
  },
  {
    title: '🎁 奖励管理',
    items: [
      { icon: '🎁', title: '奖励商城', action: 'rewardShop', iconClass: 'icon-orange' },
      { icon: '💭', title: '商量奖励', action: 'discuss', iconClass: 'icon-pink' },
      { icon: '🏆', title: '成就徽章', action: 'achievements', iconClass: 'icon-yellow' },
      { icon: '📋', title: '愿望清单', action: 'wishes', iconClass: 'icon-indigo' },
    ]
  },
  {
    title: '⚙️ 设置',
    items: [
      { icon: '👶', title: '切换孩子', action: 'switchChild', iconClass: 'icon-cyan' },
      { icon: '👨‍👩', title: '家庭成员', action: 'family', iconClass: 'icon-green' },
      { icon: '📧', title: '绑定邮箱', action: 'email', iconClass: 'icon-blue' },
      { icon: '⚙️', title: '系统设置', action: 'settings', iconClass: 'icon-gray' },
    ]
  },
]

// 方法
const handleNavChange = (key: string) => {
  activeTab.value = key
}

// const openAdminPanel = () => {
//   activeTab.value = 'admin'
// }

const handleUploadConfirm = (data: any) => {
  message.success(`${data.type === 'wrong' ? '错题' : data.type === 'material' ? '资料' : '图书'}已成功入库！`)
  // 根据类型更新对应数据
  if (data.type === 'wrong') {
    wrongQuestions.value.unshift({
      id: Date.now(),
      subject: data.aiResult.subject === '数学' ? 'math' : 'chinese',
      title: data.aiResult.knowledgePoint,
      question: data.aiResult.content.split('\n')[0],
      userAnswer: '待填写',
      correctAnswer: '待填写',
      reason: '待分析'
    })
  }
}

const handleClick = (name: string) => {
  message.info(`打开${name}`)
}

const openChildSwitch = () => {
  showChildSwitch.value = true
}

const selectChild = (child: any) => {
  currentChild.id = child.id
  currentChild.nickname = child.nickname
  currentChild.gender = child.gender
  currentChild.grade = child.grade
  currentChild.age = child.age
  currentStudentId.value = child.id
}



const openBookDetail = (book: any) => {
  message.info(`打开《${book.title}》详情`)
}

const getMedal = (index: number) => {
  const medals = ['🥇', '🥈', '🥉']
  return medals[index] || `${index + 1}`
}

const handleExchange = (reward: any) => {
  points.value -= reward.cost
  message.success(`成功兑换「${reward.name}」！`)
}

const handleAddWish = (content: string) => {
  const icons = ['🎢', '🎮', '🐱', '🎁', '🚲', '🎸', '🎨', '📚']
  const randomIcon = icons[Math.floor(Math.random() * icons.length)] || '🎁'
  wishes.value.push({
    id: Date.now(),
    icon: randomIcon,
    content,
    status: 'pending'
  })
}

// 家长专区菜单操作
const handleMenuAction = (action: string) => {
  switch (action) {
    case 'wrongQuestions':
      activeTab.value = 'wrong'
      break
    case 'plan':
      activeTab.value = 'plan'
      break
    case 'report':
      message.info('打开学习报告')
      break
    case 'reading':
      activeTab.value = 'reading'
      break
    case 'rewardShop':
      showRewardShop.value = true
      break
    case 'discuss':
      showDiscuss.value = true
      break
    case 'achievements':
      message.info('打开成就徽章')
      break
    case 'wishes':
      showDiscuss.value = true
      break
    case 'switchChild':
      showChildSwitch.value = true
      break
    case 'family':
      message.info('打开家庭成员管理')
      break
    case 'email':
      message.info('打开绑定邮箱')
      break
    case 'settings':
      message.info('打开系统设置')
      break
    default:
      message.info(`打开${action}`)
  }
}

const loadBindings = async () => {
  const res = await bindingApi.list()
  if (res.data) {
    bindings.value = res.data
  }
}

onMounted(() => {
  loadBindings()
})
</script>

<style scoped>
/* ========== 薄荷绿主题变量 ========== */
.app-container {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --accent: #F97316;
  --accent-light: #FB923C;
  --bg-light: #F8FAFC;
  --bg-card: #FFFFFF;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.06);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.1);
  --radius-sm: 12px;
  --radius-md: 16px;
  --radius-lg: 20px;

  min-height: 100vh;
  background: var(--bg-light);
  padding-bottom: 80px;
}

.main-content {
  padding: 15px;
  max-width: 800px;
  margin: 0 auto;
}

.page-content {
  padding-top: 10px;
}

/* ========== 任务卡片区域 ========== */
.task-section {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: 18px;
  margin-bottom: 16px;
  box-shadow: var(--shadow-md);
}

.task-progress {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.progress-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

/* 任务轮播容器 */
.task-carousel {
  min-height: 320px;
  position: relative;
  overflow: hidden;
}

/* 大任务卡片 */
.task-card-large {
  background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
  border-radius: var(--radius-lg);
  padding: 24px;
  text-align: center;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.task-icon-large {
  font-size: 48px;
  margin-bottom: 12px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.task-subject-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 12px;
}

.task-subject-tag.chinese {
  background: linear-gradient(135deg, #99F6E4 0%, #5EEAD4 100%);
  color: var(--primary-dark);
}

.task-subject-tag.math {
  background: linear-gradient(135deg, #FFEDD5 0%, #FED7AA 100%);
  color: #C2410C;
}

.task-subject-tag.reading {
  background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
  color: #1E40AF;
}

.task-subject-tag.writing {
  background: linear-gradient(135deg, #FCE7F3 0%, #FBCFE8 100%);
  color: #BE185D;
}

.task-title-large {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 12px;
}

.task-content-large {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.8;
  white-space: pre-line;
  margin-bottom: 20px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: var(--radius-sm);
}

.task-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.task-actions .n-button {
  flex: 1;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
}

.skip-btn {
  background: #F1F5F9 !important;
  color: var(--text-secondary) !important;
  border: none !important;
}

.skip-btn:hover {
  background: #E2E8F0 !important;
  color: var(--text-primary) !important;
}

/* 任务完成提示 */
.task-complete {
  text-align: center;
  padding: 40px 20px;
}

.complete-icon {
  font-size: 64px;
  margin-bottom: 16px;
  animation: celebrate 0.6s ease-in-out;
}

@keyframes celebrate {
  0% { transform: scale(0); opacity: 0; }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); opacity: 1; }
}

.complete-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 8px;
}

.complete-desc {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 20px;
}

.complete-stats {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.complete-stats .stat {
  background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-dark);
}

/* 任务进度指示器 */
.task-indicators {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 16px;
}

.indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #E2E8F0;
  transition: all 0.3s ease;
}

.indicator.active {
  width: 24px;
  border-radius: 4px;
  background: var(--primary);
}

.indicator.completed {
  background: var(--primary);
}

.indicator.skipped {
  background: #CBD5E1;
}

/* 卡片滑动动画 */
.task-slide-enter-active,
.task-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.task-slide-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.task-slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

/* ========== 任务列表标题 ========== */
.task-section-title {
  margin-bottom: 16px;
  color: var(--text-primary);
  font-size: 17px;
  font-weight: 600;
}

/* ========== 子任务标签 ========== */
.sub-task-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.sub-tag {
  padding: 8px 14px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.sub-tag.chinese {
  background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%);
  color: var(--primary-dark);
}

.sub-tag.math {
  background: linear-gradient(135deg, #FFEDD5 0%, #FED7AA 100%);
  color: #C2410C;
}

/* ========== 书籍列表 ========== */
.book-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

/* ========== 课后安排 ========== */
.activity-item {
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  margin-bottom: 8px;
  font-size: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
}

.activity-item:hover {
  transform: translateX(4px);
}

/* ========== 阅读提示 ========== */
.reading-tip {
  background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%);
  border-radius: var(--radius-lg);
  padding: 18px;
  margin-bottom: 16px;
  box-shadow: var(--shadow-sm);
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}

.tip-header span:last-child {
  font-weight: 600;
  color: var(--primary-dark);
}

.reading-tip p {
  font-size: 13px;
  color: var(--primary-dark);
  line-height: 1.8;
  margin: 0;
}

/* ========== 阅读统计 ========== */
.reading-stats :deep(.n-card-header) {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.stats-value {
  font-size: 18px;
  font-weight: bold;
  color: var(--primary);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  text-align: center;
}

.stat-item {
  background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
  padding: 16px;
  border-radius: var(--radius-md);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary);
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* ========== 书架 ========== */
.book-row {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 5px;
}

.book-card {
  text-align: center;
  min-width: 70px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.book-card:hover {
  transform: scale(1.05);
}

.book-cover {
  width: 60px;
  height: 80px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin: 0 auto 6px;
  box-shadow: var(--shadow-md);
}

.book-title {
  font-size: 12px;
  color: var(--text-primary);
  margin-top: 4px;
  font-weight: 500;
}

.book-card-small {
  text-align: center;
  min-width: 55px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.book-card-small:hover {
  transform: scale(1.05);
}

.book-cover-small {
  width: 45px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin: 0 auto 4px;
  box-shadow: var(--shadow-sm);
}

.book-title-small {
  font-size: 10px;
  color: var(--text-secondary);
}

/* ========== 学富五车 ========== */
.achievement-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.achievement-item {
  text-align: center;
}

.achievement-value {
  font-size: 28px;
  font-weight: bold;
  color: var(--primary);
}

.achievement-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.cart-animation {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border-radius: var(--radius-md);
  padding: 16px;
  text-align: center;
  font-size: 36px;
}

/* ========== 共享图书馆统计 ========== */
.shared-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  text-align: center;
}

.shared-item {
  background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%);
  padding: 14px;
  border-radius: var(--radius-md);
  transition: all 0.3s ease;
}

.shared-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.shared-value {
  font-size: 20px;
  font-weight: bold;
  color: var(--primary);
}

.shared-label {
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* ========== 排名 ========== */
.rank-medal {
  font-size: 18px;
}

/* ========== 推荐 ========== */
.recommend-card {
  display: flex;
  gap: 14px;
  background: linear-gradient(135deg, #F0FDFA 0%, #ECFDF5 100%);
  border-radius: var(--radius-md);
  padding: 14px;
}

.recommend-cover {
  width: 50px;
  height: 70px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.recommend-info {
  flex: 1;
}

.recommend-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.recommend-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.recommend-readers {
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 6px;
}

/* ========== 错题统计 ========== */
.wrong-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  text-align: center;
}

.wrong-stat {
  padding: 14px;
  background: #F8FAFC;
  border-radius: var(--radius-sm);
}

.wrong-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary);
}

.wrong-value.success {
  color: #10B981;
}

.wrong-value.warning {
  color: var(--accent);
}

.wrong-label {
  font-size: 12px;
  color: var(--text-secondary);
}

/* ========== 错题内容 ========== */
.question-content {
  font-size: 13px;
  line-height: 1.8;
}

.error-reason {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  padding: 12px;
  border-radius: var(--radius-sm);
  margin-top: 12px;
}

/* ========== 其他 ========== */
.section-desc {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.upload-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: var(--radius-md);
}

.upload-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary-light);
}

.upload-card :deep(.n-text) {
  display: block;
}

/* AI 欢迎语卡片 */
.ai-welcome-card {
  background: linear-gradient(135deg, #14B8A6 0%, #2DD4BF 50%, #5EEAD4 100%);
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25);
  color: white;
}

.welcome-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.welcome-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
  backdrop-filter: blur(4px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.welcome-text {
  flex: 1;
}

.welcome-greeting {
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 4px;
}

.welcome-message {
  font-size: 13px;
  opacity: 0.95;
  line-height: 1.5;
}

.welcome-interests {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.welcome-interests .n-tag {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.welcome-interests .n-tag:hover {
  background: rgba(255, 255, 255, 0.35);
}

/* ========== 家长专区样式 ========== */
.parent-zone {
  padding-top: 0;
  background: #F8FAFC;
  min-height: 100vh;
  margin: -16px -16px 0 -16px;
  padding: 16px;
}

.parent-profile-card {
  background: linear-gradient(135deg, #14B8A6 0%, #2DD4BF 100%);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.25);
  color: white;
}

.parent-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.parent-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.parent-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
  backdrop-filter: blur(4px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.avatar-icon {
  margin-top: 2px;
}

.parent-info {
  flex: 1;
}

.parent-name {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 4px;
}

.parent-id {
  font-size: 12px;
  opacity: 0.9;
}

.parent-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  cursor: pointer;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  transition: all 0.3s;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.parent-right:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.switch-child-label {
  font-size: 11px;
  opacity: 0.9;
  margin-bottom: 6px;
}

.current-child-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.child-avatar-small {
  font-size: 20px;
}

.child-name-small {
  font-size: 14px;
  font-weight: 600;
}

.switch-hint {
  font-size: 12px;
  opacity: 0.8;
  margin-left: 4px;
}

/* 扇贝风格菜单组卡片 */
.menu-group-card {
  background: white;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.menu-group-header {
  font-size: 14px;
  font-weight: 600;
  color: #64748B;
  margin-bottom: 16px;
  padding-left: 4px;
}

/* 4列网格布局 */
.menu-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.menu-item-compact {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 8px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.menu-item-compact:hover {
  background: #F8FAFC;
  transform: translateY(-2px);
}

.menu-item-compact:active {
  transform: scale(0.95);
}

/* 圆形渐变图标 */
.menu-icon-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
  transition: transform 0.2s ease;
}

.menu-item-compact:hover .menu-icon-circle {
  transform: scale(1.1);
}

.icon-emoji {
  font-size: 22px;
}

.menu-name {
  font-size: 13px;
  color: #334155;
  font-weight: 500;
  text-align: center;
  line-height: 1.3;
}

/* 图标渐变色背景 - 薄荷绿主题配色 */
.icon-red {
  background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
}

.icon-blue {
  background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
}

.icon-purple {
  background: linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%);
}

.icon-teal {
  background: linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%);
}

.icon-orange {
  background: linear-gradient(135deg, #FED7AA 0%, #FDBA74 100%);
}

.icon-pink {
  background: linear-gradient(135deg, #FCE7F3 0%, #FBCFE8 100%);
}

.icon-yellow {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
}

.icon-indigo {
  background: linear-gradient(135deg, #E0E7FF 0%, #C7D2FE 100%);
}

.icon-cyan {
  background: linear-gradient(135deg, #CFFAFE 0%, #A5F3FC 100%);
}

.icon-green {
  background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%);
}

.icon-gray {
  background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
}

/* 响应式调整 */
@media (max-width: 360px) {
  .menu-grid-4 {
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
  }

  .menu-item-compact {
    padding: 10px 4px;
  }

  .menu-icon-circle {
    width: 40px;
    height: 40px;
  }

  .icon-emoji {
    font-size: 20px;
  }

  .menu-name {
    font-size: 12px;
  }
}
</style>