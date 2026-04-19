<template>
  <div class="ai-input-box">
    <div class="input-wrapper" :class="{ 'focused': isFocused }">
      <!-- 相机按钮 -->
      <button 
        v-if="showCamera" 
        class="action-btn camera-btn" 
        @click="handleCamera" 
        title="拍照/相册"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
          <circle cx="12" cy="13" r="4"></circle>
        </svg>
      </button>
      
      <!-- 语音按钮 -->
      <button 
        v-if="showVoice" 
        class="action-btn voice-btn" 
        @click="handleVoice" 
        title="语音输入"
      >
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      </button>
      
      <!-- 输入框 -->
      <input 
        v-model="inputValue"
        class="input-field" 
        :placeholder="placeholder"
        @focus="handleFocus"
        @blur="handleBlur"
        @keyup.enter="handleEnter"
      />
      
      <!-- 发送按钮 -->
      <button class="send-btn" @click="handleSend" title="发送">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </div>
    
    <!-- 快捷短语 -->
    <div v-if="quickPhrases && quickPhrases.length > 0" class="quick-phrases">
      <div 
        v-for="(phrase, index) in quickPhrases" 
        :key="index"
        class="phrase-tag"
        @click="selectPhrase(phrase)"
      >
        <span class="phrase-icon">{{ phrase.icon }}</span>
        <span class="phrase-text">{{ phrase.text }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface QuickPhrase {
  icon: string
  text: string
  mode?: string
  action?: string
}

interface Props {
  modelValue?: string
  placeholder?: string
  showCamera?: boolean
  showVoice?: boolean
  quickPhrases?: QuickPhrase[]
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  placeholder: '接着问点什么...',
  showCamera: true,
  showVoice: true,
  quickPhrases: () => [],
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'submit', value: string): void
  (e: 'voice'): void
  (e: 'camera', file: File): void
  (e: 'phrase-select', phrase: QuickPhrase): void
}>()

const inputValue = ref(props.modelValue)
const isFocused = ref(false)

watch(() => props.modelValue, (val) => {
  inputValue.value = val
})

watch(inputValue, (val) => {
  emit('update:modelValue', val)
})

const handleFocus = () => {
  isFocused.value = true
}

const handleBlur = () => {
  isFocused.value = false
}

const handleEnter = () => {
  handleSend()
}

const handleSend = () => {
  if (!inputValue.value.trim()) return
  emit('submit', inputValue.value)
  inputValue.value = ''
}

const handleVoice = () => {
  emit('voice')
}

const handleCamera = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.capture = 'environment'
  
  input.onchange = (e) => {
    const target = e.target as HTMLInputElement
    const file = target?.files?.[0]
    if (file) {
      emit('camera', file)
    }
  }
  
  input.click()
}

const selectPhrase = (phrase: QuickPhrase) => {
  emit('phrase-select', phrase)
}
</script>

<style scoped>
.ai-input-box {
  width: 100%;
}

.input-wrapper {
  display: flex;
  align-items: center;
  background: #F5F5F5;
  border-radius: 24px;
  padding: 6px 8px;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.input-wrapper.focused {
  background: #FFFFFF;
  border-color: #14B8A6;
  box-shadow: 0 0 0 4px rgba(20, 184, 166, 0.08);
}

.action-btn {
  width: 36px;
  height: 36px;
  border: 2px solid #E0E0E0;
  background: #FFFFFF;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #333333;
  transition: all 0.3s;
  flex-shrink: 0;
}

.action-btn:hover {
  border-color: #14B8A6;
  color: #14B8A6;
  transform: scale(1.05);
}

.camera-btn {
  margin-right: 6px;
}

.voice-btn {
  margin-right: 8px;
}

.input-field {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  color: #333333;
  background: transparent;
  padding: 10px 4px;
}

.input-field::placeholder {
  color: #999999;
}

.send-btn {
  width: 42px;
  height: 42px;
  border: none;
  background: #333333;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  transition: all 0.3s;
  flex-shrink: 0;
  margin-left: 8px;
}

.send-btn:hover {
  background: #14B8A6;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
}

/* 快捷短语 */
.quick-phrases {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.phrase-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 13px;
  color: #64748B;
}

.phrase-tag:hover {
  border-color: #14B8A6;
  background: rgba(20, 184, 166, 0.05);
  color: #14B8A6;
  transform: translateY(-2px);
}

.phrase-icon {
  font-size: 16px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .action-btn {
    width: 34px;
    height: 34px;
  }
  
  .send-btn {
    width: 38px;
    height: 38px;
  }
  
  .input-field {
    font-size: 14px;
  }
  
  .phrase-tag {
    padding: 6px 12px;
    font-size: 12px;
  }
}
</style>
