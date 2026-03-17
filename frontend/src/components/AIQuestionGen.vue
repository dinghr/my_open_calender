<template>
  <div class="ai-learn-page">
    <!-- 顶部欢迎区 -->
    <div class="welcome-section">
      <div class="welcome-header">
        <div class="welcome-icon">🤖</div>
        <div class="welcome-text">
          <h1 class="page-title">AI 伴学</h1>
          <p class="page-subtitle">告诉 AI 你想学什么，马上开始</p>
        </div>
      </div>
    </div>

    <!-- 快捷输入区 -->
    <div class="quick-input-section">
      <AIInputBox
        v-model="userInput"
        placeholder="接着问点什么..."
        :show-camera="true"
        :show-voice="true"
        :quick-phrases="quickPhrases"
        @submit="handleInput"
        @voice="handleVoice"
        @camera="handleCamera"
        @phrase-select="selectPhrase"
      />
    </div>

    <!-- 学习模式选择 -->
    <div class="mode-section">
      <div class="section-header">
        <h2 class="section-title">选择学习模式</h2>
        <span class="section-count">{{ modeList.length }} 个模式</span>
      </div>
      
      <div class="mode-grid">
        <div 
          v-for="mode in modeList" 
          :key="mode.key"
          class="mode-card"
          :class="{ 'mode-card-lg': mode.large }"
          @click="selectMode(mode.key)"
        >
          <div class="mode-icon-wrapper" :style="{ background: mode.gradient }">
            <span class="mode-icon">{{ mode.icon }}</span>
          </div>
          <div class="mode-content">
            <div class="mode-name">{{ mode.name }}</div>
            <div class="mode-desc">{{ mode.desc }}</div>
          </div>
          <div class="mode-arrow">›</div>
        </div>
      </div>
    </div>

    <!-- 学习记录 -->
    <div v-if="!currentMode && learningHistory.length > 0" class="history-section">
      <div class="section-header">
        <h2 class="section-title">最近学习</h2>
        <n-button text size="small" @click="clearHistory">清空</n-button>
      </div>
      <div class="history-list">
        <div 
          v-for="(record, index) in learningHistory.slice(0, 5)" 
          :key="index"
          class="history-item"
          @click="resumeLearning(record)"
        >
          <div class="history-icon" :style="{ background: record.color }">{{ record.icon }}</div>
          <div class="history-info">
            <div class="history-name">{{ record.name }}</div>
            <div class="history-time">{{ record.time }}</div>
          </div>
          <span class="history-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </span>
        </div>
      </div>
    </div>

    <!-- 学习弹窗 -->
    <Transition name="modal">
      <div v-if="currentMode" class="modal-overlay" @click.self="closeLearning">
        <div class="modal-content">
          <!-- 弹窗头部 -->
          <div class="modal-header">
            <div class="modal-title-wrapper">
              <span class="modal-icon">{{ modeList.find(m => m.key === currentMode)?.icon }}</span>
              <h3 class="modal-title">{{ modeList.find(m => m.key === currentMode)?.name }}</h3>
            </div>
            <button class="modal-close" @click="closeLearning">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- 弹窗内容区 -->
          <div class="modal-body">
            <!-- 背单词模式 -->
            <div v-if="currentMode === 'vocabulary'" class="learn-mode">
              <div class="word-card">
                <div class="word-main">
                  <div class="word-text">{{ currentWord.word }}</div>
                  <div class="word-phonetic">/{{ currentWord.phonetic }}/</div>
                </div>
                <div class="word-meaning">{{ currentWord.meaning }}</div>
                <div class="word-example">
                  <span class="example-label">例句：</span>
                  <span class="example-text">{{ currentWord.example }}</span>
                </div>
              </div>
              <div class="nav-buttons">
                <n-button @click="prevWord" :disabled="currentWordIndex === 0">
                  ← 上一个
                </n-button>
                <span class="progress-indicator">{{ currentWordIndex + 1 }} / {{ vocabularyList.length }}</span>
                <n-button type="success" @click="nextWord" :disabled="currentWordIndex === vocabularyList.length - 1">
                  下一个 →
                </n-button>
              </div>
            </div>

            <!-- 背古诗模式 -->
            <div v-if="currentMode === 'poetry'" class="learn-mode">
              <div class="poetry-card">
                <div class="poetry-title">{{ currentPoetry.title }}</div>
                <div class="poetry-author">{{ currentPoetry.author }}</div>
                <div class="poetry-content">
                  <div v-for="line in currentPoetry.lines" :key="line" class="poetry-line">
                    {{ line }}
                  </div>
                </div>
                <div class="poetry-translation">
                  <div class="translation-label">译文：</div>
                  <div class="translation-text">{{ currentPoetry.translation }}</div>
                </div>
              </div>
              <div class="nav-buttons">
                <n-button @click="prevPoetry" :disabled="currentPoetryIndex === 0">
                  ← 上一首
                </n-button>
                <span class="progress-indicator">{{ currentPoetryIndex + 1 }} / {{ poetryList.length }}</span>
                <n-button type="success" @click="nextPoetry" :disabled="currentPoetryIndex === poetryList.length - 1">
                  下一首 →
                </n-button>
              </div>
            </div>

            <!-- 错题复习模式 -->
            <div v-if="currentMode === 'wrongReview'" class="learn-mode">
              <div class="wrong-card">
                <div class="wrong-question">{{ currentWrong.question }}</div>
                <div class="wrong-answer-section">
                  <div class="wrong-user-answer">
                    <span class="answer-label">你的答案：</span>
                    <span class="answer-value wrong">{{ currentWrong.userAnswer }}</span>
                  </div>
                  <div class="wrong-correct-answer">
                    <span class="answer-label">正确答案：</span>
                    <span class="answer-value correct">{{ currentWrong.correctAnswer }}</span>
                  </div>
                </div>
                <div class="wrong-analysis">
                  <div class="analysis-title">💡 错因分析</div>
                  <div class="analysis-text">{{ currentWrong.analysis }}</div>
                </div>
                <div class="wrong-similar">
                  <div class="similar-title">📝 举一反三</div>
                  <div class="similar-text">{{ currentWrong.similar }}</div>
                </div>
              </div>
              <div class="nav-buttons">
                <n-button @click="prevWrong" :disabled="currentWrongIndex === 0">
                  ← 上一题
                </n-button>
                <span class="progress-indicator">{{ currentWrongIndex + 1 }} / {{ wrongList.length }}</span>
                <n-button type="success" @click="nextWrong" :disabled="currentWrongIndex === wrongList.length - 1">
                  下一题 →
                </n-button>
              </div>
            </div>

            <!-- 每日出题/口算/同步/挑战模式 -->
            <div v-if="['daily', 'math', 'school', 'challenge'].includes(currentMode)" class="learn-mode">
              <div class="question-card">
                <div class="question-header">
                  <n-tag size="small" :type="getSubjectTagType(currentMode)">{{ questionSubject }}</n-tag>
                </div>
                <div class="question-text">{{ currentQuestion }}</div>
                <div class="question-input-wrapper">
                  <n-input 
                    v-model:value="userAnswer" 
                    placeholder="输入你的答案" 
                    size="large"
                    @keyup.enter="checkAnswer"
                  />
                </div>
              </div>
              <div class="nav-buttons">
                <n-button @click="skipQuestion">跳过</n-button>
                <n-button type="success" @click="checkAnswer">提交答案</n-button>
              </div>
              <Transition name="fade">
                <div v-if="answerResult" class="answer-result" :class="answerResult.correct ? 'correct' : 'wrong'">
                  <span class="result-icon">{{ answerResult.correct ? '✅' : '❌' }}</span>
                  <span class="result-text">{{ answerResult.message }}</span>
                </div>
              </Transition>
            </div>

            <!-- 打印试卷模式 -->
            <div v-if="currentMode === 'print'" class="learn-mode">
              <div class="print-card">
                <div class="print-preview">
                  <div class="preview-header">
                    <span class="preview-icon">📄</span>
                    <span class="preview-title">试卷预览</span>
                  </div>
                  <div class="preview-content">
                    <div class="preview-title-text">{{ printTypeOptions.find(o => o.value === printType)?.label }}</div>
                    <div class="preview-info">共 {{ printCount }} 题 · {{ showAnswer ? '含答案' : '不含答案' }}</div>
                  </div>
                </div>
                <div class="print-settings">
                  <div class="setting-row">
                    <span class="setting-label">试卷类型</span>
                    <n-select v-model:value="printType" :options="printTypeOptions" size="medium" style="width: 140px" />
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">题目数量</span>
                    <n-select v-model:value="printCount" :options="printCountOptions" size="medium" style="width: 100px" />
                  </div>
                  <div class="setting-row">
                    <span class="setting-label">显示答案</span>
                    <n-switch v-model:value="showAnswer" />
                  </div>
                </div>
              </div>
              <div class="print-actions">
                <n-button type="success" size="large" @click="handlePrint" block>
                  🖨️ 生成并打印试卷
                </n-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import AIInputBox from './AIInputBox.vue'

// 用户输入
const userInput = ref('')

// 模式列表
const modeList = ref([
  { key: 'vocabulary', name: '背单词', desc: '每日 10 词，轻松记忆', icon: '📖', gradient: 'linear-gradient(135deg, #14B8A6 0%, #2DD4BF 100%)', color: 'rgba(20, 184, 166, 0.1)' },
  { key: 'poetry', name: '背古诗', desc: '唐诗宋词，带拼音译文', icon: '📜', gradient: 'linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%)', color: 'rgba(139, 92, 246, 0.1)' },
  { key: 'wrongReview', name: '错题复习', desc: '薄弱点强化，举一反三', icon: '📕', gradient: 'linear-gradient(135deg, #EF4444 0%, #F87171 100%)', color: 'rgba(239, 68, 68, 0.1)' },
  { key: 'daily', name: '每日出题', desc: 'AI 智能推荐适合你的难度', icon: '📝', gradient: 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)', color: 'rgba(245, 158, 11, 0.1)', large: true },
  { key: 'math', name: '口算练习', desc: '速算训练，提升计算力', icon: '🔢', gradient: 'linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%)', color: 'rgba(59, 130, 246, 0.1)' },
  { key: 'school', name: '同步进度', desc: '课堂同步，巩固当天知识', icon: '📚', gradient: 'linear-gradient(135deg, #10B981 0%, #34D399 100%)', color: 'rgba(16, 185, 129, 0.1)' },
  { key: 'challenge', name: '思维挑战', desc: '奥数思维，挑战高阶题', icon: '🚀', gradient: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)', color: 'rgba(249, 115, 22, 0.1)' },
  { key: 'print', name: '打印试卷', desc: 'A4 组卷，随时打印', icon: '🖨️', gradient: 'linear-gradient(135deg, #EC4899 0%, #F472B6 100%)', color: 'rgba(236, 72, 153, 0.1)', large: true },
])

// 快捷短语
const quickPhrases = ref([
  { icon: '📕', text: '错题复习', mode: 'wrongReview' },
  { icon: '🏫', text: '学校进度', mode: 'school' },
  { icon: '🚀', text: '增强挑战', mode: 'challenge' },
  { icon: '🔢', text: '口算练习', mode: 'math' },
  { icon: '📖', text: '背单词', mode: 'vocabulary' },
])

// 当前模式
const currentMode = ref(null)

// 背单词数据
const currentWordIndex = ref(0)
const vocabularyList = ref([
  { word: 'apple', phonetic: 'ˈæpl', meaning: 'n. 苹果', example: 'I eat an apple every day.' },
  { word: 'beautiful', phonetic: 'ˈbjuːtɪfl', meaning: 'adj. 美丽的', example: 'The flower is beautiful.' },
  { word: 'challenge', phonetic: 'ˈtʃælɪndʒ', meaning: 'n. 挑战', example: 'This is a big challenge.' },
  { word: 'discover', phonetic: 'dɪˈskʌvər', meaning: 'v. 发现', example: 'We discovered a new planet.' },
  { word: 'energy', phonetic: 'ˈenərdʒi', meaning: 'n. 能量', example: 'Solar energy is clean.' },
])
const currentWord = computed(() => vocabularyList.value[currentWordIndex.value])

// 背古诗数据
const currentPoetryIndex = ref(0)
const poetryList = ref([
  { 
    title: '静夜思', 
    author: '唐·李白',
    lines: ['床前明月光，', '疑是地上霜。', '举头望明月，', '低头思故乡。'],
    translation: '明亮的月光洒在床前，好像地上泛起了一层白霜。我抬头看天上的明月，不禁低头思念远方的故乡。'
  },
  { 
    title: '春晓', 
    author: '唐·孟浩然',
    lines: ['春眠不觉晓，', '处处闻啼鸟。', '夜来风雨声，', '花落知多少。'],
    translation: '春天睡得香甜，不知不觉天已亮了。到处都能听到鸟儿的叫声。想起昨夜的风雨，不知道花儿被打落了多少。'
  },
  { 
    title: '登鹳雀楼', 
    author: '唐·王之涣',
    lines: ['白日依山尽，', '黄河入海流。', '欲穷千里目，', '更上一层楼。'],
    translation: '夕阳依傍着西山慢慢落下，黄河朝着东海滔滔奔流。想要看尽千里风光，就要再登上一层高楼。'
  },
])
const currentPoetry = computed(() => poetryList.value[currentPoetryIndex.value])

// 错题复习数据
const currentWrongIndex = ref(0)
const wrongList = ref([
  { 
    question: '36 ÷ 4 = ?', 
    userAnswer: '8', 
    correctAnswer: '9',
    analysis: '除法计算错误。36 ÷ 4 表示把 36 平均分成 4 份，每份是 9。可以用乘法口诀验证：4 × 9 = 36。',
    similar: '类似题：48 ÷ 6 = ? （答案：8）'
  },
  { 
    question: '一个长方形的长是 8cm，宽是 5cm，周长是多少？', 
    userAnswer: '13cm', 
    correctAnswer: '26cm',
    analysis: '周长公式记错了。长方形周长 = (长 + 宽) × 2 = (8 + 5) × 2 = 26cm。你只计算了长 + 宽，忘记乘以 2 了。',
    similar: '类似题：长 10cm，宽 6cm 的长方形周长是？（答案：32cm）'
  },
])
const currentWrong = computed(() => wrongList.value[currentWrongIndex.value])

// 每日出题数据
const currentQuestion = ref('25 × 4 = ?')
const questionSubject = ref('数学 · 三年级')
const userAnswer = ref('')
const answerResult = ref(null)
const currentQuestionAnswer = ref('')

// 打印设置
const printType = ref('wrongReview')
const printCount = ref(10)
const printTypeOptions = ref([
  { label: '错题复习卷', value: 'wrongReview' },
  { label: '同步练习卷', value: 'school' },
  { label: '口算速算卷', value: 'math' },
  { label: '思维挑战卷', value: 'challenge' },
])
const printCountOptions = ref([
  { label: '10 题', value: 10 },
  { label: '15 题', value: 15 },
  { label: '20 题', value: 20 },
])
const showAnswer = ref(false)

// 学习记录
const learningHistory = ref([
  { icon: '📖', name: '背单词', time: '10 分钟前', mode: 'vocabulary', color: 'rgba(20, 184, 166, 0.1)' },
  { icon: '📕', name: '错题复习', time: '1 小时前', mode: 'wrongReview', color: 'rgba(239, 68, 68, 0.1)' },
  { icon: '📝', name: '每日出题', time: '昨天', mode: 'daily', color: 'rgba(245, 158, 11, 0.1)' },
])

// 方法
const handleInput = () => {
  if (!userInput.value.trim()) return
  console.log('用户输入:', userInput.value)
  userInput.value = ''
}

const handleVoice = () => {
  console.log('语音输入')
  // TODO: 调用语音识别 API
}

const handleCamera = () => {
  // 创建隐藏的文件输入框
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.capture = 'environment'
  
  input.onchange = (e) => {
    const target = e.target
    const file = target?.files?.[0]
    if (file) {
      console.log('选择的图片:', file)
      alert(`已选择图片：${file.name}\n（待实现 OCR 识别）`)
    }
  }
  
  input.click()
}

const selectPhrase = (phrase) => {
  selectMode(phrase.mode)
}

const selectMode = (mode) => {
  currentMode.value = mode
  currentWordIndex.value = 0
  currentPoetryIndex.value = 0
  currentWrongIndex.value = 0
  userAnswer.value = ''
  answerResult.value = null
  
  if (['daily', 'math', 'school', 'challenge'].includes(mode)) {
    generateQuestion(mode)
  }
  
  addToHistory(mode)
}

const closeLearning = () => {
  currentMode.value = null
}

const addToHistory = (mode) => {
  const modeInfo = modeList.value.find(m => m.key === mode)
  learningHistory.value.unshift({
    icon: modeInfo.icon,
    name: modeInfo.name,
    time: '刚刚',
    mode: mode,
    color: modeInfo.color,
  })
}

const resumeLearning = (record) => {
  selectMode(record.mode)
}

const clearHistory = () => {
  learningHistory.value = []
}

// 背单词导航
const prevWord = () => {
  if (currentWordIndex.value > 0) currentWordIndex.value--
}

const nextWord = () => {
  if (currentWordIndex.value < vocabularyList.value.length - 1) currentWordIndex.value++
}

// 背古诗导航
const prevPoetry = () => {
  if (currentPoetryIndex.value > 0) currentPoetryIndex.value--
}

const nextPoetry = () => {
  if (currentPoetryIndex.value < poetryList.value.length - 1) currentPoetryIndex.value++
}

// 错题复习导航
const prevWrong = () => {
  if (currentWrongIndex.value > 0) currentWrongIndex.value--
}

const nextWrong = () => {
  if (currentWrongIndex.value < wrongList.value.length - 1) currentWrongIndex.value++
}

// 获取题目标签类型
const getSubjectTagType = (mode) => {
  const types = { daily: 'warning', math: 'info', school: 'success', challenge: 'error' }
  return types[mode] || 'default'
}

// 生成题目
const generateQuestion = (mode) => {
  const questions = {
    daily: [
      { text: '25 × 4 = ?', subject: '数学 · 三年级', answer: '100' },
      { text: '3/4 + 1/4 = ?', subject: '数学 · 三年级', answer: '1' },
      { text: '1 小时 = ? 分钟', subject: '数学 · 三年级', answer: '60' },
    ],
    math: [
      { text: '15 + 27 = ?', subject: '口算 · 加法', answer: '42' },
      { text: '50 - 23 = ?', subject: '口算 · 减法', answer: '27' },
      { text: '8 × 7 = ?', subject: '口算 · 乘法', answer: '56' },
    ],
    school: [
      { text: '写出"美丽"的近义词', subject: '语文 · 三年级', answer: '漂亮' },
      { text: '《静夜思》的作者是谁？', subject: '语文 · 三年级', answer: '李白' },
    ],
    challenge: [
      { text: '1 + 2 + 3 + ... + 100 = ?', subject: '奥数 · 求和', answer: '5050' },
      { text: '鸡兔同笼，头 10 个，脚 28 只，问鸡兔各几只？', subject: '奥数 · 应用题', answer: '鸡 6 只，兔 4 只' },
    ],
  }
  
  const q = questions[mode][Math.floor(Math.random() * questions[mode].length)]
  currentQuestion.value = q.text
  questionSubject.value = q.subject
  currentQuestionAnswer.value = q.answer
}

const skipQuestion = () => {
  generateQuestion(currentMode.value)
  userAnswer.value = ''
  answerResult.value = null
}

const checkAnswer = () => {
  if (!userAnswer.value.trim()) return
  
  const isCorrect = userAnswer.value.trim() === currentQuestionAnswer.value
  answerResult.value = {
    correct: isCorrect,
    message: isCorrect ? '太棒了！回答正确！' : `不对哦，正确答案是：${currentQuestionAnswer.value}`,
  }
  
  if (isCorrect) {
    // TODO: 增加积分
  }
  
  setTimeout(() => {
    skipQuestion()
  }, 2000)
}

const handlePrint = () => {
  console.log('打印试卷:', { type: printType.value, count: printCount.value, showAnswer: showAnswer.value })
  alert('试卷生成中，请稍候...')
}
</script>

<style scoped>
.ai-learn-page {
  min-height: 100vh;
  background: #F8FAFC;
  padding: 20px 16px;
  padding-bottom: 100px;
}

/* 欢迎区 */
.welcome-section {
  margin-bottom: 20px;
}

.welcome-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.welcome-icon {
  font-size: 36px;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(45, 212, 191, 0.1) 100%);
  border-radius: 16px;
}

.welcome-text {
  flex: 1;
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1E293B;
  margin: 0 0 4px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #64748B;
  margin: 0;
}

/* 快捷输入区 */
.quick-input-section {
  margin-bottom: 24px;
}

/* 模式选择区 */
.mode-section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
  margin: 0;
}

.section-count {
  font-size: 13px;
  color: #94A3B8;
}

.mode-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.mode-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #FFFFFF;
  border-radius: 16px;
  padding: 14px 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid transparent;
}

.mode-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: rgba(20, 184, 166, 0.2);
}

.mode-card-lg {
  grid-column: span 2;
}

.mode-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.mode-icon {
  font-size: 22px;
}

.mode-content {
  flex: 1;
  min-width: 0;
}

.mode-name {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 2px;
}

.mode-desc {
  font-size: 12px;
  color: #64748B;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mode-arrow {
  font-size: 20px;
  color: #CBD5E1;
  transition: all 0.3s;
}

.mode-card:hover .mode-arrow {
  color: #14B8A6;
  transform: translateX(4px);
}

/* 历史记录 */
.history-section {
  margin-top: 24px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #FFFFFF;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid transparent;
}

.history-item:hover {
  background: #F8FAFC;
  border-color: rgba(20, 184, 166, 0.2);
  transform: translateX(4px);
}

.history-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.history-info {
  flex: 1;
  min-width: 0;
}

.history-name {
  font-size: 14px;
  font-weight: 500;
  color: #1E293B;
  margin-bottom: 2px;
}

.history-time {
  font-size: 12px;
  color: #94A3B8;
}

.history-arrow {
  color: #CBD5E1;
  transition: all 0.3s;
}

.history-item:hover .history-arrow {
  color: #14B8A6;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: #FFFFFF;
  border-radius: 20px;
  width: 100%;
  max-width: 520px;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.25);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid #E2E8F0;
}

.modal-title-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.modal-icon {
  font-size: 24px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F1F5F9;
  border-radius: 12px;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  color: #1E293B;
  margin: 0;
}

.modal-close {
  width: 36px;
  height: 36px;
  border: none;
  background: #F1F5F9;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748B;
  transition: all 0.3s;
}

.modal-close:hover {
  background: #EF4444;
  color: #FFFFFF;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

/* 学习卡片通用样式 */
.learn-mode {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.word-card, .poetry-card, .wrong-card, .question-card {
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-radius: 16px;
  padding: 24px;
}

/* 单词卡片 */
.word-main {
  text-align: center;
  margin-bottom: 16px;
}

.word-text {
  font-size: 32px;
  font-weight: 700;
  color: #1E293B;
  margin-bottom: 6px;
}

.word-phonetic {
  font-size: 15px;
  color: #64748B;
  font-family: 'Arial', sans-serif;
}

.word-meaning {
  font-size: 17px;
  color: #1E293B;
  text-align: center;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(20, 184, 166, 0.1);
  border-radius: 10px;
}

.word-example {
  font-size: 14px;
  color: #64748B;
  line-height: 1.6;
  padding: 14px;
  background: #FFFFFF;
  border-radius: 10px;
  border-left: 3px solid #14B8A6;
}

.example-label {
  font-weight: 600;
  color: #14B8A6;
}

/* 古诗卡片 */
.poetry-title {
  font-size: 22px;
  font-weight: 700;
  color: #1E293B;
  text-align: center;
  margin-bottom: 6px;
}

.poetry-author {
  font-size: 14px;
  color: #64748B;
  text-align: center;
  margin-bottom: 20px;
}

.poetry-content {
  text-align: center;
  margin-bottom: 20px;
}

.poetry-line {
  font-size: 17px;
  color: #1E293B;
  margin-bottom: 8px;
  line-height: 1.8;
}

.poetry-translation {
  background: #FFFFFF;
  padding: 16px;
  border-radius: 12px;
  border-left: 3px solid #8B5CF6;
}

.translation-label {
  font-size: 13px;
  font-weight: 600;
  color: #8B5CF6;
  margin-bottom: 8px;
}

.translation-text {
  font-size: 14px;
  color: #64748B;
  line-height: 1.7;
}

/* 错题卡片 */
.wrong-question {
  font-size: 18px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 18px;
  padding-bottom: 16px;
  border-bottom: 1px solid #E2E8F0;
}

.wrong-answer-section {
  margin-bottom: 18px;
}

.wrong-user-answer, .wrong-correct-answer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 10px;
  margin-bottom: 8px;
  font-size: 14px;
}

.wrong-user-answer {
  background: rgba(239, 68, 68, 0.1);
}

.wrong-correct-answer {
  background: rgba(16, 185, 129, 0.1);
}

.answer-label {
  font-weight: 500;
  color: #64748B;
}

.answer-value {
  font-weight: 600;
}

.answer-value.wrong {
  color: #EF4444;
}

.answer-value.correct {
  color: #10B981;
}

.wrong-analysis, .wrong-similar {
  padding: 14px;
  border-radius: 12px;
  margin-bottom: 10px;
}

.wrong-analysis {
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid #F59E0B;
}

.wrong-similar {
  background: rgba(59, 130, 246, 0.1);
  border-left: 3px solid #3B82F6;
}

.analysis-title, .similar-title {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 8px;
}

.analysis-text, .similar-text {
  font-size: 14px;
  color: #64748B;
  line-height: 1.6;
}

/* 题目卡片 */
.question-header {
  margin-bottom: 12px;
}

.question-text {
  font-size: 20px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 20px;
  line-height: 1.5;
}

.question-input-wrapper {
  margin-bottom: 8px;
}

.answer-result {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px;
  border-radius: 12px;
  font-weight: 600;
  font-size: 15px;
  margin-top: 8px;
}

.answer-result.correct {
  background: rgba(16, 185, 129, 0.1);
  color: #10B981;
}

.answer-result.wrong {
  background: rgba(239, 68, 68, 0.1);
  color: #EF4444;
}

/* 打印卡片 */
.print-card {
  background: #FFFFFF;
  border: 2px solid #E2E8F0;
  border-radius: 16px;
  overflow: hidden;
}

.print-preview {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.05) 0%, rgba(45, 212, 191, 0.05) 100%);
  padding: 20px;
  border-bottom: 1px solid #E2E8F0;
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.preview-icon {
  font-size: 24px;
}

.preview-title {
  font-size: 14px;
  font-weight: 600;
  color: #64748B;
}

.preview-content {
  background: #FFFFFF;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  padding: 16px;
}

.preview-title-text {
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 6px;
}

.preview-info {
  font-size: 13px;
  color: #94A3B8;
}

.print-settings {
  padding: 20px;
}

.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #F1F5F9;
}

.setting-row:last-child {
  border-bottom: none;
}

.setting-label {
  font-size: 14px;
  color: #64748B;
}

.print-actions {
  margin-top: 16px;
}

/* 导航按钮 */
.nav-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.progress-indicator {
  font-size: 13px;
  color: #94A3B8;
  min-width: 60px;
  text-align: center;
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

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9) translateY(20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .mode-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .mode-card-lg {
    grid-column: span 2;
  }
  
  .mode-card {
    padding: 12px 10px;
  }
  
  .mode-icon-wrapper {
    width: 40px;
    height: 40px;
  }
  
  .mode-icon {
    font-size: 20px;
  }
  
  .mode-name {
    font-size: 13px;
  }
  
  .mode-desc {
    font-size: 11px;
  }
  
  .modal-content {
    max-height: 90vh;
  }
  
  .modal-header {
    padding: 14px 16px;
  }
  
  .modal-body {
    padding: 16px;
  }
  
  .word-card, .poetry-card, .wrong-card, .question-card {
    padding: 18px;
  }
  
  .word-text {
    font-size: 26px;
  }
  
  .poetry-title {
    font-size: 18px;
  }
  
  .poetry-line {
    font-size: 15px;
  }
}
</style>
