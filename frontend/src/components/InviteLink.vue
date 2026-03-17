<template>
  <n-card title="🔗 邀请家人绑定" class="invite-card">
    <p class="description">生成邀请二维码或链接，分享给家人即可快速绑定小朋友账号</p>

    <n-space>
      <n-button type="primary" @click="showModal = true">
        生成邀请链接
      </n-button>
    </n-space>

    <!-- 邀请链接列表 -->
    <n-card title="📋 邀请记录" size="small" style="margin-top: 16px;" v-if="inviteLinks.length > 0">
      <n-list bordered>
        <n-list-item v-for="link in inviteLinks" :key="link.id">
          <n-space justify="space-between" align="center" style="width: 100%;">
            <div>
              <n-text strong>{{ link.code }}</n-text>
              <br />
              <n-text depth="3" style="font-size: 12px;">
                创建于 {{ formatDate(link.created_at) }}
              </n-text>
            </div>
            <n-tag :type="getStatusType(link.status)">
              {{ getStatusText(link.status) }}
            </n-tag>
          </n-space>
        </n-list-item>
      </n-list>
    </n-card>

    <!-- 生成弹窗 -->
    <n-modal v-model:show="showModal" preset="card" title="生成邀请链接" style="width: 400px;">
      <n-form ref="formRef" :model="formData" label-placement="left" label-width="80">
        <n-form-item label="有效期">
          <n-radio-group v-model:value="formData.expire_type">
            <n-radio-button value="7days">7天</n-radio-button>
            <n-radio-button value="30days">30天</n-radio-button>
            <n-radio-button value="forever">永久</n-radio-button>
          </n-radio-group>
        </n-form-item>

        <n-form-item label="使用次数">
          <n-radio-group v-model:value="formData.usage_type">
            <n-radio-button value="once">仅1次</n-radio-button>
            <n-radio-button value="multiple">多次使用</n-radio-button>
          </n-radio-group>
        </n-form-item>
      </n-form>

      <template #footer>
        <n-space justify="end">
          <n-button @click="showModal = false">取消</n-button>
          <n-button type="primary" :loading="isCreating" @click="handleCreate">
            生成
          </n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 结果弹窗 -->
    <n-modal v-model:show="showResult" preset="card" title="邀请链接已生成" style="width: 400px;">
      <div style="text-align: center;">
        <!-- 二维码占位 -->
        <div class="qrcode-placeholder">
          <n-icon size="64" color="#667eea">
            <svg viewBox="0 0 24 24">
              <path fill="currentColor" d="M3,3H10V10H3V3M13,3H21V10H13V3M3,13H10V21H3V13M13,13H16V16H13V13M19,13H21V16H19V13M13,19H16V21H13V19M19,19H21V21H19V19M16,16H19V19H16V16Z" />
            </svg>
          </n-icon>
          <p style="margin-top: 8px; font-size: 12px; color: #666;">扫码即可绑定小朋友账号</p>
        </div>

        <!-- 链接 -->
        <n-input-group style="margin-top: 16px;">
          <n-input :value="generatedLink" readonly />
          <n-button type="primary" @click="copyLink">复制</n-button>
        </n-input-group>

        <!-- 信息 -->
        <n-descriptions :column="2" style="margin-top: 16px;">
          <n-descriptions-item label="有效期">{{ getExpireText(formData.expire_type) }}</n-descriptions-item>
          <n-descriptions-item label="使用次数">{{ formData.usage_type === 'once' ? '仅1次' : '多次' }}</n-descriptions-item>
        </n-descriptions>
      </div>

      <template #footer>
        <n-button block @click="showResult = false">关闭</n-button>
      </template>
    </n-modal>
  </n-card>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  NCard, NButton, NSpace, NList, NListItem, NTag, NText, NModal,
  NForm, NFormItem, NRadioGroup, NRadioButton, NInput, NInputGroup,
  NDescriptions, NDescriptionsItem, NIcon, useMessage
} from 'naive-ui'
import { inviteApi } from '../api'

const props = defineProps<{
  studentId: string
}>()

const message = useMessage()
const showModal = ref(false)
const showResult = ref(false)
const isCreating = ref(false)
const inviteLinks = ref<any[]>([])
const generatedLink = ref('')

const formData = ref({
  expire_type: '7days' as '7days' | '30days' | 'forever',
  usage_type: 'once' as 'once' | 'multiple'
})

const loadInviteLinks = async () => {
  const res = await inviteApi.list(props.studentId)
  if (res.data) {
    inviteLinks.value = res.data
  }
}

const handleCreate = async () => {
  isCreating.value = true

  const res = await inviteApi.create({
    student_id: props.studentId,
    ...formData.value
  })

  isCreating.value = false

  if (res.data) {
    generatedLink.value = res.data.link_url
    showModal.value = false
    showResult.value = true
    loadInviteLinks()
  }
}

const copyLink = () => {
  navigator.clipboard.writeText(generatedLink.value)
  message.success('链接已复制到剪贴板')
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const getStatusType = (status: string) => {
  switch (status) {
    case 'active': return 'success'
    case 'used': return 'info'
    case 'expired': return 'warning'
    case 'disabled': return 'error'
    default: return 'default'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'active': return '待使用'
    case 'used': return '已使用'
    case 'expired': return '已过期'
    case 'disabled': return '已关闭'
    default: return status
  }
}

const getExpireText = (type: string) => {
  switch (type) {
    case '7days': return '7天'
    case '30days': return '30天'
    case 'forever': return '永久'
    default: return type
  }
}

onMounted(() => {
  loadInviteLinks()
})
</script>

<style scoped>
.invite-card {
  margin-bottom: 16px;
}

.description {
  font-size: 12px;
  color: #666;
  margin-bottom: 12px;
}

.qrcode-placeholder {
  width: 160px;
  height: 160px;
  background: #f3f4f6;
  border-radius: 12px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>