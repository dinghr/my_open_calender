<template>
  <n-card class="daily-practice-card">
    <template #header>
      <div class="card-header">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
          </svg>
        </div>
        <span class="header-title">每日一练</span>
        <n-tag type="warning" size="small" class="header-tag">
          <template #icon>
            <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
          </template>
          请在放学前确认
        </n-tag>
      </div>
    </template>

    <!-- 确认状态提示 -->
    <n-alert
      v-if="!allVerified"
      type="warning"
      class="status-alert warning"
    >
      <template #icon>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
          <line x1="12" y1="9" x2="12" y2="13" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
      </template>
      待家长确认 - 请在 <strong>15:30 放学</strong>前完成内容确认
    </n-alert>

    <n-alert
      v-else
      type="success"
      class="status-alert success"
    >
      <template #icon>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
          <polyline points="22 4 12 14.01 9 11.01" />
        </svg>
      </template>
      已确认 - 可以打印
    </n-alert>

    <!-- 预览入口 -->
    <div class="preview-cards">
      <!-- 语文 -->
      <div class="preview-card chinese" @click="handlePreview('chinese')">
        <div class="preview-header">
          <div class="preview-icon chinese-icon">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              <path d="M8 7h8M8 11h6" />
            </svg>
          </div>
          <div class="preview-title">
            <span class="title-text">语文</span>
            <n-tag size="small" :type="chineseVerified ? 'success' : 'warning'" round>
              {{ chineseVerified ? '已确认' : '待确认' }}
            </n-tag>
          </div>
        </div>
        <div class="preview-content">
          《静夜思》背诵 + 生字练习
        </div>
      </div>

      <!-- 数学 -->
      <div class="preview-card math" @click="handlePreview('math')">
        <div class="preview-header">
          <div class="preview-icon math-icon">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23" />
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
          </div>
          <div class="preview-title">
            <span class="title-text">数学</span>
            <n-tag size="small" :type="mathVerified ? 'success' : 'warning'" round>
              {{ mathVerified ? '已确认' : '待确认' }}
            </n-tag>
          </div>
        </div>
        <div class="preview-content">
          口算练习 + 应用题
        </div>
      </div>
    </div>

    <!-- 确认按钮 -->
    <n-button
      type="success"
      block
      class="verify-btn"
      :disabled="allVerified"
      @click="handleVerifyAll"
    >
      <template #icon>
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12" />
        </svg>
      </template>
      确认今日每日一练内容
    </n-button>

    <!-- 打印按钮 -->
    <div class="print-section" :class="{ disabled: !allVerified }">
      <div class="print-buttons">
        <n-button type="primary" class="print-btn chinese-btn" @click="handlePrint('chinese')">
          <template #icon>
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
          </template>
          打印语文
        </n-button>
        <n-button class="print-btn math-btn" @click="handlePrint('math')">
          <template #icon>
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23" />
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
          </template>
          打印数学
        </n-button>
      </div>

      <n-button block class="print-all-btn" @click="handlePrint('all')">
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 6 2 18 2 18 9" />
            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2" />
            <rect x="6" y="14" width="12" height="8" />
          </svg>
        </template>
        打印全部（语文+数学）
      </n-button>
    </div>
  </n-card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  NCard, NTag, NAlert, NButton, useMessage
} from 'naive-ui'
import { dailyPracticeApi } from '../api'

const props = defineProps<{
  studentId: string
}>()

const message = useMessage()

const practiceData = ref<any[]>([])
const chineseVerified = ref(false)
const mathVerified = ref(false)

const allVerified = computed(() => chineseVerified.value && mathVerified.value)

const loadData = async () => {
  const res = await dailyPracticeApi.get(props.studentId)
  if (res.data) {
    practiceData.value = res.data
    res.data.forEach((item: any) => {
      if (item.subject === 'chinese') {
        chineseVerified.value = item.parent_verified
      } else if (item.subject === 'math') {
        mathVerified.value = item.parent_verified
      }
    })
  }
}

const handlePreview = (subject: string) => {
  message.info(`跳转到${subject === 'chinese' ? '语文' : '数学'}每日一练预览页`)
}

const handleVerifyAll = async () => {
  for (const item of practiceData.value) {
    if (!item.parent_verified) {
      await dailyPracticeApi.verify(item.id)
    }
  }
  chineseVerified.value = true
  mathVerified.value = true
  message.success('已确认')
}

const handlePrint = (type: 'chinese' | 'math' | 'all') => {
  if (!allVerified.value) {
    message.warning('请先确认内容后再打印')
    return
  }

  const typeText = type === 'chinese' ? '语文' : type === 'math' ? '数学' : '全部'
  message.info(`正在打印${typeText}每日一练...`)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* 薄荷绿主题变量 */
.daily-practice-card {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --accent: #F97316;
  --bg-light: #F8FAFC;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --radius-sm: 12px;
  --radius-md: 16px;

  margin-bottom: 16px;
  border-radius: var(--radius-md);
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
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  flex: 1;
}

.header-tag {
  font-size: 11px;
}

.status-alert {
  margin-bottom: 16px;
  border-radius: var(--radius-sm);
}

.status-alert.warning {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(245, 158, 11, 0.1) 100%);
  border: 1px solid rgba(251, 191, 36, 0.2);
}

.status-alert.success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

/* 预览卡片 */
.preview-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.preview-card {
  background: var(--bg-light);
  border-radius: var(--radius-md);
  padding: 14px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.preview-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.preview-card.chinese:hover {
  border-color: var(--primary);
}

.preview-card.math:hover {
  border-color: var(--accent);
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.preview-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.preview-icon.chinese-icon {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
}

.preview-icon.math-icon {
  background: linear-gradient(135deg, var(--accent) 0%, #FB923C 100%);
  color: white;
}

.preview-title {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-text {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.preview-content {
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.5;
}

/* 确认按钮 */
.verify-btn {
  height: 44px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  margin-bottom: 12px;
  background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  border: none;
}

.verify-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #059669 0%, #10B981 100%);
}

/* 打印区域 */
.print-section {
  transition: opacity 0.3s;
}

.print-section.disabled {
  opacity: 0.5;
  pointer-events: none;
}

.print-buttons {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

.print-btn {
  height: 40px;
  font-weight: 500;
  border-radius: var(--radius-sm);
}

.chinese-btn {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border: none;
}

.chinese-btn:hover {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
}

.math-btn {
  background: linear-gradient(135deg, var(--accent) 0%, #FB923C 100%);
  border: none;
  color: white;
}

.math-btn:hover {
  background: linear-gradient(135deg, #EA580C 0%, var(--accent) 100%);
}

.print-all-btn {
  height: 40px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  border: 1px dashed #E2E8F0;
}

.print-all-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}
</style>