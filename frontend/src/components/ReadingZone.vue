<template>
  <div class="reading-zone">
    <!-- 阅读统计 + 学富五车 + AI 劝读 -->
    <div class="reading-stats-card">
      <!-- 左侧统计数据 -->
      <div class="stats-left">
        <div class="stat-row">
          <div class="stat-item">
            <div class="stat-icon">📖</div>
            <div class="stat-value">{{ stats.completedBooks }}</div>
            <div class="stat-label">已读</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">🔥</div>
            <div class="stat-value">{{ stats.readingBooks }}</div>
            <div class="stat-label">在读</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">📝</div>
            <div class="stat-value">{{ stats.totalWords }}</div>
            <div class="stat-label">字数</div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">⭐</div>
            <div class="stat-value">{{ stats.points }}</div>
            <div class="stat-label">积分</div>
          </div>
        </div>
      </div>

      <!-- 右侧学富五车动画 + AI 劝读 -->
      <div class="stats-right">
        <div class="mountain-library">
          <!-- 上半部分：学富五车动画 -->
          <div class="mountain-top">
            <div class="mountain-title">📚 学富五车</div>
            <div class="mountain-scene">
              <!-- 书山背景 -->
              <div class="book-mountain">
                <!-- 山体层叠 -->
                <div class="mountain-layer layer-1"></div>
                <div class="mountain-layer layer-2"></div>
                <div class="mountain-layer layer-3"></div>
                
                <!-- 书籍装饰 -->
                <div class="floating-book book-1">📕</div>
                <div class="floating-book book-2">📗</div>
                <div class="floating-book book-3">📘</div>
                <div class="floating-book book-4">📙</div>
                
                <!-- 路径 -->
                <div class="knowledge-path"></div>
                
                <!-- 山顶光芒 -->
                <div class="mountain-glow"></div>
              </div>
              
              <!-- 已读数量展示 -->
              <div class="completed-count">
                <span class="count-number">{{ stats.completedBooks }}</span>
                <span class="count-label">本</span>
              </div>
            </div>
          </div>
          
          <!-- 下半部分：AI 劝读 -->
          <div class="ai-quote-mini">
            <div class="quote-mini-header">
              <span class="quote-mini-icon">✨</span>
              <span class="quote-mini-label">AI 姐姐说</span>
              <n-button size="tiny" text @click="refreshQuote" :loading="quoteLoading">
                🔄
              </n-button>
            </div>
            <div class="quote-mini-content" v-if="!quoteLoading">
              {{ currentQuote }}
            </div>
            <div class="quote-mini-loading" v-else>
              思考中...
            </div>
          </div>
          
          <div class="mountain-poem">书山有路勤为径</div>
        </div>
      </div>
    </div>

    <!-- 我的书架 - 真实书架效果 -->
    <div class="bookshelf-section">
      <div class="section-header">
        <h2 class="section-title">📚 我的书架</h2>
        <n-button text type="primary" size="small" @click="showAddBook = true">
          + 添加图书
        </n-button>
      </div>

      <!-- 书架层板 -->
      <div class="bookshelf">
        <!-- 正在阅读 -->
        <div class="bookshelf-row">
          <div class="shelf-label">
            <span class="shelf-icon">🔥</span>
            <span>正在阅读</span>
          </div>
          <div class="shelf-books">
            <div 
              v-for="book in readingBooks" 
              :key="book.id"
              class="book-spine"
              :style="{ background: book.color }"
              @click="openBook(book)">
              <div class="spine-title">{{ book.title }}</div>
              <div class="spine-progress">
                <div class="progress-bar" :style="{ width: book.progress + '%' }"></div>
              </div>
              <div class="spine-percent">{{ book.progress }}%</div>
            </div>
            <!-- 空书架提示 -->
            <div v-if="readingBooks.length === 0" class="empty-shelf">
              还没有正在阅读的书籍
            </div>
          </div>
        </div>

        <!-- 待读书架 -->
        <div class="bookshelf-row">
          <div class="shelf-label">
            <span class="shelf-icon">📖</span>
            <span>待读</span>
          </div>
          <div class="shelf-books">
            <div 
              v-for="book in toReadBooks" 
              :key="book.id"
              class="book-spine to-read"
              :style="{ background: book.color }"
              @click="startReading(book)">
              <div class="spine-title">{{ book.title }}</div>
              <div class="spine-action">点击开始</div>
            </div>
            <div v-if="toReadBooks.length === 0" class="empty-shelf">
              待读书架为空
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 书友推荐 - 简化为点击弹出 -->
    <div class="recommend-section">
      <div class="section-header">
        <h2 class="section-title">👥 书友推荐</h2>
        <n-button text size="small" @click="showRecommendations = true">
          查看全部 ›
        </n-button>
      </div>
      
      <div class="recommend-preview">
        <div 
          v-for="book in recommendations.slice(0, 3)" 
          :key="book.id"
          class="recommend-item"
          @click="showRecommendations = true">
          <div class="recommend-cover" :style="{ background: book.color }">
            {{ book.emoji }}
          </div>
          <div class="recommend-info">
            <div class="recommend-title">{{ book.title }}</div>
            <div class="recommend-meta">
              <span class="recommend-hot">🔥 {{ book.readers }}人在读</span>
              <span class="recommend-score">⭐ {{ book.score }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 阅读目标进度 -->
    <div class="goal-section">
      <div class="section-header">
        <h2 class="section-title">🎯 本月目标</h2>
      </div>
      <div class="goal-card">
        <div class="goal-info">
          <div class="goal-value">{{ stats.totalWords }} / {{ stats.monthlyGoal }}</div>
          <div class="goal-label">已读字数</div>
        </div>
        <div class="goal-percent">{{ readingProgress }}%</div>
      </div>
      <n-progress 
        type="line" 
        :percentage="readingProgress" 
        :indicator-placement="'inside'"
        :height="8"
        :border-radius="4"
        style="margin-top: 12px;">
        加油！坚持就是胜利～
      </n-progress>
    </div>

    <!-- 书友推荐弹窗 -->
    <n-modal 
      v-model:show="showRecommendations" 
      preset="card" 
      title="👥 书友推荐"
      class="recommend-modal"
      :style="{ maxWidth: '500px' }">
      <div class="recommend-list">
        <div 
          v-for="book in recommendations" 
          :key="book.id"
          class="recommend-item-full"
          @click="openBook(book)">
          <div class="recommend-cover-large" :style="{ background: book.color }">
            {{ book.emoji }}
          </div>
          <div class="recommend-detail">
            <div class="recommend-title-large">{{ book.title }}</div>
            <div class="recommend-desc">{{ book.description }}</div>
            <div class="recommend-meta-full">
              <span>🔥 {{ book.readers }}人在读</span>
              <span>⭐ {{ book.score }}分</span>
            </div>
          </div>
          <n-button size="small" type="primary" @click.stop="startReading(book)">
            开始阅读
          </n-button>
        </div>
      </div>
    </n-modal>

    <!-- 添加图书弹窗 -->
    <n-modal v-model:show="showAddBook" preset="card" title="➕ 添加图书">
      <n-form>
        <n-form-item label="书名">
          <n-input placeholder="请输入书名" />
        </n-form-item>
        <n-form-item label="作者">
          <n-input placeholder="请输入作者" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddBook = false">取消</n-button>
          <n-button type="primary">添加</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { NButton, NModal, NProgress, NSpace, NInput, useMessage } from 'naive-ui'

const message = useMessage()

// AI 劝读文案
const quotePresets = [
  '阅读就像给大脑吃糖果！每读一本书，你的小脑瓜就会变得更聪明一点点～今天想探索什么故事呢？',
  '高尔基说"书籍是人类进步的阶梯"。宝贝，你今天的阶梯铺好了吗？一步一步来，妈妈陪着你！',
  '打开一本书，就像推开一扇魔法门！门后有会说话的动物、勇敢的英雄、还有无限的可能～',
  '你知道吗？每本书都是一颗种子。你现在读的每一页，都会在未来长成参天大树！🌳',
  '阅读是最便宜的旅行！不用买机票，就能去任何想去的地方。今天想去哪里冒险呢？',
  '古人说"读书破万卷，下笔如有神"。你现在读的每一本书，都会让明天的你更厉害！',
  '书籍是时间的魔法盒！打开它，你可以和古代的人对话，可以去未来世界探险～',
  '阅读就像交朋友。每读一本书，你就多了一个智慧的朋友。今天想认识哪位新朋友呢？',
]

const currentQuote = ref('')
const quoteLoading = ref(false)
let quoteIndex = 0

const getRandomQuote = () => {
  const randomIndex = Math.floor(Math.random() * quotePresets.length)
  currentQuote.value = quotePresets[randomIndex] || ''
  quoteIndex = randomIndex
}

const refreshQuote = () => {
  quoteLoading.value = true
  setTimeout(() => {
    let newIndex = Math.floor(Math.random() * quotePresets.length)
    while (newIndex === quoteIndex && quotePresets.length > 1) {
      newIndex = Math.floor(Math.random() * quotePresets.length)
    }
    currentQuote.value = quotePresets[newIndex] || ''
    quoteIndex = newIndex
    quoteLoading.value = false
  }, 500)
}

onMounted(() => {
  getRandomQuote()
})

// 阅读数据
const stats = ref({
  totalWords: 12580,
  completedBooks: 5,
  readingBooks: 2,
  points: 280,
  monthlyGoal: 20000,
})

const readingProgress = computed(() => {
  return Math.min(Math.round((stats.value.totalWords / stats.value.monthlyGoal) * 100), 100)
})

// 书架数据
const readingBooks = ref([
  { id: 1, title: '夏洛的网', color: 'linear-gradient(180deg, #34D399 0%, #10B981 100%)', progress: 65, emoji: '🕸️' },
  { id: 2, title: '小王子', color: 'linear-gradient(180deg, #FCD34D 0%, #F59E0B 100%)', progress: 30, emoji: '🤴' },
])

const toReadBooks = ref([
  { id: 3, title: '哈利·波特', color: 'linear-gradient(180deg, #60A5FA 0%, #3B82F6 100%)', emoji: '🧙' },
  { id: 4, title: '绿野仙踪', color: 'linear-gradient(180deg, #4ADE80 0%, #22C55E 100%)', emoji: '🌈' },
  { id: 5, title: '安徒生童话', color: 'linear-gradient(180deg, #F472B6 0%, #EC4899 100%)', emoji: '🧚' },
])

const recommendations = ref([
  { 
    id: 9, 
    title: '神奇树屋', 
    color: 'linear-gradient(180deg, #10B981 0%, #059669 100%)', 
    emoji: '🌳',
    readers: 12580,
    score: 4.9,
    description: '穿越时空的冒险故事，知识与趣味并存！'
  },
  { 
    id: 10, 
    title: '窗边的小豆豆', 
    color: 'linear-gradient(180deg, #FCD34D 0%, #F59E0B 100%)', 
    emoji: '👧',
    readers: 9876,
    score: 4.8,
    description: '温暖治愈的成长故事，感动无数人！'
  },
  { 
    id: 11, 
    title: '昆虫记', 
    color: 'linear-gradient(180deg, #4ADE80 0%, #22C55E 100%)', 
    emoji: '🐛',
    readers: 7654,
    score: 4.7,
    description: '探索奇妙的昆虫世界，科普经典！'
  },
])

const showRecommendations = ref(false)
const showAddBook = ref(false)

const openBook = (book: any) => {
  message.info(`打开《${book.title}》`)
}

const startReading = (book: any) => {
  message.success(`开始阅读《${book.title}》`)
}
</script>

<style scoped>
.reading-zone {
  padding: 16px;
  padding-bottom: 80px;
  background: #F8FAFC;
  min-height: 100vh;
}

/* AI 劝读卡片 */
.ai-quote-card {
  background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 50%, #6EE7B7 100%);
  border-radius: 20px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
}

.quote-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.quote-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 600;
  color: #065F46;
}

.quote-icon {
  font-size: 18px;
}

.quote-content {
  font-size: 14px;
  line-height: 2;
  color: #047857;
  background: rgba(255, 255, 255, 0.6);
  padding: 12px 16px;
  border-radius: 12px;
}

.quote-loading {
  font-size: 14px;
  color: #059669;
  text-align: center;
  padding: 20px;
}

/* 阅读统计 + 学富五车 + AI 劝读 */
.reading-stats-card {
  display: flex;
  gap: 16px;
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.stats-left {
  flex: 1;
}

.stat-row {
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.stat-item {
  text-align: center;
}

.stat-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: #1E293B;
}

.stat-label {
  font-size: 12px;
  color: #64748B;
  margin-top: 2px;
}

/* 学富五车 - 书山有路勤为径 */
.stats-right {
  width: 280px;
  flex-shrink: 0;
}

.mountain-library {
  background: linear-gradient(180deg, #F0F9FF 0%, #E0F2FE 100%);
  border-radius: 12px;
  padding: 12px;
  height: 220px;
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(20, 184, 166, 0.2);
  display: flex;
  flex-direction: column;
}

.mountain-top {
  flex: 1;
  position: relative;
}

.mountain-title {
  font-size: 13px;
  font-weight: 600;
  color: #0D9488;
  text-align: center;
  margin-bottom: 4px;
}

.mountain-scene {
  position: relative;
  height: 110px;
}

/* 书山 */
.book-mountain {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 140px;
  height: 80px;
}

/* 山体层叠 */
.mountain-layer {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 50% 50% 0 0;
}

.layer-1 {
  width: 140px;
  height: 60px;
  background: linear-gradient(180deg, #14B8A6 0%, #0D9488 100%);
  z-index: 1;
}

.layer-2 {
  width: 100px;
  height: 45px;
  background: linear-gradient(180deg, #2DD4BF 0%, #14B8A6 100%);
  bottom: 15px;
  z-index: 2;
}

.layer-3 {
  width: 60px;
  height: 30px;
  background: linear-gradient(180deg, #5EEAD4 0%, #2DD4BF 100%);
  bottom: 30px;
  z-index: 3;
}

/* 漂浮的书籍 */
.floating-book {
  position: absolute;
  font-size: 14px;
  animation: float 3s ease-in-out infinite;
}

.book-1 {
  top: 10px;
  left: 10px;
  animation-delay: 0s;
}

.book-2 {
  top: 20px;
  right: 15px;
  animation-delay: 0.5s;
}

.book-3 {
  top: 35px;
  left: 20px;
  animation-delay: 1s;
}

.book-4 {
  top: 15px;
  right: 35px;
  animation-delay: 1.5s;
}

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-5px) rotate(5deg); }
}

/* 知识路径 */
.knowledge-path {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 40px;
  background: linear-gradient(180deg, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0.1) 100%);
  border-radius: 0 0 40px 40px;
  z-index: 4;
}

/* 山顶光芒 */
.mountain-glow {
  position: absolute;
  top: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: radial-gradient(circle, rgba(251, 191, 36, 0.6) 0%, transparent 70%);
  border-radius: 50%;
  animation: glow 2s ease-in-out infinite;
  z-index: 5;
}

@keyframes glow {
  0%, 100% { opacity: 0.6; transform: translateX(-50%) scale(1); }
  50% { opacity: 1; transform: translateX(-50%) scale(1.2); }
}

/* 已读数量 */
.completed-count {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  text-align: center;
}

.count-number {
  font-size: 32px;
  font-weight: 700;
  color: #0D9488;
  display: block;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.8);
}

.count-label {
  font-size: 12px;
  color: #0D9488;
  font-weight: 600;
}

/* AI 劝读迷你版 */
.ai-quote-mini {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 8px;
  padding: 8px 10px;
  margin-top: 8px;
  border: 1px solid rgba(20, 184, 166, 0.2);
}

.quote-mini-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.quote-mini-icon {
  font-size: 14px;
  margin-right: 4px;
}

.quote-mini-label {
  font-size: 12px;
  font-weight: 600;
  color: #0D9488;
  flex: 1;
}

.quote-mini-content {
  font-size: 11px;
  line-height: 1.6;
  color: #047857;
  max-height: 44px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.quote-mini-loading {
  font-size: 11px;
  color: #059669;
  text-align: center;
  padding: 4px 0;
}

.mountain-poem {
  font-size: 10px;
  color: #64748B;
  text-align: center;
  margin-top: 6px;
  font-style: italic;
}

/* 书架区域 */
.bookshelf-section {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
  margin: 0;
}

/* 真实书架效果 */
.bookshelf {
  background: linear-gradient(180deg, #F5F5DC 0%, #E8E4C9 100%);
  border-radius: 12px;
  padding: 16px;
  border: 2px solid #D4C9A8;
  box-shadow: 
    inset 0 2px 4px rgba(255, 255, 255, 0.5),
    inset 0 -2px 4px rgba(0, 0, 0, 0.1),
    0 4px 8px rgba(0, 0, 0, 0.1);
}

.bookshelf-row {
  margin-bottom: 16px;
}

.bookshelf-row:last-child {
  margin-bottom: 0;
}

.shelf-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #8B7355;
  margin-bottom: 12px;
  padding-left: 4px;
}

.shelf-icon {
  font-size: 15px;
}

.shelf-books {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 8px 4px;
  background: linear-gradient(180deg, #E8E4C9 0%, #D4C9A8 100%);
  border-radius: 8px;
  border-bottom: 4px solid #C4B59A;
}

/* 书脊样式 */
.book-spine {
  flex-shrink: 0;
  width: 60px;
  height: 100px;
  border-radius: 4px 4px 0 0;
  padding: 8px 6px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  box-shadow: 
    inset 2px 0 4px rgba(255, 255, 255, 0.3),
    inset -2px 0 4px rgba(0, 0, 0, 0.2),
    2px 2px 4px rgba(0, 0, 0, 0.2);
}

.book-spine:hover {
  transform: translateY(-4px);
  box-shadow: 
    inset 2px 0 4px rgba(255, 255, 255, 0.4),
    inset -2px 0 4px rgba(0, 0, 0, 0.2),
    4px 4px 8px rgba(0, 0, 0, 0.3);
}

.spine-title {
  font-size: 11px;
  font-weight: 600;
  color: white;
  text-align: center;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.3;
}

.spine-progress {
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: white;
  border-radius: 2px;
  transition: width 0.3s;
}

.spine-percent {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  font-weight: 600;
}

.spine-action {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.8);
  text-align: center;
  font-weight: 500;
}

.empty-shelf {
  font-size: 13px;
  color: #94A3B8;
  padding: 20px;
  text-align: center;
  width: 100%;
}

/* 书友推荐 */
.recommend-section {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.recommend-preview {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommend-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #F8FAFC;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.recommend-item:hover {
  background: #F1F5F9;
  transform: translateX(4px);
}

.recommend-cover {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex-shrink: 0;
}

.recommend-info {
  flex: 1;
  min-width: 0;
}

.recommend-title {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 4px;
}

.recommend-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #64748B;
}

.recommend-hot {
  color: #F97316;
}

.recommend-score {
  color: #FBBF24;
}

/* 阅读目标 */
.goal-section {
  background: white;
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.goal-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.08) 0%, rgba(45, 212, 191, 0.08) 100%);
  border: 1px solid rgba(20, 184, 166, 0.2);
  border-radius: 12px;
  padding: 16px;
}

.goal-info {
  flex: 1;
}

.goal-value {
  font-size: 24px;
  font-weight: 700;
  color: #0D9488;
  margin-bottom: 4px;
}

.goal-label {
  font-size: 13px;
  color: #64748B;
}

.goal-percent {
  font-size: 28px;
  font-weight: 700;
  color: #14B8A6;
}

/* 推荐弹窗 */
.recommend-modal :deep(.n-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #E2E8F0;
}

.recommend-modal :deep(.n-card__content) {
  padding: 16px 20px;
}

.recommend-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommend-item-full {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #F8FAFC;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.recommend-item-full:hover {
  background: #F1F5F9;
}

.recommend-cover-large {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.recommend-detail {
  flex: 1;
  min-width: 0;
}

.recommend-title-large {
  font-size: 15px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 4px;
}

.recommend-desc {
  font-size: 13px;
  color: #64748B;
  margin-bottom: 6px;
  line-height: 1.4;
}

.recommend-meta-full {
  display: flex;
  gap: 12px;
  font-size: 12px;
}

.recommend-meta-full span:first-child {
  color: #F97316;
}

.recommend-meta-full span:last-child {
  color: #FBBF24;
}
</style>
