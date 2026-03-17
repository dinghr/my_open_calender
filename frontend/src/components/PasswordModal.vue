<template>
  <n-modal v-model:show="showModal" preset="card" style="width: 90%; max-width: 320px;" class="password-modal">
    <div class="password-content">
      <div class="password-icon">
        <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
          <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </svg>
      </div>
      <h3 class="password-title">家长验证</h3>
      <p class="password-desc">请输入家长密码</p>
      <n-input
        v-model:value="password"
        type="password"
        maxlength="6"
        placeholder="请输入密码"
        size="large"
        class="password-input"
        @keyup.enter="verifyPassword"
      />
      <div class="password-actions">
        <n-button class="action-btn cancel-btn" @click="handleCancel">
          取消
        </n-button>
        <n-button type="primary" class="action-btn confirm-btn" @click="verifyPassword">
          <template #icon>
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </template>
          确认
        </n-button>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { NModal, NInput, NButton, useMessage } from 'naive-ui'

const props = defineProps<{
  show: boolean
  correctPassword?: string
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'success'): void
  (e: 'cancel'): void
}>()

const message = useMessage()

const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const password = ref('')

const verifyPassword = () => {
  const correct = props.correctPassword || '0000'
  if (password.value === correct) {
    emit('success')
    showModal.value = false
    password.value = ''
  } else {
    message.error('密码错误，请重试')
    password.value = ''
  }
}

const handleCancel = () => {
  emit('cancel')
  showModal.value = false
  password.value = ''
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.password-modal {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --radius-sm: 12px;
  --radius-md: 16px;
}

.password-content {
  text-align: center;
  padding: 16px 0;
}

.password-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: white;
  box-shadow: 0 4px 16px rgba(20, 184, 166, 0.3);
}

.password-title {
  margin: 0 0 8px 0;
  font-size: 20px;
  font-weight: 600;
  color: var(--text-primary);
}

.password-desc {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}

.password-input {
  margin-bottom: 20px;
}

.password-input :deep(.n-input__input-el) {
  text-align: center;
  font-size: 20px;
  letter-spacing: 8px;
}

.password-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  height: 44px;
  font-weight: 500;
  border-radius: var(--radius-sm);
}

.cancel-btn {
  border: 1px solid #E2E8F0;
}

.cancel-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.confirm-btn {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border: none;
}

.confirm-btn:hover {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
}
</style>