<template>
  <n-modal v-model:show="showModal" preset="card" style="width: 90%; max-width: 380px;" :title="modalTitle">
    <div class="upload-content">
      <!-- 拍照区域 -->
      <div class="camera-preview" :class="{ 'has-image': previewImage }">
        <template v-if="!previewImage">
          <div class="camera-placeholder">
            <div class="camera-icon">📸</div>
            <div class="camera-text">点击下方按钮调用相机</div>
          </div>
        </template>
        <template v-else>
          <img :src="previewImage" alt="预览图片" class="preview-image" />
        </template>
      </div>

      <!-- 拍照/选图按钮 -->
      <div v-if="!previewImage" class="action-buttons">
        <n-button type="primary" style="flex: 1;" @click="takePhoto">
          📷 拍照
        </n-button>
        <n-button style="flex: 1;" @click="chooseFromAlbum">
          🖼️ 相册选择
        </n-button>
      </div>

      <!-- AI 识别结果预览 -->
      <div v-if="showAiResult" class="ai-result">
        <div class="ai-result-header">
          <span>🤖</span>
          <span class="ai-result-title">AI 识别结果</span>
        </div>
        <div class="ai-result-content">
          <div class="result-item">
            <span class="result-label">📚 类型：</span>
            <span class="result-value">{{ aiResult.type }}</span>
          </div>
          <div class="result-item">
            <span class="result-label">📖 科目：</span>
            <span class="result-value">{{ aiResult.subject }}</span>
          </div>
          <div class="result-item">
            <span class="result-label">📝 内容：</span>
            <div class="result-content-text">{{ aiResult.content }}</div>
          </div>
          <div v-if="aiResult.knowledgePoint" class="result-item">
            <span class="result-label">🎯 知识点：</span>
            <span class="result-value">{{ aiResult.knowledgePoint }}</span>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div v-if="previewImage" class="action-buttons">
        <n-button v-if="!showAiResult" style="flex: 1;" @click="resetPhoto">
          🔄 重选
        </n-button>
        <n-button v-if="!showAiResult" type="primary" style="flex: 1;" @click="analyzeImage" :loading="analyzing">
          🤖 AI 识别
        </n-button>
        <n-button v-if="showAiResult" style="flex: 1;" @click="resetPhoto">
          🔄 重拍
        </n-button>
        <n-button v-if="showAiResult" type="success" style="flex: 1;" @click="confirmUpload">
          ✓ 确认入库
        </n-button>
      </div>
    </div>

    <!-- 隐藏的文件输入 -->
    <input
      ref="cameraInput"
      type="file"
      accept="image/*"
      capture="environment"
      style="display: none;"
      @change="handleFileSelect"
    />
    <input
      ref="albumInput"
      type="file"
      accept="image/*"
      style="display: none;"
      @change="handleFileSelect"
    />
  </n-modal>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { NModal, NButton, useMessage } from 'naive-ui'

const props = defineProps<{
  show: boolean
  type: 'wrong' | 'material' | 'book'
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'confirm', data: any): void
}>()

const message = useMessage()

const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const modalTitle = computed(() => {
  const titles = {
    wrong: '📷 错题录入',
    material: '📄 资料录入',
    book: '📚 图书录入'
  }
  return titles[props.type]
})

const cameraInput = ref<HTMLInputElement | null>(null)
const albumInput = ref<HTMLInputElement | null>(null)
const previewImage = ref<string | null>(null)
const showAiResult = ref(false)
const analyzing = ref(false)

const aiResult = ref({
  type: '',
  subject: '',
  content: '',
  knowledgePoint: ''
})

// 模拟不同类型的 AI 识别结果
const mockResults = {
  wrong: {
    type: '错题',
    subject: '数学',
    content: '小明有 5 盒铅笔，每盒 12 支，一共有多少支铅笔？\n\n你的答案：5 + 12 = 17（支）❌\n正确答案：5 × 12 = 60（支）✅',
    knowledgePoint: '两位数乘法'
  },
  material: {
    type: '学习资料',
    subject: '语文',
    content: '《静夜思》\n李白\n\n床前明月光，疑是地上霜。\n举头望明月，低头思故乡。\n\n【注释】\n1. 疑：好像\n2. 举头：抬头',
    knowledgePoint: '古诗鉴赏'
  },
  book: {
    type: '图书',
    subject: '文学',
    content: '《小王子》\n作者：[法] 圣埃克苏佩里\n字数：约 4.5 万字\n\n内容简介：小王子从自己的星球出发，游历各个星球，最后来到地球的故事。',
    knowledgePoint: '儿童文学'
  }
}

watch(showModal, (newVal) => {
  if (!newVal) {
    resetState()
  }
})

const resetState = () => {
  previewImage.value = null
  showAiResult.value = false
  analyzing.value = false
  aiResult.value = { type: '', subject: '', content: '', knowledgePoint: '' }
}

const takePhoto = () => {
  cameraInput.value?.click()
}

const chooseFromAlbum = () => {
  albumInput.value?.click()
}

const handleFileSelect = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      previewImage.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
  }
  // 重置 input 以便可以重复选择同一文件
  input.value = ''
}

const resetPhoto = () => {
  previewImage.value = null
  showAiResult.value = false
  aiResult.value = { type: '', subject: '', content: '', knowledgePoint: '' }
}

const analyzeImage = async () => {
  analyzing.value = true

  // 模拟 AI 识别延迟
  await new Promise(resolve => setTimeout(resolve, 1500))

  // 使用模拟结果
  aiResult.value = { ...mockResults[props.type] }
  showAiResult.value = true
  analyzing.value = false

  message.success('AI 识别完成！')
}

const confirmUpload = () => {
  emit('confirm', {
    type: props.type,
    image: previewImage.value,
    aiResult: { ...aiResult.value }
  })

  message.success('已成功入库！')
  showModal.value = false
}
</script>

<style scoped>
.upload-content {
  padding: 0;
}

.camera-preview {
  background: #2c3e50;
  border-radius: 10px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
  position: relative;
  overflow: hidden;
}

.camera-preview.has-image {
  background: transparent;
  height: auto;
  min-height: 200px;
}

.camera-placeholder {
  text-align: center;
  color: white;
}

.camera-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.camera-text {
  font-size: 14px;
  opacity: 0.8;
}

.preview-image {
  width: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.ai-result {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 15px;
}

.ai-result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.ai-result-title {
  font-weight: bold;
  color: #667eea;
}

.ai-result-content {
  font-size: 13px;
  line-height: 1.8;
}

.result-item {
  margin-bottom: 8px;
}

.result-item:last-child {
  margin-bottom: 0;
}

.result-label {
  color: #666;
  font-weight: 500;
}

.result-value {
  color: #333;
}

.result-content-text {
  background: white;
  padding: 10px;
  border-radius: 8px;
  margin-top: 4px;
  white-space: pre-wrap;
  color: #333;
  font-size: 13px;
  line-height: 1.6;
}
</style>