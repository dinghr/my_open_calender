<template>
  <n-card class="teacher-advice-card">
    <template #header>
      <div class="card-header">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
        </div>
        <span class="header-title">老师学习建议</span>
      </div>
    </template>

    <p class="description">
      <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
        <circle cx="12" cy="12" r="10" />
        <path d="M12 16v-4M12 8h.01" />
      </svg>
      粘贴老师发送的学习内容，AI 自动解析生成学习计划
    </p>

    <!-- 输入区域 -->
    <n-input
      v-model:value="rawContent"
      type="textarea"
      placeholder="在此粘贴老师发送的学习建议、作业要求、复习要点等内容..."
      :autosize="{ minRows: 4, maxRows: 8 }"
      :disabled="isParsing || isConfirmed"
      class="content-input"
    />

    <div class="action-row">
      <n-button
        type="primary"
        :disabled="!rawContent.trim() || isParsing || isConfirmed"
        :loading="isParsing"
        class="parse-btn"
        @click="handleParse"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2a10 10 0 1 0 10 10H12V2z" />
            <path d="M12 2a10 10 0 0 1 10 10" />
          </svg>
        </template>
        AI 解析
      </n-button>
    </div>

    <!-- 解析结果 -->
    <n-collapse-transition :show="showResult">
      <div class="parse-result">
        <n-alert type="success" class="success-alert">
          <template #icon>
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
              <polyline points="22 4 12 14.01 9 11.01" />
            </svg>
          </template>
          解析完成
        </n-alert>

        <div class="result-section">
          <div class="result-item">
            <span class="result-label">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              </svg>
              学科
            </span>
            <n-tag type="info" size="small">{{ parseResult.subject || '-' }}</n-tag>
          </div>
          <div class="result-item">
            <span class="result-label">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
              </svg>
              课题
            </span>
            <span class="result-value">{{ parseResult.topic || '-' }}</span>
          </div>
          <div class="result-item">
            <span class="result-label">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
                <circle cx="12" cy="12" r="10" />
                <circle cx="12" cy="12" r="6" />
                <circle cx="12" cy="12" r="2" />
              </svg>
              知识点
            </span>
            <div class="tag-list">
              <n-tag v-for="point in parseResult.knowledge_points" :key="point" type="warning" size="small">
                {{ point }}
              </n-tag>
            </div>
          </div>
        </div>

        <div class="task-section">
          <div class="section-title">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
              <path d="M9 11l3 3L22 4" />
              <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
            </svg>
            任务清单
          </div>
          <div class="task-list">
            <div v-for="(task, index) in parseResult.tasks" :key="index" class="task-item">
              <n-checkbox :checked="false">{{ task.content }}</n-checkbox>
            </div>
          </div>
        </div>

        <div class="reminder-section" v-if="parseResult.reminders.length > 0">
          <div class="section-title">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            提醒事项
          </div>
          <div class="reminder-list">
            <div v-for="(reminder, index) in parseResult.reminders" :key="index" class="reminder-item">
              {{ reminder }}
            </div>
          </div>
        </div>

        <div class="confirm-row">
          <n-button type="success" :loading="isConfirming" class="confirm-btn" @click="handleConfirm">
            <template #icon>
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </template>
            确认并添加到计划
          </n-button>
        </div>
      </div>
    </n-collapse-transition>
  </n-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  NCard, NInput, NButton, NTag, NCheckbox, NCollapseTransition
} from 'naive-ui'
import { teacherAdviceApi } from '../api'

const props = defineProps<{
  studentId: string
}>()

const emit = defineEmits<{
  (e: 'confirmed'): void
}>()

const rawContent = ref('')
const isParsing = ref(false)
const isConfirming = ref(false)
const isConfirmed = ref(false)
const showResult = ref(false)
const adviceId = ref('')

const parseResult = ref<{
  subject: string
  topic: string
  knowledge_points: string[]
  tasks: { content: string }[]
  reminders: string[]
}>({
  subject: '',
  topic: '',
  knowledge_points: [],
  tasks: [],
  reminders: []
})

const handleParse = async () => {
  isParsing.value = true

  const createRes = await teacherAdviceApi.create({
    student_id: props.studentId,
    raw_content: rawContent.value
  })

  if (createRes.error || !createRes.data?.id) {
    isParsing.value = false
    return
  }

  adviceId.value = createRes.data.id

  const parseRes = await teacherAdviceApi.parse(adviceId.value)

  isParsing.value = false

  if (parseRes.data) {
    parseResult.value = {
      subject: parseRes.data.subject || '',
      topic: parseRes.data.topic || '',
      knowledge_points: parseRes.data.knowledge_points || [],
      tasks: parseRes.data.tasks || [],
      reminders: parseRes.data.reminders || []
    }
    showResult.value = true
  }
}

const handleConfirm = async () => {
  isConfirming.value = true

  const res = await teacherAdviceApi.confirm(adviceId.value)

  isConfirming.value = false

  if (res.data) {
    isConfirmed.value = true
    emit('confirmed')
  }
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.teacher-advice-card {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --bg-light: #F8FAFC;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --radius-sm: 12px;
  --radius-md: 16px;

  margin-bottom: 16px;
  border-radius: var(--radius-md);
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
}

.description {
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
}

.content-input {
  border-radius: var(--radius-sm);
}

.action-row {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.parse-btn {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border: none;
  font-weight: 500;
}

.parse-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
}

.parse-result {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #E2E8F0;
}

.success-alert {
  margin-bottom: 16px;
  border-radius: var(--radius-sm);
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(52, 211, 153, 0.1) 100%);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.result-section {
  background: var(--bg-light);
  border-radius: var(--radius-sm);
  padding: 14px;
  margin-bottom: 16px;
}

.result-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px dashed #E2E8F0;
}

.result-item:last-child {
  border-bottom: none;
}

.result-label {
  font-size: 12px;
  color: var(--text-secondary);
  min-width: 80px;
  display: flex;
  align-items: center;
}

.result-value {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.task-section, .reminder-section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.task-list, .reminder-list {
  background: var(--bg-light);
  border-radius: var(--radius-sm);
  padding: 12px;
}

.task-item {
  padding: 6px 0;
}

.task-item:not(:last-child) {
  border-bottom: 1px solid #E2E8F0;
}

.reminder-item {
  font-size: 12px;
  color: var(--text-secondary);
  padding: 4px 0;
}

.reminder-item::before {
  content: '•';
  margin-right: 6px;
  color: var(--primary);
}

.confirm-row {
  display: flex;
  justify-content: center;
}

.confirm-btn {
  background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  border: none;
  font-weight: 500;
  padding: 0 32px;
}

.confirm-btn:hover {
  background: linear-gradient(135deg, #059669 0%, #10B981 100%);
}
</style>