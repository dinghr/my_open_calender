<template>
  <Transition name="modal">
    <div v-if="show" class="modal-overlay" @click.self="handleClose">
      <div class="modal-content photo-capture-modal">
        <!-- 顶部导航栏 -->
        <div class="modal-header">
          <div class="modal-title-wrapper">
            <span class="modal-icon">📸</span>
            <h3 class="modal-title">{{ subjectLabel }}错题拍照</h3>
          </div>
          <button class="modal-close" @click="handleClose">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- 相机取景预览区 -->
        <div class="camera-preview-container">
          <div class="camera-preview" :style="{ aspectRatio: '4/3' }">
            <!-- 隐藏的视频元素用于相机预览 -->
            <video
              ref="videoRef"
              class="camera-video"
              autoplay
              playsinline
              muted
            ></video>

            <!-- 拍摄的图片预览 -->
            <img
              v-if="capturedImage && !isCameraActive"
              :src="capturedImage"
              class="captured-image"
              alt="captured"
            />

            <!-- 辅助网格 -->
            <div v-if="showGrid && isCameraActive" class="grid-overlay">
              <div class="grid-line horizontal" style="top: 33.33%"></div>
              <div class="grid-line horizontal" style="top: 66.66%"></div>
              <div class="grid-line vertical" style="left: 33.33%"></div>
              <div class="grid-line vertical" style="left: 66.66%"></div>
            </div>

            <!-- 题目识别框 -->
            <div v-if="isCameraActive && aiDetect" class="detect-frame">
              <div class="detect-corner top-left"></div>
              <div class="detect-corner top-right"></div>
              <div class="detect-corner bottom-left"></div>
              <div class="detect-corner bottom-right"></div>
              <div class="detect-label">AI 识别题目</div>
            </div>

            <!-- 相机未启动时的提示 -->
            <div v-if="!isCameraActive && !capturedImage" class="camera-placeholder">
              <div class="placeholder-icon">📷</div>
              <div class="placeholder-text">点击下方按钮开启相机</div>
            </div>
          </div>
        </div>

        <!-- 辅助网格开关 -->
        <div class="grid-toggle" v-if="isCameraActive">
          <div class="toggle-label" @click="showGrid = !showGrid">
            <span class="toggle-icon">📐</span>
            <span class="toggle-text">辅助网格</span>
          </div>
          <n-switch v-model:value="showGrid" size="small" />
        </div>

        <!-- 拍照提示卡片 -->
        <Transition name="slide">
          <div v-if="showTip && isCameraActive" class="tip-card">
            <div class="tip-header">
              <span class="tip-icon">💡</span>
              <span class="tip-title">拍摄建议</span>
              <button class="tip-close" @click="closeTip">×</button>
            </div>
            <ul class="tip-content">
              <li>保持光线充足</li>
              <li>题目完整入镜</li>
              <li>避免手抖模糊</li>
            </ul>
          </div>
        </Transition>

        <!-- 已拍摄的照片缩略图（多题模式） -->
        <Transition name="slide">
          <div v-if="capturedPhotos.length > 0" class="captured-photos">
            <div class="photos-header">
              <span class="photos-count">已拍摄：{{ capturedPhotos.length }} 张</span>
              <n-button text type="primary" size="small" @click="finishCapture">
                完成
              </n-button>
            </div>
            <div class="photos-thumbnails">
              <div
                v-for="(photo, index) in capturedPhotos"
                :key="index"
                class="thumbnail-item"
                @click="removePhoto(index)"
              >
                <img :src="photo" class="thumbnail-img" alt="photo" />
                <div class="thumbnail-delete">×</div>
              </div>
              <div class="thumbnail-add" @click="takePhoto" v-if="capturedPhotos.length < 9">
                <span>+</span>
              </div>
            </div>
          </div>
        </Transition>

        <!-- 底部操作区 -->
        <div class="camera-controls">
          <!-- 相册按钮 -->
          <div class="control-btn album-btn" @click="openAlbum">
            <div class="btn-icon">📷</div>
            <div class="btn-label">相册</div>
          </div>

          <!-- 拍照按钮 -->
          <div class="control-btn camera-btn" @click="takePhoto">
            <div class="camera-btn-inner">
              <div class="shutter"></div>
            </div>
            <div class="btn-label">拍照</div>
          </div>

          <!-- 模式切换按钮 -->
          <div class="control-btn mode-btn" @click="toggleMode">
            <div class="btn-icon">{{ isMultiMode ? '➖' : '📒' }}</div>
            <div class="btn-label">{{ isMultiMode ? '单题' : '多题' }}</div>
          </div>
        </div>

        <!-- 确认按钮（拍摄后显示） -->
        <Transition name="slide">
          <div v-if="capturedImage && !isMultiMode" class="confirm-actions">
            <n-button class="retake-btn" size="large" @click="retakePhoto">
              重新拍摄
            </n-button>
            <n-button type="success" size="large" @click="confirmPhoto">
              确认使用
            </n-button>
          </div>
        </Transition>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import { NButton, NSwitch, useMessage } from 'naive-ui'

const props = defineProps<{
  show: boolean
  subject: 'chinese' | 'math' | 'english'
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'confirm', data: { subject: string; images: string[] }): void
}>()

const message = useMessage()

// 科目标签
const subjectLabel = computed(() => {
  const labels: Record<string, string> = {
    chinese: '语文',
    math: '数学',
    english: '英语'
  }
  return labels[props.subject] || ''
})

// 相机相关
const videoRef = ref<HTMLVideoElement | null>(null)
const isCameraActive = ref(false)
const cameraStream = ref<MediaStream | null>(null)

// 拍照相关
const capturedImage = ref<string | null>(null)
const capturedPhotos = ref<string[]>([])
const isMultiMode = ref(false)

// 辅助功能
const showGrid = ref(false)
const aiDetect = ref(true)
const showTip = ref(true)

// 初始化相机
const initCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment',
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      }
    })
    cameraStream.value = stream
    if (videoRef.value) {
      videoRef.value.srcObject = stream
    }
    isCameraActive.value = true
  } catch (error) {
    console.error('相机初始化失败:', error)
    message.error('无法访问相机，请检查权限设置')
  }
}

// 停止相机
const stopCamera = () => {
  if (cameraStream.value) {
    cameraStream.value.getTracks().forEach(track => track.stop())
    cameraStream.value = null
  }
  isCameraActive.value = false
}

// 拍照
const takePhoto = () => {
  if (!videoRef.value || !isCameraActive.value) {
    // 如果相机未启动，先启动相机
    initCamera()
    return
  }

  const video = videoRef.value
  const canvas = document.createElement('canvas')
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  const ctx = canvas.getContext('2d')
  if (ctx) {
    ctx.drawImage(video, 0, 0)
    const imageData = canvas.toDataURL('image/jpeg', 0.8)

    if (isMultiMode.value) {
      // 多题模式：添加到列表
      capturedPhotos.value.push(imageData)
      message.success(`已拍摄第 ${capturedPhotos.value.length} 张`)
    } else {
      // 单题模式：替换当前图片
      capturedImage.value = imageData
      stopCamera()
    }
  }
}

// 打开相册
const openAlbum = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.multiple = isMultiMode.value
  input.onchange = (e) => {
    const files = (e.target as HTMLInputElement).files
    if (files) {
      Array.from(files).forEach(file => {
        const reader = new FileReader()
        reader.onload = (event) => {
          const result = event.target?.result as string
          if (isMultiMode.value) {
            capturedPhotos.value.push(result)
          } else {
            capturedImage.value = result
            stopCamera()
          }
        }
        reader.readAsDataURL(file)
      })
    }
  }
  input.click()
}

// 重拍
const retakePhoto = () => {
  capturedImage.value = null
  initCamera()
}

// 确认使用
const confirmPhoto = () => {
  if (capturedImage.value) {
    emit('confirm', {
      subject: props.subject,
      images: [capturedImage.value]
    })
    handleClose()
  }
}

// 切换模式
const toggleMode = () => {
  isMultiMode.value = !isMultiMode.value
  if (!isMultiMode.value) {
    // 切换到单题模式时，清空多题模式的照片
    capturedPhotos.value = []
  }
}

// 删除照片
const removePhoto = (index: number) => {
  capturedPhotos.value.splice(index, 1)
}

// 完成拍摄（多题模式）
const finishCapture = () => {
  if (capturedPhotos.value.length > 0) {
    emit('confirm', {
      subject: props.subject,
      images: capturedPhotos.value
    })
    handleClose()
  }
}

// 关闭提示
const closeTip = () => {
  showTip.value = false
  // 7天内不再显示
  localStorage.setItem('photoTipLastClose', Date.now().toString())
}

// 关闭弹窗
const handleClose = () => {
  stopCamera()
  capturedImage.value = null
  capturedPhotos.value = []
  emit('update:show', false)
}

// 监听显示状态
watch(() => props.show, (newVal) => {
  if (newVal) {
    // 检查是否需要显示提示
    const lastClose = localStorage.getItem('photoTipLastClose')
    if (lastClose) {
      const days = 7
      const now = Date.now()
      if (now - parseInt(lastClose) < days * 24 * 60 * 60 * 1000) {
        showTip.value = false
      }
    }

    // 初始化相机
    initCamera()
  } else {
    stopCamera()
  }
})

// 组件卸载时停止相机
onBeforeUnmount(() => {
  stopCamera()
})
</script>

<style scoped>
/* 弹窗基础样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
  backdrop-filter: blur(4px);
}

.photo-capture-modal {
  background: #FFFFFF;
  border-radius: 20px;
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.25);
}

/* 弹窗头部 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #E2E8F0;
  background: linear-gradient(135deg, #14B8A6 0%, #2DD4BF 100%);
  color: white;
}

.modal-title-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-icon {
  font-size: 24px;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.modal-close {
  width: 36px;
  height: 36px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s;
}

.modal-close:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 相机预览区 */
.camera-preview-container {
  padding: 16px;
}

.camera-preview {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: 16px;
  overflow: hidden;
}

.camera-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.captured-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.camera-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #1E293B;
}

.placeholder-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.placeholder-text {
  font-size: 14px;
  color: #94A3B8;
}

/* 辅助网格 */
.grid-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.grid-line {
  position: absolute;
  background: rgba(255, 255, 255, 0.3);
}

.grid-line.horizontal {
  height: 1px;
  left: 0;
  right: 0;
}

.grid-line.vertical {
  width: 1px;
  top: 0;
  bottom: 0;
}

/* 题目识别框 */
.detect-frame {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 60%;
  border: 2px solid #3B82F6;
  border-radius: 12px;
}

.detect-corner {
  position: absolute;
  width: 20px;
  height: 20px;
  border: 3px solid #3B82F6;
}

.detect-corner.top-left {
  top: -2px;
  left: -2px;
  border-right: none;
  border-bottom: none;
}

.detect-corner.top-right {
  top: -2px;
  right: -2px;
  border-left: none;
  border-bottom: none;
}

.detect-corner.bottom-left {
  bottom: -2px;
  left: -2px;
  border-right: none;
  border-top: none;
}

.detect-corner.bottom-right {
  bottom: -2px;
  right: -2px;
  border-left: none;
  border-top: none;
}

.detect-label {
  position: absolute;
  top: -28px;
  left: 0;
  background: #3B82F6;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

/* 网格开关 */
.grid-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: #F8FAFC;
  margin: 0 16px 12px;
  border-radius: 12px;
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.toggle-icon {
  font-size: 18px;
}

.toggle-text {
  font-size: 14px;
  font-weight: 500;
  color: #1E293B;
}

/* 提示卡片 */
.tip-card {
  background: #FFFBEB;
  border: 1px solid #FCD34D;
  border-radius: 12px;
  padding: 14px 16px;
  margin: 0 16px 12px;
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}

.tip-icon {
  font-size: 16px;
}

.tip-title {
  font-size: 14px;
  font-weight: 600;
  color: #92400E;
  flex: 1;
}

.tip-close {
  background: none;
  border: none;
  font-size: 18px;
  color: #92400E;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tip-content {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tip-content li {
  font-size: 13px;
  color: #78350F;
  line-height: 1.8;
  padding-left: 16px;
  position: relative;
}

.tip-content li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #F59E0B;
}

/* 已拍摄照片 */
.captured-photos {
  padding: 12px 16px;
  background: #F8FAFC;
  margin: 0 16px 12px;
  border-radius: 12px;
}

.photos-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.photos-count {
  font-size: 14px;
  font-weight: 500;
  color: #1E293B;
}

.photos-thumbnails {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.thumbnail-item {
  position: relative;
  width: 60px;
  height: 60px;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  flex-shrink: 0;
}

.thumbnail-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-delete {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 18px;
  height: 18px;
  background: rgba(239, 68, 68, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  opacity: 0;
  transition: opacity 0.2s;
}

.thumbnail-item:hover .thumbnail-delete {
  opacity: 1;
}

.thumbnail-add {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  border: 2px dashed #CBD5E1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  color: #94A3B8;
  font-size: 24px;
}

/* 底部操作区 */
.camera-controls {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 20px 16px;
  background: white;
  border-top: 1px solid #E2E8F0;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.btn-icon {
  font-size: 24px;
}

.btn-label {
  font-size: 12px;
  color: #64748B;
}

/* 拍照按钮 */
.camera-btn-inner {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3B82F6, #2563EB);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  transition: all 0.2s;
}

.camera-btn:active .camera-btn-inner {
  transform: scale(0.95);
}

.shutter {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: white;
  border: 4px solid #3B82F6;
}

.camera-btn .btn-label {
  color: #3B82F6;
  font-weight: 600;
}

/* 确认操作 */
.confirm-actions {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: white;
  border-top: 1px solid #E2E8F0;
}

.confirm-actions .n-button {
  flex: 1;
  height: 48px;
  font-weight: 600;
}

.retake-btn {
  background: #F1F5F9 !important;
  border: none !important;
}

/* 动画 */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .photo-capture-modal,
.modal-leave-to .photo-capture-modal {
  transform: scale(0.9) translateY(20px);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>