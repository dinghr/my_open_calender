<template>
  <div class="reading-recommend">
    <!-- 今日精读卡片 -->
    <n-card class="recommend-card" :bordered="false">
      <template #header>
        <div class="card-header">
          <div class="header-icon">
            <span class="icon-emoji">📚</span>
          </div>
          <span class="header-title">今日精读</span>
          <n-tag type="success" size="small" v-if="completed">
            已完成
          </n-tag>
          <n-tag type="warning" size="small" v-else>
            待阅读
          </n-tag>
        </div>
      </template>

      <!-- 加载状态 -->
      <div class="loading-section" v-if="loading">
        <n-spin size="medium" />
        <p class="loading-text">正在为你生成精读材料...</p>
      </div>

      <!-- 精读内容 -->
      <div class="recommend-content" v-else>
        <!-- 标题 -->
        <div class="title-section">
          <h3 class="content-title">{{ recommendData.title }}</h3>
          <span class="word-count">约 {{ recommendData.word_count }} 字</span>
        </div>

        <!-- 正文带拼音 -->
        <div class="content-section">
          <div class="content-text">
            <span
              v-for="(item, index) in recommendData.content_pinyin"
              :key="index"
              class="char-with-pinyin"
              @click="showCharInfo(item)"
            >
              <span class="pinyin">{{ item.pinyin }}</span>
              <span class="char">{{ item.char }}</span>
            </span>
          </div>
        </div>

        <!-- 语言解析 -->
        <div class="analysis-section">
          <div class="analysis-header">
            <span class="analysis-icon">💡</span>
            <span class="analysis-title">精读解析</span>
          </div>

          <!-- 成语 -->
          <div class="analysis-item" v-if="recommendData.analysis?.idioms?.length > 0">
            <div class="analysis-label">成语</div>
            <div class="analysis-list">
              <div class="analysis-card" v-for="item in recommendData.analysis.idioms" :key="item.text">
                <span class="highlight-text">{{ item.text }}</span>
                <p class="analysis-meaning">{{ item.meaning }}</p>
                <p class="analysis-guide">👉 {{ item.guide }}</p>
              </div>
            </div>
          </div>

          <!-- 固定句式 -->
          <div class="analysis-item" v-if="recommendData.analysis?.sentence_patterns?.length > 0">
            <div class="analysis-label">固定句式</div>
            <div class="analysis-list">
              <div class="analysis-card" v-for="item in recommendData.analysis.sentence_patterns" :key="item.text">
                <span class="highlight-text">{{ item.text }}</span>
                <p class="analysis-structure">结构：{{ item.structure }}</p>
                <p class="analysis-guide">👉 {{ item.guide }}</p>
              </div>
            </div>
          </div>

          <!-- 比喻 -->
          <div class="analysis-item" v-if="recommendData.analysis?.metaphors?.length > 0">
            <div class="analysis-label">比喻</div>
            <div class="analysis-list">
              <div class="analysis-card" v-for="item in recommendData.analysis.metaphors" :key="item.text">
                <span class="highlight-text">{{ item.text }}</span>
                <p class="analysis-meaning">把「{{ item.source }}」比作「{{ item.target }}」</p>
                <p class="analysis-guide">👉 {{ item.guide }}</p>
              </div>
            </div>
          </div>

          <!-- 形容词 -->
          <div class="analysis-item" v-if="recommendData.analysis?.adjectives?.length > 0">
            <div class="analysis-label">形容词</div>
            <div class="analysis-list">
              <div class="analysis-card" v-for="item in recommendData.analysis.adjectives" :key="item.text">
                <span class="highlight-text">{{ item.text }}</span>
                <p class="analysis-meaning">{{ item.meaning }}（{{ item.feeling }}）</p>
                <p class="analysis-guide">👉 {{ item.guide }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 模仿说话 -->
        <div class="imitation-section">
          <div class="imitation-header">
            <span class="imitation-icon">🎯</span>
            <span class="imitation-title">模仿说话</span>
          </div>
          <div class="imitation-list">
            <div class="imitation-item" v-for="(prompt, idx) in recommendData.imitation_prompts" :key="idx">
              <span class="imitation-number">{{ (idx as number) + 1 }}</span>
              <span class="imitation-text">{{ prompt }}</span>
            </div>
          </div>
        </div>

        <!-- 阅读小贴士 -->
        <div class="tip-section" v-if="recommendData.reading_tip">
          <div class="tip-header">
            <span class="tip-icon">📝</span>
            <span class="tip-title">给家长的建议</span>
          </div>
          <p class="tip-content">{{ recommendData.reading_tip }}</p>
        </div>

        <!-- 操作按钮 -->
        <div class="action-section">
          <n-button
            type="primary"
            class="action-btn complete-btn"
            @click="handleComplete"
            :disabled="completed"
            :loading="completing"
          >
            <template #icon>
              <span>✅</span>
            </template>
            完成精读
          </n-button>
          <n-button
            class="action-btn refresh-btn"
            @click="handleRefresh"
            :loading="refreshing"
          >
            <template #icon>
              <span>🔄</span>
            </template>
            换一篇
          </n-button>
        </div>
      </div>
    </n-card>

    <!-- 完成奖励弹窗 -->
    <n-modal v-model:show="showRewardModal" preset="card" :style="{ width: '320px' }">
      <div class="reward-modal">
        <div class="reward-icon">🎉</div>
        <h3 class="reward-title">精读完成！</h3>
        <div class="reward-items">
          <div class="reward-item">
            <span class="reward-emoji">⭐</span>
            <span class="reward-text">+20 积分</span>
          </div>
          <div class="reward-item">
            <span class="reward-emoji">🦕</span>
            <span class="reward-text">棘龙 +10 经验</span>
          </div>
        </div>
        <n-button type="primary" block @click="showRewardModal = false">
          太棒了！
        </n-button>
      </div>
    </n-modal>

    <!-- 字符详情弹窗 -->
    <n-modal v-model:show="showCharModal" preset="card" :style="{ width: '200px' }">
      <div class="char-modal">
        <div class="char-display">{{ currentChar.char }}</div>
        <div class="char-pinyin">{{ currentChar.pinyin }}</div>
      </div>
    </n-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NCard, NTag, NSpin, NButton, NModal, useMessage } from 'naive-ui'
import { readingRecommendApi } from '../api'

const props = defineProps<{
  studentId: string
}>()

const message = useMessage()

const loading = ref(true)
const refreshing = ref(false)
const completing = ref(false)
const completed = ref(false)
const showRewardModal = ref(false)
const showCharModal = ref(false)

const recommendData = ref<any>({
  title: '',
  content: '',
  content_pinyin: [],
  word_count: 0,
  analysis: {
    idioms: [],
    sentence_patterns: [],
    metaphors: [],
    adjectives: []
  },
  imitation_prompts: [],
  reading_tip: '',
  grade: 1,
  semester: '下学期'
})

const currentChar = ref<any>({ char: '', pinyin: '' })

const loadRecommend = async () => {
  loading.value = true
  try {
    const res = await readingRecommendApi.get(props.studentId)
    if (res.data) {
      recommendData.value = res.data
    }
  } catch (error: any) {
    message.error('获取精读推荐失败：' + error.message)
  } finally {
    loading.value = false
  }
}

const handleRefresh = async () => {
  refreshing.value = true
  try {
    const res = await readingRecommendApi.new(props.studentId)
    if (res.data) {
      recommendData.value = res.data
      message.success('已换一篇新的精读材料')
    }
  } catch (error: any) {
    message.error('换一篇失败：' + error.message)
  } finally {
    refreshing.value = false
  }
}

const handleComplete = async () => {
  completing.value = true
  try {
    const res = await readingRecommendApi.complete(props.studentId, {
      duration_minutes: 5,
      liked: true
    })
    if (res.data) {
      completed.value = true
      showRewardModal.value = true
    }
  } catch (error: any) {
    message.error('完成失败：' + error.message)
  } finally {
    completing.value = false
  }
}

const showCharInfo = (item: any) => {
  if (item.pinyin) {
    currentChar.value = item
    showCharModal.value = true
  }
}

onMounted(() => {
  loadRecommend()
})
</script>

<style scoped>
.reading-recommend {
  margin-bottom: 16px;
}

.recommend-card {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --accent: #F97316;
  --bg-light: #F8FAFC;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  border-radius: 16px;
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #F97316 0%, #FB923C 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-emoji {
  font-size: 18px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
}

/* 加载状态 */
.loading-section {
  text-align: center;
  padding: 40px 20px;
}

.loading-text {
  margin-top: 12px;
  font-size: 14px;
  color: var(--text-secondary);
}

/* 标题区 */
.title-section {
  margin-bottom: 16px;
}

.content-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 4px;
}

.word-count {
  font-size: 12px;
  color: var(--text-secondary);
}

/* 正文区 - 带拼音 */
.content-section {
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid rgba(251, 191, 36, 0.3);
}

.content-text {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  line-height: 2.2;
}

.char-with-pinyin {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  padding: 2px 4px;
  border-radius: 4px;
  transition: background 0.2s;
}

.char-with-pinyin:hover {
  background: rgba(255, 255, 255, 0.5);
}

.pinyin {
  font-size: 10px;
  color: #B45309;
  line-height: 1;
}

.char {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
}

/* 解析区 */
.analysis-section {
  background: var(--bg-light);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.analysis-icon {
  font-size: 18px;
}

.analysis-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.analysis-item {
  margin-bottom: 12px;
}

.analysis-item:last-child {
  margin-bottom: 0;
}

.analysis-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 8px;
}

.analysis-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.analysis-card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  border: 1px solid #E2E8F0;
}

.highlight-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent);
  display: inline-block;
  padding: 2px 8px;
  background: rgba(249, 115, 22, 0.1);
  border-radius: 4px;
  margin-bottom: 4px;
}

.analysis-meaning,
.analysis-structure {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 4px 0;
}

.analysis-guide {
  font-size: 13px;
  color: #059669;
  margin-top: 6px;
}

/* 模仿说话 */
.imitation-section {
  background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.imitation-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.imitation-icon {
  font-size: 18px;
}

.imitation-title {
  font-size: 15px;
  font-weight: 600;
  color: #065F46;
}

.imitation-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.imitation-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 8px;
  padding: 10px;
}

.imitation-number {
  width: 20px;
  height: 20px;
  background: #10B981;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.imitation-text {
  font-size: 14px;
  color: #047857;
  line-height: 1.5;
}

/* 阅读小贴士 */
.tip-section {
  background: #EFF6FF;
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 16px;
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.tip-icon {
  font-size: 16px;
}

.tip-title {
  font-size: 13px;
  font-weight: 600;
  color: #1E40AF;
}

.tip-content {
  font-size: 13px;
  color: #3B82F6;
  line-height: 1.5;
}

/* 操作按钮 */
.action-section {
  display: flex;
  gap: 12px;
}

.action-btn {
  height: 44px;
  font-weight: 600;
  border-radius: 12px;
}

.complete-btn {
  flex: 2;
  background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  border: none;
}

.complete-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #10B981 100%);
}

.refresh-btn {
  flex: 1;
  border: 1px dashed #E2E8F0;
}

.refresh-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

/* 奖励弹窗 */
.reward-modal {
  text-align: center;
  padding: 20px;
}

.reward-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.reward-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.reward-items {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 20px;
}

.reward-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reward-emoji {
  font-size: 24px;
}

.reward-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--primary);
}

/* 字符弹窗 */
.char-modal {
  text-align: center;
  padding: 20px;
}

.char-display {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
}

.char-pinyin {
  font-size: 18px;
  color: #B45309;
  margin-top: 8px;
}
</style>