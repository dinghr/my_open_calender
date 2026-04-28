<template>
  <div class="poetry-chat">
    <!-- 对话历史区域 -->
    <div class="chat-history" ref="chatHistoryRef">
      <div v-for="(msg, index) in messages" :key="index" class="chat-message" :class="msg.role">
        <!-- 助手头像 -->
        <div v-if="msg.role === 'assistant'" class="avatar-wrapper">
          <div class="assistant-avatar">🎓</div>
        </div>

        <!-- 消息内容 -->
        <div class="message-wrapper">
          <div class="message-bubble">
            <span v-if="msg.isTyping" class="typing-content">{{ msg.displayText }}<span class="cursor">|</span></span>
            <span v-else>{{ msg.content }}</span>
          </div>
        </div>
      </div>

      <!-- 加载指示器 -->
      <div v-if="loading" class="chat-message assistant">
        <div class="avatar-wrapper">
          <div class="assistant-avatar">🎓</div>
        </div>
        <div class="message-wrapper">
          <div class="message-bubble loading">
            <span class="loading-dots">
              <span></span><span></span><span></span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷选择标签 -->
    <div class="quick-tags" v-if="!currentPoetry">
      <div class="tags-label">💡 快捷选择</div>
      <div class="tags-grid">
        <div
          v-for="tag in quickTags"
          :key="tag.value"
          class="quick-tag"
          @click="selectTag(tag)"
        >
          {{ tag.icon }} {{ tag.label }}
        </div>
      </div>
    </div>

    <!-- 开始学习按钮 -->
    <div class="start-learn-btn" v-if="currentPoetry && !isTyping">
      <n-button type="success" size="large" block @click="startLearning">
        📖 开始学习这首诗
      </n-button>
    </div>

    <!-- 输入框 -->
    <div class="input-area">
      <div class="input-wrapper">
        <input
          v-model="userInput"
          type="text"
          placeholder="输入你想学的古诗..."
          @keyup.enter="sendMessage"
          :disabled="loading || isTyping"
        />
        <button class="send-btn" @click="sendMessage" :disabled="loading || isTyping || !userInput.trim()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { NButton, useMessage } from 'naive-ui'
import { poetryApi } from '../api'

const props = defineProps({
  studentId: String,
  grade: { type: Number, default: 1 }
})

const emit = defineEmits(['poetry-ready'])

const message = useMessage()
const messages = ref([])
const userInput = ref('')
const loading = ref(false)
const isTyping = ref(false)
const currentPoetry = ref(null)
const chatHistoryRef = ref(null)

// 快捷标签
const quickTags = [
  { label: '李白', value: '李白', icon: '🌙' },
  { label: '杜甫', value: '杜甫', icon: '🏔️' },
  { label: '春天', value: '春天', icon: '🌸' },
  { label: '思乡', value: '思乡', icon: '🏠' },
  { label: '送别', value: '送别', icon: '👋' },
  { label: '随机', value: '', icon: '🎲' },
]

// 初始化欢迎消息
const initWelcome = () => {
  messages.value = [
    {
      role: 'assistant',
      content: '你好呀！我是小E老师。想要学习什么古诗呢？要不要学一首李白的诗？或者告诉我你喜欢的主题，我来推荐适合的古诗！'
    }
  ]
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatHistoryRef.value) {
      chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight
    }
  })
}

// 打字机效果
const typewriterEffect = async (text, msgIndex) => {
  isTyping.value = true
  const msg = messages.value[msgIndex]
  if (!msg) {
    isTyping.value = false
    return
  }
  msg.isTyping = true
  msg.displayText = ''

  for (let i = 0; i < text.length; i++) {
    if (!isTyping.value) break
    msg.displayText = text.substring(0, i + 1)
    scrollToBottom()
    await new Promise(resolve => setTimeout(resolve, 30 + Math.random() * 20))
  }

  if (msg) {
    msg.content = text
    msg.isTyping = false
  }
  isTyping.value = false
}

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value || isTyping.value) return

  const keyword = userInput.value.trim()
  messages.value.push({ role: 'user', content: keyword })
  userInput.value = ''
  loading.value = true
  scrollToBottom()

  try {
    const res = await poetryApi.chat({
      message: keyword,
      student_id: props.studentId,
      grade: props.grade || 1,
      textbook: '人教版'
    })

    // 添加助手回复消息（打字机效果）
    const msgIndex = messages.value.length
    messages.value.push({
      role: 'assistant',
      content: '',
      isTyping: true,
      displayText: ''
    })

    loading.value = false

    if (res.data && !res.data.error && res.data.poetry) {
      currentPoetry.value = res.data.poetry

      // 使用后端返回的介绍文本
      const introText = res.data.reply || generateIntroText(res.data.poetry)

      // 打字机效果展示介绍
      await typewriterEffect(introText, msgIndex)

      // 通知父组件古诗已准备好
      emit('poetry-ready', res.data.poetry)
    } else {
      const errMsg = messages.value[msgIndex]
      if (errMsg) {
        errMsg.content = res.data?.reply || '抱歉，没有找到相关的古诗。换个关键词试试？'
        errMsg.isTyping = false
      }
    }
  } catch (e) {
    loading.value = false
    message.error('加载古诗失败')
    messages.value.push({
      role: 'assistant',
      content: '哎呀，出了点问题。请稍后再试～'
    })
  }

  scrollToBottom()
}

// 选择快捷标签
const selectTag = (tag) => {
  userInput.value = tag.value || '随机推荐'
  sendMessage()
}

// 生成介绍文本
const generateIntroText = (poetry) => {
  const intros = [
    `这首诗是《${poetry.title}》，作者是${poetry.dynasty ? poetry.dynasty + '代' : ''}诗人${poetry.author || '佚名'}。`,
    poetry.annotation?.background
      ? `${poetry.annotation.background}`
      : `这是一首非常优美的古诗，很适合你这个年级学习哦！`,
    `诗歌内容：${poetry.lines?.map(l => l.text).join('，') || ''}`,
    `让我来告诉你这首诗的意思吧：${poetry.translation || '这首诗描绘了一幅美丽的画面。'}`,
    `点击"开始学习"按钮，我们一起来学习这首诗吧！`
  ]

  return intros.filter(Boolean).join('\n\n')
}

// 开始学习
const startLearning = () => {
  if (currentPoetry.value) {
    emit('poetry-ready', currentPoetry.value)
  }
}

// 初始化
initWelcome()
</script>

<style scoped>
.poetry-chat {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 400px;
  background: linear-gradient(180deg, #FFFBEB 0%, #FEF3C7 100%);
  border-radius: 16px;
  overflow: hidden;
}

/* 对话历史 */
.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.chat-message {
  display: flex;
  gap: 12px;
  max-width: 100%;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.avatar-wrapper {
  flex-shrink: 0;
}

.assistant-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.message-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-message.user .message-wrapper {
  align-items: flex-end;
}

.chat-message.assistant .message-wrapper {
  align-items: flex-start;
}

.message-bubble {
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-message.user .message-bubble {
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  color: #FFFFFF;
  border-bottom-right-radius: 4px;
}

.chat-message.assistant .message-bubble {
  background: #FFFFFF;
  color: #78350F;
  border-bottom-left-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.message-bubble.loading {
  padding: 16px 20px;
}

/* 打字效果 */
.typing-content {
  position: relative;
}

.cursor {
  animation: blink 1s infinite;
  color: #F59E0B;
  font-weight: bold;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* 加载动画 */
.loading-dots {
  display: flex;
  gap: 4px;
}

.loading-dots span {
  width: 8px;
  height: 8px;
  background: #F59E0B;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.loading-dots span:nth-child(1) { animation-delay: 0s; }
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

/* 快捷标签 */
.quick-tags {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.8);
  border-top: 1px solid rgba(245, 158, 11, 0.2);
}

.tags-label {
  font-size: 13px;
  color: #92400E;
  margin-bottom: 10px;
  font-weight: 500;
}

.tags-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.quick-tag {
  padding: 8px 14px;
  background: #FFFFFF;
  border: 1px solid rgba(245, 158, 11, 0.3);
  border-radius: 20px;
  font-size: 13px;
  color: #78350F;
  cursor: pointer;
  transition: all 0.3s;
}

.quick-tag:hover {
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  color: #FFFFFF;
  border-color: transparent;
  transform: translateY(-2px);
}

/* 开始学习按钮 */
.start-learn-btn {
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.8);
  border-top: 1px solid rgba(245, 158, 11, 0.2);
}

/* 输入区域 */
.input-area {
  padding: 12px 16px;
  background: #FFFFFF;
  border-top: 1px solid rgba(245, 158, 11, 0.2);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #FEF3C7;
  border-radius: 24px;
  padding: 4px 4px 4px 16px;
}

.input-wrapper input {
  flex: 1;
  border: none;
  background: transparent;
  font-size: 14px;
  color: #78350F;
  outline: none;
}

.input-wrapper input::placeholder {
  color: #B45309;
  opacity: 0.6;
}

.send-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  border-radius: 50%;
  color: #FFFFFF;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>