<template>
  <n-modal v-model:show="showModal" preset="card" style="width: 90%; max-width: 400px;" class="discuss-modal">
    <template #header>
      <div class="modal-header">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        </div>
        <span class="header-title">和爸爸妈妈商量奖励</span>
      </div>
    </template>

    <div class="discuss-content">
      <!-- 提示 -->
      <div class="discuss-tip">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 16v-4M12 8h.01" />
        </svg>
        小朋友可以在这里写下想要的奖励，爸爸妈妈会和你一起商量哦！
      </div>

      <!-- 输入愿望 -->
      <div class="discuss-input-area">
        <div class="discuss-title">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
          </svg>
          我的愿望清单
        </div>
        <n-input
          v-model:value="newWish"
          placeholder="写下你想要的奖励..."
          class="wish-input"
          @keyup.enter="addWish"
        />
        <n-button type="primary" block class="send-btn" @click="addWish" :disabled="!newWish.trim()">
          <template #icon>
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </template>
          发送给爸爸妈妈
        </n-button>
      </div>

      <!-- 愿望列表 -->
      <div class="wish-section">
        <div class="section-title">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
          </svg>
          愿望讨论记录
        </div>

        <div class="wish-list">
          <div v-for="wish in wishes" :key="wish.id" class="wish-item">
            <span class="wish-icon">{{ wish.icon }}</span>
            <span class="wish-text">{{ wish.content }}</span>
            <n-tag :type="getStatusType(wish.status)" size="small" round>
              {{ getStatusText(wish.status) }}
            </n-tag>
          </div>
        </div>
      </div>

      <!-- 家长回复区 -->
      <div class="parent-reply">
        <div class="reply-title">
          <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          爸爸妈妈的回复
        </div>
        <div class="reply-content">
          {{ parentReply || '暂无回复，爸爸妈妈看到后会回复你的～' }}
        </div>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { NModal, NInput, NButton, NTag, useMessage } from 'naive-ui'

const props = defineProps<{
  show: boolean
  wishes: any[]
  parentReply?: string
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'addWish', content: string): void
}>()

const message = useMessage()

const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const newWish = ref('')

const addWish = () => {
  if (newWish.value.trim()) {
    emit('addWish', newWish.value.trim())
    message.success('愿望已发送给爸爸妈妈！')
    newWish.value = ''
  }
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'approved': return 'success'
    case 'rejected': return 'error'
    default: return 'warning'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'approved': return '爸爸同意了'
    case 'rejected': return '暂时不行'
    default: return '讨论中'
  }
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.discuss-modal {
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

.discuss-content {
  padding: 0;
}

.discuss-tip {
  background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  margin-bottom: 16px;
  font-size: 13px;
  color: #0369A1;
  line-height: 1.6;
  display: flex;
  align-items: flex-start;
}

.discuss-input-area {
  background: var(--bg-light);
  border-radius: var(--radius-md);
  padding: 14px;
  margin-bottom: 16px;
}

.discuss-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.wish-input {
  margin-bottom: 10px;
}

.send-btn {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border: none;
  font-weight: 500;
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
}

.wish-section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.wish-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.wish-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: var(--bg-light);
  border-radius: var(--radius-sm);
  transition: all 0.3s;
}

.wish-item:hover {
  background: rgba(20, 184, 166, 0.06);
}

.wish-icon {
  font-size: 20px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 8px;
}

.wish-text {
  flex: 1;
  font-size: 13px;
  color: var(--text-primary);
}

.parent-reply {
  background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
  padding: 14px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.reply-title {
  font-size: 12px;
  font-weight: 600;
  color: #166534;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.reply-content {
  background: white;
  padding: 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  color: var(--text-primary);
  line-height: 1.7;
}
</style>