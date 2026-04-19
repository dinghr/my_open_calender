<template>
  <div class="poetry-card">
    <!-- 标题区域 -->
    <div class="poetry-header">
      <div class="poetry-title">{{ poetry.title }}</div>
      <div class="poetry-title-pinyin" v-if="poetry.title_pinyin">{{ poetry.title_pinyin }}</div>
      <div class="poetry-author" v-if="poetry.author">
        <span class="dynasty" v-if="poetry.dynasty">{{ poetry.dynasty }}·</span>{{ poetry.author }}
      </div>
    </div>

    <!-- 田字格诗句区域 -->
    <div class="poetry-content">
      <div v-for="(line, lineIndex) in poetry.lines" :key="lineIndex" class="poetry-line-wrapper">
        <!-- 拼音线 -->
        <div class="pinyin-line">
          <div
            v-for="(char, charIndex) in line.chars"
            :key="charIndex"
            class="pinyin-cell"
            :class="{ 'punctuation': isPunctuation(char.char) }"
          >
            <span class="pinyin-text">{{ char.pinyin }}</span>
          </div>
        </div>
        <!-- 田字格 -->
        <div class="tianzige-line">
          <div
            v-for="(char, charIndex) in line.chars"
            :key="charIndex"
            class="tianzige-cell"
            :class="{ 'punctuation': isPunctuation(char.char) }"
          >
            <div class="tianzige-inner">
              <div class="tianzige-midline-h"></div>
              <div class="tianzige-midline-v"></div>
              <div class="tianzige-diagonal-1"></div>
              <div class="tianzige-diagonal-2"></div>
            </div>
            <span class="char-text">{{ char.char }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 译文区域 -->
    <div class="poetry-translation" v-if="poetry.translation">
      <div class="translation-label">📖 译文</div>
      <div class="translation-text">{{ poetry.translation }}</div>
    </div>

    <!-- 学习状态与操作 -->
    <div class="poetry-actions" v-if="showActions">
      <div class="mastery-status" v-if="memory">
        <span class="status-icon">{{ masteryIcon }}</span>
        <span class="status-text">{{ memory.mastery_text }}</span>
        <span class="review-count" v-if="memory.review_count > 0">复习 {{ memory.review_count }} 次</span>
      </div>

      <div class="action-buttons">
        <n-button
          :type="memory?.mastery_level === 'mastered' ? 'success' : 'default'"
          :ghost="memory?.mastery_level !== 'mastered'"
          size="large"
          @click="submitMastery('mastered')"
          :loading="loading === 'mastered'"
        >
          ✅ 会背了
        </n-button>
        <n-button
          :type="memory?.mastery_level === 'familiar' ? 'warning' : 'default'"
          :ghost="memory?.mastery_level !== 'familiar'"
          size="large"
          @click="submitMastery('familiar')"
          :loading="loading === 'familiar'"
        >
          😊 熟悉
        </n-button>
        <n-button
          :type="memory?.mastery_level === 'unfamiliar' ? 'error' : 'default'"
          :ghost="memory?.mastery_level !== 'unfamiliar'"
          size="large"
          @click="submitMastery('unfamiliar')"
          :loading="loading === 'unfamiliar'"
        >
          🤔 不太熟
        </n-button>
      </div>

      <!-- 下次复习提醒 -->
      <div class="review-reminder" v-if="memory?.next_review_at">
        <span class="reminder-icon">📅</span>
        <span class="reminder-text">{{ formatReviewDate(memory.next_review_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { NButton, useMessage } from 'naive-ui'
import { poetryApi } from '../api'

interface PoetryChar {
  char: string
  pinyin: string
}

interface PoetryLine {
  text: string
  pinyin: string
  chars: PoetryChar[]
}

interface Poetry {
  id: string
  title: string
  title_pinyin?: string
  author?: string
  dynasty?: string
  lines: PoetryLine[]
  translation?: string
  annotation?: Record<string, any>
  grade?: number
  semester?: string
  category?: string
  textbook?: string
}

interface Memory {
  id: string
  poetry_id: string
  poetry_title: string
  mastery_level: string
  mastery_text: string
  status: string
  review_count: number
  next_review_at?: string
  first_learned_at?: string
  last_reviewed_at?: string
}

const props = defineProps<{
  poetry: Poetry
  studentId?: string
  showActions?: boolean
}>()

const emit = defineEmits<{
  (e: 'mastery-change', data: { poetry_id: string; mastery_level: string }): void
}>()

const message = useMessage()
const loading = ref<string | null>(null)
const memory = ref<Memory | null>(null)

const masteryIcon = computed(() => {
  const icons: Record<string, string> = {
    new: '🌟',
    unfamiliar: '🤔',
    familiar: '😊',
    mastered: '✅'
  }
  return icons[memory.value?.mastery_level || 'new'] || '🌟'
})

// 判断是否为标点符号
const isPunctuation = (char: string): boolean => {
  return /[，。！？、；：""''（）《》]/.test(char)
}

// 格式化复习日期
const formatReviewDate = (dateStr: string): string => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffDays = Math.ceil((date.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))

  if (diffDays <= 0) return '今天需要复习'
  if (diffDays === 1) return '明天复习'
  if (diffDays <= 7) return `${diffDays}天后复习`
  return `${date.getMonth() + 1}月${date.getDate()}日复习`
}

// 提交掌握程度
const submitMastery = async (level: 'mastered' | 'familiar' | 'unfamiliar') => {
  if (!props.studentId) {
    message.warning('请先登录')
    return
  }

  loading.value = level
  try {
    const res = await poetryApi.submitMemory({
      student_id: props.studentId,
      poetry_id: props.poetry.id,
      mastery_level: level
    })

    if (res.data) {
      message.success(res.data.message || '状态已更新')

      // 更新本地状态
      const masteryTexts: Record<string, string> = {
        new: '新学',
        unfamiliar: '不太熟',
        familiar: '熟悉',
        mastered: '会背了'
      }

      memory.value = {
        ...memory.value,
        id: memory.value?.id || '',
        poetry_id: props.poetry.id,
        poetry_title: props.poetry.title,
        mastery_level: level,
        mastery_text: masteryTexts[level] || '新学',
        status: level === 'mastered' ? 'mastered' : level === 'familiar' ? 'reviewed' : 'learning',
        review_count: (memory.value?.review_count || 0) + 1,
        next_review_at: res.data.next_review_at
      }

      emit('mastery-change', { poetry_id: props.poetry.id, mastery_level: level })
    }
  } catch (e) {
    message.error('提交失败')
  } finally {
    loading.value = null
  }
}

onMounted(() => {
  // 不再预加载学习状态
})
</script>

<style scoped>
.poetry-card {
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(251, 191, 36, 0.15);
}

/* 标题区域 */
.poetry-header {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px dashed rgba(251, 191, 36, 0.3);
}

.poetry-title {
  font-size: 28px;
  font-weight: 700;
  color: #92400E;
  margin-bottom: 4px;
  letter-spacing: 4px;
}

.poetry-title-pinyin {
  font-size: 14px;
  color: #B45309;
  font-family: 'Times New Roman', serif;
  letter-spacing: 2px;
  margin-bottom: 4px;
}

.poetry-author {
  font-size: 14px;
  color: #D97706;
}

.dynasty {
  color: #B45309;
}

/* 田字格诗句区域 */
.poetry-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.poetry-line-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 拼音线 */
.pinyin-line {
  display: flex;
  justify-content: center;
  margin-bottom: 4px;
}

.pinyin-cell {
  width: 40px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pinyin-cell.punctuation {
  width: 24px;
}

.pinyin-text {
  font-size: 12px;
  color: #B45309;
  font-family: 'Times New Roman', serif;
}

/* 田字格 */
.tianzige-line {
  display: flex;
  justify-content: center;
}

.tianzige-cell {
  width: 40px;
  height: 40px;
  position: relative;
  background: #FFFDF7;
  border: 1px solid #F59E0B;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tianzige-cell.punctuation {
  width: 24px;
  background: transparent;
  border: none;
}

.tianzige-inner {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

/* 田字格中线 */
.tianzige-midline-h {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(245, 158, 11, 0.3);
}

.tianzige-midline-v {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
  background: rgba(245, 158, 11, 0.3);
}

/* 田字格对角线 */
.tianzige-diagonal-1 {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: none;
}

.tianzige-diagonal-1::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 56.57px;
  height: 1px;
  background: rgba(245, 158, 11, 0.2);
  transform: rotate(45deg);
  transform-origin: 0 0;
}

.tianzige-diagonal-2::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 56.57px;
  height: 1px;
  background: rgba(245, 158, 11, 0.2);
  transform: rotate(-45deg);
  transform-origin: 0 0;
}

.char-text {
  font-size: 24px;
  font-weight: 600;
  color: #78350F;
  position: relative;
  z-index: 1;
}

.tianzige-cell.punctuation .char-text {
  font-size: 18px;
  color: #B45309;
}

/* 译文区域 */
.poetry-translation {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 20px;
  border-left: 4px solid #F59E0B;
}

.translation-label {
  font-size: 13px;
  font-weight: 600;
  color: #B45309;
  margin-bottom: 8px;
}

.translation-text {
  font-size: 14px;
  color: #78350F;
  line-height: 1.8;
}

/* 学习状态与操作 */
.poetry-actions {
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
  padding: 16px;
}

.mastery-status {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  justify-content: center;
}

.status-icon {
  font-size: 20px;
}

.status-text {
  font-size: 14px;
  font-weight: 600;
  color: #78350F;
}

.review-count {
  font-size: 12px;
  color: #B45309;
  margin-left: 8px;
}

.action-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons .n-button {
  min-width: 100px;
}

/* 复习提醒 */
.review-reminder {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed rgba(180, 83, 9, 0.2);
}

.reminder-icon {
  font-size: 16px;
}

.reminder-text {
  font-size: 13px;
  color: #B45309;
}

/* 响应式调整 */
@media (max-width: 400px) {
  .tianzige-cell {
    width: 32px;
    height: 32px;
  }

  .tianzige-cell.punctuation {
    width: 20px;
  }

  .pinyin-cell {
    width: 32px;
  }

  .pinyin-cell.punctuation {
    width: 20px;
  }

  .char-text {
    font-size: 20px;
  }

  .pinyin-text {
    font-size: 10px;
  }
}
</style>