<template>
  <div class="task-card" :class="{ 'daily-practice': isDailyPractice, completed: status === 'done' }" @click="handleClick">
    <div class="task-header">
      <span class="task-icon">{{ icon }}</span>
      <span class="task-title">{{ title }}</span>
      <span class="task-status" :class="statusClass">{{ statusText }}</span>
    </div>
    <div v-if="showContent" class="task-content">
      <slot></slot>
    </div>
    <div v-if="showActions && status !== 'done'" class="task-actions" @click.stop>
      <button class="btn btn-secondary" @click="$emit('secondary')">{{ secondaryText }}</button>
      <button class="btn btn-primary" @click="$emit('primary')">{{ primaryText }}</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  icon: string
  title: string
  status: 'pending' | 'done'
  isDailyPractice?: boolean
  showContent?: boolean
  showActions?: boolean
  secondaryText?: string
  primaryText?: string
}>()

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'secondary'): void
  (e: 'primary'): void
}>()

const statusClass = computed(() => {
  return props.status === 'done' ? 'status-done' : 'status-pending'
})

const statusText = computed(() => {
  return props.status === 'done' ? '✓ 已完成' : '○ 待完成'
})

const handleClick = () => {
  emit('click')
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.task-card {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --accent: #F97316;
  --bg-light: #F8FAFC;
  --bg-card: #FFFFFF;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --radius-sm: 12px;
  --radius-md: 16px;

  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.task-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  border-color: rgba(20, 184, 166, 0.2);
}

.task-card.daily-practice {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.06) 0%, rgba(45, 212, 191, 0.06) 100%);
  border-left: 4px solid var(--primary);
}

.task-card.completed {
  opacity: 0.75;
}

.task-card.completed:hover {
  opacity: 1;
}

.task-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.task-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(45, 212, 191, 0.1) 100%);
  border-radius: var(--radius-sm);
}

.task-title {
  font-weight: 600;
  font-size: 15px;
  flex: 1;
  color: var(--text-primary);
}

.task-status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s;
}

.status-done {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(52, 211, 153, 0.15) 100%);
  color: #059669;
}

.status-pending {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.12) 0%, rgba(251, 146, 60, 0.12) 100%);
  color: #EA580C;
}

.task-content {
  background: transparent;
  padding: 12px 0;
  margin-top: 12px;
  font-size: 14px;
  line-height: 1.6;
  border-top: 1px dashed rgba(0, 0, 0, 0.06);
}

.task-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(20, 184, 166, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(20, 184, 166, 0.4);
}

.btn-primary:active {
  transform: translateY(0);
}

.btn-secondary {
  background: var(--bg-light);
  color: var(--text-secondary);
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.btn-secondary:hover {
  background: rgba(20, 184, 166, 0.08);
  color: var(--primary-dark);
  border-color: var(--primary-light);
}

.btn-secondary:active {
  transform: scale(0.98);
}
</style>