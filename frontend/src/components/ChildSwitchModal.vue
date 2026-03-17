<template>
  <n-modal v-model:show="showModal" preset="card" style="width: 90%; max-width: 380px;" class="child-switch-modal">
    <template #header>
      <div class="modal-header">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
        </div>
        <span class="header-title">切换小朋友</span>
      </div>
    </template>

    <div class="switch-content">
      <p class="switch-desc">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 16v-4M12 8h.01" />
        </svg>
        选择要查看的小朋友
      </p>

      <div class="child-list">
        <div
          v-for="child in children"
          :key="child.id"
          class="child-item"
          :class="{ active: child.id === currentChildId }"
          @click="selectChild(child)"
        >
          <div class="child-avatar" :class="child.gender">
            {{ child.gender === 'girl' ? '👧' : '👦' }}
          </div>
          <div class="child-info">
            <div class="child-name">{{ child.nickname }}</div>
            <div class="child-meta">{{ child.grade }} · {{ child.gender === 'girl' ? '女孩' : '男孩' }} · {{ child.age }}岁</div>
            <div class="child-detail">{{ child.textbook }} · {{ child.hobbies }}</div>
          </div>
          <div class="child-status">
            <n-tag v-if="child.id === currentChildId" type="success" size="small" round>当前</n-tag>
            <div v-else class="status-dot"></div>
          </div>
        </div>
      </div>

      <n-button
        block
        dashed
        class="add-btn"
        :disabled="children.length >= 2"
        @click="handleAddChild"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
        </template>
        添加小朋友（已达上限 {{ children.length }}/2）
      </n-button>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NModal, NTag, NButton, useMessage } from 'naive-ui'

interface Child {
  id: string
  nickname: string
  gender: 'girl' | 'boy'
  grade: string
  age: number
  textbook: string
  hobbies: string
}

const props = defineProps<{
  show: boolean
  children: Child[]
  currentChildId: string
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'select', child: Child): void
  (e: 'add'): void
}>()

const message = useMessage()

const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const selectChild = (child: Child) => {
  if (child.id !== props.currentChildId) {
    emit('select', child)
    message.success(`已切换到 ${child.nickname}`)
  }
  showModal.value = false
}

const handleAddChild = () => {
  if (props.children.length >= 2) {
    message.warning('每个账号最多绑定2位小朋友')
    return
  }
  emit('add')
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.child-switch-modal {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --bg-light: #F8FAFC;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  --radius-sm: 12px;
  --radius-md: 16px;
}

.modal-header {
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
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.switch-content {
  padding: 0;
}

.switch-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  display: flex;
  align-items: center;
}

.child-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.child-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px;
  background: var(--bg-light);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 2px solid transparent;
}

.child-item:hover {
  background: rgba(20, 184, 166, 0.06);
  transform: translateX(4px);
}

.child-item.active {
  border-color: var(--primary);
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.08) 0%, rgba(45, 212, 191, 0.08) 100%);
}

.child-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.child-avatar.girl {
  background: linear-gradient(135deg, #FCE7F3 0%, #FBCFE8 100%);
}

.child-avatar.boy {
  background: linear-gradient(135deg, #DBEAFE 0%, #BFDBFE 100%);
}

.child-info {
  flex: 1;
  min-width: 0;
}

.child-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.child-meta {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 3px;
}

.child-detail {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.child-status {
  display: flex;
  align-items: center;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #E2E8F0;
}

.add-btn {
  margin-top: 16px;
  height: 48px;
  border-radius: var(--radius-md);
  border-color: #E2E8F0;
  color: var(--text-secondary);
  font-weight: 500;
}

.add-btn:hover:not(:disabled) {
  border-color: var(--primary);
  color: var(--primary);
}

.add-btn:disabled {
  opacity: 0.5;
}
</style>