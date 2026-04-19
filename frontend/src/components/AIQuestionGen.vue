<template>
  <div class="ai-learn-page">
    <!-- 小 E 老师欢迎区 -->
    <div class="teacher-welcome-section">
      <div class="teacher-avatar">
        <div class="avatar-glow"></div>
        <span class="avatar-icon">👩‍🏫</span>
      </div>
      <div class="welcome-speech">
        <div class="speech-bubble">
          <p class="speech-text">今天想学什么呢？</p>
        </div>
        <div class="speech-tail"></div>
      </div>
    </div>

    <!-- 学科选择区 -->
    <div class="subject-section">
      <div class="section-header">
        <h2 class="section-title">📚 选择学科</h2>
      </div>

      <div class="subject-cards">
        <!-- 语文 -->
        <div class="subject-card" :class="{ expanded: expandedSubject === 'chinese' }" @click="toggleSubject('chinese')">
          <div class="subject-header">
            <div class="subject-icon-wrapper chinese">
              <span class="subject-icon">🇨🇳</span>
            </div>
            <div class="subject-info">
              <h3 class="subject-name">语文</h3>
              <span class="subject-count">{{ chineseFunctions.length }} 功能</span>
            </div>
            <div class="subject-expand-icon">
              <svg :class="{ rotated: expandedSubject === 'chinese' }" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>

          <Transition name="expand">
            <div v-if="expandedSubject === 'chinese'" class="function-grid">
              <div
                v-for="func in chineseFunctions"
                :key="func.key"
                class="function-item"
                :class="{ 'p0': func.priority === 'P0', 'p1': func.priority === 'P1' }"
                @click.stop="selectFunction('chinese', func)"
              >
                <span class="func-icon">{{ func.icon }}</span>
                <span class="func-name">{{ func.name }}</span>
                <span v-if="func.priority === 'P0'" class="func-badge p0">推荐</span>
              </div>
            </div>
          </Transition>
        </div>

        <!-- 数学 -->
        <div class="subject-card" :class="{ expanded: expandedSubject === 'math' }" @click="toggleSubject('math')">
          <div class="subject-header">
            <div class="subject-icon-wrapper math">
              <span class="subject-icon">🔢</span>
            </div>
            <div class="subject-info">
              <h3 class="subject-name">数学</h3>
              <span class="subject-count">{{ mathFunctions.length }} 功能</span>
            </div>
            <div class="subject-expand-icon">
              <svg :class="{ rotated: expandedSubject === 'math' }" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>

          <Transition name="expand">
            <div v-if="expandedSubject === 'math'" class="function-grid">
              <div
                v-for="func in mathFunctions"
                :key="func.key"
                class="function-item"
                :class="{ 'p0': func.priority === 'P0', 'p1': func.priority === 'P1' }"
                @click.stop="selectFunction('math', func)"
              >
                <span class="func-icon">{{ func.icon }}</span>
                <span class="func-name">{{ func.name }}</span>
                <span v-if="func.priority === 'P0'" class="func-badge p0">推荐</span>
              </div>
            </div>
          </Transition>
        </div>

        <!-- 英语 -->
        <div class="subject-card" :class="{ expanded: expandedSubject === 'english' }" @click="toggleSubject('english')">
          <div class="subject-header">
            <div class="subject-icon-wrapper english">
              <span class="subject-icon">🔤</span>
            </div>
            <div class="subject-info">
              <h3 class="subject-name">英语</h3>
              <span class="subject-count">{{ englishFunctions.length }} 功能</span>
            </div>
            <div class="subject-expand-icon">
              <svg :class="{ rotated: expandedSubject === 'english' }" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </div>
          </div>

          <Transition name="expand">
            <div v-if="expandedSubject === 'english'" class="function-grid">
              <div
                v-for="func in englishFunctions"
                :key="func.key"
                class="function-item"
                :class="{ 'p0': func.priority === 'P0', 'p1': func.priority === 'P1' }"
                @click.stop="selectFunction('english', func)"
              >
                <span class="func-icon">{{ func.icon }}</span>
                <span class="func-name">{{ func.name }}</span>
                <span v-if="func.priority === 'P0'" class="func-badge p0">推荐</span>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>

    <!-- 学习模式快捷入口（保留原有的常用模式） -->
    <div class="quick-modes-section">
      <div class="section-header">
        <h2 class="section-title">⚡ 快捷学习</h2>
      </div>

      <div class="quick-modes-grid">
        <div
          v-for="mode in quickModes"
          :key="mode.key"
          class="quick-mode-card"
          :style="{ background: mode.gradient }"
          @click="selectQuickMode(mode)"
        >
          <span class="quick-mode-icon">{{ mode.icon }}</span>
          <span class="quick-mode-name">{{ mode.name }}</span>
        </div>
      </div>
    </div>

    <!-- 固定底部 AI 按钮 -->
    <div class="ai-fixed-bottom" @click="openDirectAsk">
      <div class="ai-btn-inner">
        <span class="ai-btn-icon">🤖</span>
        <span class="ai-btn-text">AI 按钮 · 直接问</span>
        <svg class="ai-btn-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>
    </div>

    <!-- 功能弹窗 -->
    <Transition name="modal">
      <div v-if="currentFunction" class="modal-overlay" @click.self="closeFunction">
        <div class="modal-content">
          <!-- 弹窗头部 -->
          <div class="modal-header">
            <div class="modal-title-wrapper">
              <span class="modal-icon">{{ currentFunction.icon }}</span>
              <h3 class="modal-title">{{ currentFunction.name }}</h3>
            </div>
            <button class="modal-close" @click="closeFunction">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>

          <!-- 弹窗内容区 -->
          <div class="modal-body">
            <!-- 古诗推荐 -->
            <div v-if="currentFunction.key === 'poetry_recommend'" class="func-content">
              <!-- 页签切换 -->
              <div class="poetry-tabs">
                <div
                  class="poetry-tab"
                  :class="{ active: poetryTab === 'chat' }"
                  @click="poetryTab = 'chat'"
                >
                  💬 对话学习
                </div>
                <div
                  class="poetry-tab"
                  :class="{ active: poetryTab === 'card' }"
                  @click="poetryTab = 'card'"
                >
                  📖 古诗展示
                </div>
              </div>

              <!-- 对话学习页签 -->
              <div v-if="poetryTab === 'chat'" class="poetry-tab-content">
                <PoetryChat
                  student-id="e756948a-b945-412f-b969-80cc326abe64"
                  :grade="1"
                  @poetry-ready="handlePoetryReady"
                />
              </div>

              <!-- 古诗展示页签 -->
              <div v-if="poetryTab === 'card'" class="poetry-tab-content">
                <div v-if="poetryLoading" class="poetry-loading">
                  <span class="loading-icon">📚</span>
                  <span>正在加载古诗...</span>
                </div>
                <template v-else-if="currentPoetry">
                  <PoetryCard
                    :poetry="currentPoetry"
                    student-id="e756948a-b945-412f-b969-80cc326abe64"
                    :show-actions="true"
                    @mastery-change="handleMasteryChange"
                  />
                  <div class="nav-buttons">
                    <n-button @click="prevPoetry" :disabled="currentPoetryIndex === 0">
                      ← 上一首
                    </n-button>
                    <span class="progress-indicator">{{ currentPoetryIndex + 1 }} / {{ poetryList.length || 1 }}</span>
                    <n-button type="success" @click="nextPoetry">
                      下一首 →
                    </n-button>
                  </div>
                </template>
                <div v-else class="poetry-empty">
                  <span class="empty-icon">📖</span>
                  <span>暂无古诗数据</span>
                </div>
              </div>
            </div>

            <!-- 易错字练写 -->
            <div v-if="currentFunction.key === 'wrong_chars'" class="func-content">
              <div class="char-card">
                <div class="char-main">
                  <div class="char-text">{{ currentChar.char }}</div>
                  <div class="char-pinyin">{{ currentChar.pinyin }}</div>
                </div>
                <div class="char-tips">
                  <div class="tip-item">
                    <span class="tip-label">易错笔画：</span>
                    <span class="tip-value">{{ currentChar.wrongStroke }}</span>
                  </div>
                  <div class="tip-item">
                    <span class="tip-label">正确写法：</span>
                    <span class="tip-value">{{ currentChar.correctWay }}</span>
                  </div>
                </div>
                <div class="stroke-animation">
                  <n-button type="primary" size="large" @click="playStrokeAnimation">
                    ▶️ 播放笔顺动画
                  </n-button>
                </div>
              </div>
              <div class="nav-buttons">
                <n-button @click="prevChar" :disabled="currentCharIndex === 0">
                  ← 上一个
                </n-button>
                <span class="progress-indicator">{{ currentCharIndex + 1 }} / {{ charList.length }}</span>
                <n-button type="success" @click="nextChar" :disabled="currentCharIndex === charList.length - 1">
                  下一个 →
                </n-button>
              </div>
            </div>

            <!-- 口算批改 -->
            <div v-if="currentFunction.key === 'oral_math'" class="func-content">
              <div class="math-capture">
                <div class="capture-area" @click="captureMath">
                  <div class="capture-icon">📷</div>
                  <div class="capture-text">点击拍照识别口算题</div>
                </div>
                <div class="capture-tips">
                  <p>支持识别：加减乘除四则运算</p>
                  <p>建议在光线充足的环境下拍摄</p>
                </div>
              </div>
            </div>

            <!-- 错题出题 -->
            <div v-if="currentFunction.key === 'wrong_questions'" class="func-content">
              <div class="wrong-gen-card">
                <div class="wrong-gen-header">
                  <span class="wrong-gen-icon">📝</span>
                  <span class="wrong-gen-title">根据错题生成同类题</span>
                </div>
                <div class="wrong-gen-options">
                  <div class="option-row">
                    <span class="option-label">出题数量</span>
                    <n-select v-model:value="questionCount" :options="countOptions" size="medium" style="width: 100px" />
                  </div>
                  <div class="option-row">
                    <span class="option-label">难度调整</span>
                    <n-select v-model:value="difficultyLevel" :options="difficultyOptions" size="medium" style="width: 100px" />
                  </div>
                </div>
                <n-button type="success" size="large" block @click="generateFromWrong">
                  🎯 生成练习题
                </n-button>
              </div>
            </div>

            <!-- 单词默写 -->
            <div v-if="currentFunction.key === 'dictation'" class="func-content">
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

            <!-- 错题本 -->
            <div v-if="currentFunction.key === 'wrong_book'" class="func-content">
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

            <!-- 默认提示 -->
            <div v-if="!['poetry_recommend', 'wrong_chars', 'oral_math', 'wrong_questions', 'dictation', 'wrong_book'].includes(currentFunction.key)" class="func-content">
              <div class="coming-soon">
                <span class="coming-soon-icon">🚧</span>
                <p class="coming-soon-text">功能开发中，敬请期待...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- AI 直接问弹窗 -->
    <Transition name="modal">
      <div v-if="showDirectAsk" class="modal-overlay" @click.self="closeDirectAsk">
        <div class="modal-content direct-ask-modal">
          <div class="modal-header">
            <div class="modal-title-wrapper">
              <span class="modal-icon">🤖</span>
              <h3 class="modal-title">AI 助手</h3>
            </div>
            <button class="modal-close" @click="closeDirectAsk">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <AIInputBox
              v-model="directAskInput"
              placeholder="问我任何学习问题..."
              :show-camera="true"
              :show-voice="true"
              :quick-phrases="directAskPhrases"
              @submit="handleDirectAsk"
              @voice="handleVoice"
              @camera="handleCamera"
            />
            <div class="chat-history" v-if="chatHistory.length > 0">
              <div v-for="(msg, index) in chatHistory" :key="index" class="chat-message" :class="msg.role">
                <div class="message-content">{{ msg.content }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 错题拍照弹窗 -->
    <WrongPhotoCapture
      v-model:show="showPhotoCapture"
      :subject="photoCaptureSubject"
      @confirm="handlePhotoConfirm"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AIInputBox from './AIInputBox.vue'
import WrongPhotoCapture from './WrongPhotoCapture.vue'
import PoetryCard from './PoetryCard.vue'
import PoetryChat from './PoetryChat.vue'
import { poetryApi } from '../api'

// 展开的学科
const expandedSubject = ref(null)

// 当前选中的功能
const currentFunction = ref(null)

// AI 直接问
const showDirectAsk = ref(false)
const directAskInput = ref('')
const chatHistory = ref([])

// 错题拍照
const showPhotoCapture = ref(false)
const photoCaptureSubject = ref<'chinese' | 'math' | 'english'>('chinese')

// 学科功能定义
const chineseFunctions = ref([
  { key: 'photo_wrong', name: '错题拍照', icon: '📸', desc: '拍照录入语文错题', priority: 'P0', isPhotoCapture: true },
  { key: 'poetry_recommend', name: '古诗推荐', icon: '📖', desc: '根据年级推荐古诗 + 解析', priority: 'P0' },
  { key: 'wrong_chars', name: '易错字练写', icon: '✍️', desc: '常见易错字练习 + 笔顺动画', priority: 'P0' },
  { key: 'reading_train', name: '精读训练', icon: '📚', desc: '阅读理解训练 + AI 讲解', priority: 'P1' },
  { key: 'pinyin', name: '拼音练习', icon: '🔤', desc: '拼音认读 + 发音评测', priority: 'P1' },
  { key: 'idiom_chain', name: '成语接龙', icon: '🎮', desc: '趣味成语学习游戏', priority: 'P2' },
  { key: 'make_sentence', name: '造句练习', icon: '✏️', desc: '词语造句 + AI 点评', priority: 'P1' },
  { key: 'dictation_cn', name: '听写练习', icon: '🎧', desc: '自动报词 + 批改', priority: 'P1' },
  { key: 'reading_comp', name: '阅读理解', icon: '📖', desc: '短文阅读 + 答题', priority: 'P2' },
  { key: 'composition', name: '作文素材', icon: '💡', desc: '好词好句积累', priority: 'P2' },
  { key: 'calligraphy', name: '书法练习', icon: '🖌️', desc: '硬笔书法字帖生成', priority: 'P2' },
  { key: 'oral_expr', name: '口语表达', icon: '🎤', desc: '看图说话训练', priority: 'P2' },
])

const mathFunctions = ref([
  { key: 'photo_wrong', name: '错题拍照', icon: '📸', desc: '拍照录入数学错题', priority: 'P0', isPhotoCapture: true },
  { key: 'oral_math', name: '口算批改', icon: '🧮', desc: '拍照识别口算题 + 批改', priority: 'P0' },
  { key: 'wrong_questions', name: '错题出题', icon: '📝', desc: '根据错题生成同类题', priority: 'P0' },
  { key: 'wrong_book', name: '错题本', icon: '📕', desc: '错题整理 + 举一反三', priority: 'P0' },
  { key: 'word_problem', name: '应用题讲解', icon: '📚', desc: '应用题分步解析', priority: 'P1' },
  { key: 'calc_practice', name: '计算练习', icon: '🔢', desc: '加减乘除专项练习', priority: 'P1' },
  { key: 'geometry', name: '几何认知', icon: '📐', desc: '图形识别 + 面积计算', priority: 'P2' },
  { key: 'logic_train', name: '思维训练', icon: '🧩', desc: '逻辑思维题目', priority: 'P2' },
  { key: 'formula', name: '公式速记', icon: '📋', desc: '数学公式卡片', priority: 'P2' },
])

const englishFunctions = ref([
  { key: 'photo_wrong', name: '错题拍照', icon: '📸', desc: '拍照录入英语错题', priority: 'P0', isPhotoCapture: true },
  { key: 'dictation', name: '单词默写', icon: '✍️', desc: '同步教材单词默写', priority: 'P0' },
  { key: 'essay_correct', name: '作文批改', icon: '📝', desc: '英语作文批改 + 润色', priority: 'P1' },
  { key: 'oral_practice', name: '口语练习', icon: '🎤', desc: '对话练习 + 发音评测', priority: 'P1' },
  { key: 'listening', name: '听力训练', icon: '🎧', desc: '听力材料 + 答题', priority: 'P2' },
  { key: 'grammar', name: '语法练习', icon: '📚', desc: '语法专项练习', priority: 'P2' },
  { key: 'picture_book', name: '绘本阅读', icon: '📖', desc: '英文绘本 + 跟读', priority: 'P2' },
])

// 快捷模式
const quickModes = ref([
  { key: 'daily', name: '每日出题', icon: '📝', gradient: 'linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%)' },
  { key: 'challenge', name: '思维挑战', icon: '🚀', gradient: 'linear-gradient(135deg, #F97316 0%, #FB923C 100%)' },
  { key: 'print', name: '打印试卷', icon: '🖨️', gradient: 'linear-gradient(135deg, #EC4899 0%, #F472B6 100%)' },
  { key: 'poetry', name: '背古诗', icon: '📜', gradient: 'linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%)' },
])

// AI 直接问快捷短语
const directAskPhrases = ref([
  { icon: '📐', text: '帮我解这道题' },
  { icon: '📖', text: '解释这个成语' },
  { icon: '🔤', text: '这个单词怎么读' },
  { icon: '📝', text: '帮我检查作业' },
])

// 数据
const poetryTab = ref<'chat' | 'card'>('chat')  // 古诗页签
const currentPoetryIndex = ref(0)
const poetryList = ref([])
const poetryLoading = ref(false)
const currentPoetry = computed(() => poetryList.value[currentPoetryIndex.value])

// 加载古诗列表
const loadPoetryList = async () => {
  poetryLoading.value = true
  try {
    const res = await poetryApi.list({ grade: 1, textbook: '人教版' })
    if (res.data) {
      poetryList.value = res.data
    }
  } catch (e) {
    console.error('加载古诗失败', e)
  } finally {
    poetryLoading.value = false
  }
}

// 易错字数据
const currentCharIndex = ref(0)
const charList = ref([
  { char: '己', pinyin: 'jǐ', wrongStroke: '开口方向', correctWay: '开口向左，不要写成"已"或"巳"' },
  { char: '候', pinyin: 'hòu', wrongStroke: '中间一竖', correctWay: '中间有一竖，不要漏掉' },
  { char: '真', pinyin: 'zhēn', wrongStroke: '里面三横', correctWay: '里面是三横，不是两横' },
])
const currentChar = computed(() => charList.value[currentCharIndex.value])

// 单词数据
const currentWordIndex = ref(0)
const vocabularyList = ref([
  { word: 'apple', phonetic: 'ˈæpl', meaning: 'n. 苹果', example: 'I eat an apple every day.' },
  { word: 'beautiful', phonetic: 'ˈbjuːtɪfl', meaning: 'adj. 美丽的', example: 'The flower is beautiful.' },
  { word: 'challenge', phonetic: 'ˈtʃælɪndʒ', meaning: 'n. 挑战', example: 'This is a big challenge.' },
])
const currentWord = computed(() => vocabularyList.value[currentWordIndex.value])

// 错题数据
const currentWrongIndex = ref(0)
const wrongList = ref([
  { question: '36 ÷ 4 = ?', userAnswer: '8', correctAnswer: '9', analysis: '除法计算错误。36 ÷ 4 表示把 36 平均分成 4 份，每份是 9。可以用乘法口诀验证：4 × 9 = 36。' },
  { question: '一个长方形的长是 8cm，宽是 5cm，周长是多少？', userAnswer: '13cm', correctAnswer: '26cm', analysis: '周长公式记错了。长方形周长 = (长 + 宽) × 2 = (8 + 5) × 2 = 26cm。' },
])
const currentWrong = computed(() => wrongList.value[currentWrongIndex.value])

// 出题设置
const questionCount = ref(10)
const difficultyLevel = ref('same')
const countOptions = ref([
  { label: '5 题', value: 5 },
  { label: '10 题', value: 10 },
  { label: '15 题', value: 15 },
])
const difficultyOptions = ref([
  { label: '相同难度', value: 'same' },
  { label: '稍简单', value: 'easier' },
  { label: '稍难', value: 'harder' },
])

// 方法
const toggleSubject = (subject) => {
  expandedSubject.value = expandedSubject.value === subject ? null : subject
}

const selectFunction = (subject, func) => {
  // 如果是错题拍照功能，打开拍照弹窗
  if (func.isPhotoCapture) {
    photoCaptureSubject.value = subject
    showPhotoCapture.value = true
    return
  }
  // 如果是古诗推荐，重置页签
  if (func.key === 'poetry_recommend') {
    poetryTab.value = 'chat'
  }
  currentFunction.value = func
}

const closeFunction = () => {
  currentFunction.value = null
}

const openDirectAsk = () => {
  showDirectAsk.value = true
}

const closeDirectAsk = () => {
  showDirectAsk.value = false
}

const selectQuickMode = (mode) => {
  console.log('选择快捷模式:', mode)
  // TODO: 实现快捷模式
}

// 古诗导航
const prevPoetry = () => { if (currentPoetryIndex.value > 0) currentPoetryIndex.value-- }
const nextPoetry = async () => {
  if (currentPoetryIndex.value < poetryList.value.length - 1) {
    currentPoetryIndex.value++
  } else {
    // 加载新的古诗
    poetryLoading.value = true
    try {
      const res = await poetryApi.recommend({ grade: 1, textbook: '人教版' })
      if (res.data) {
        poetryList.value.push(res.data)
        currentPoetryIndex.value = poetryList.value.length - 1
      }
    } catch (e) {
      console.error('加载古诗失败', e)
    } finally {
      poetryLoading.value = false
    }
  }
}

// 易错字导航
const prevChar = () => { if (currentCharIndex.value > 0) currentCharIndex.value-- }
const nextChar = () => { if (currentCharIndex.value < charList.value.length - 1) currentCharIndex.value++ }
const playStrokeAnimation = () => { console.log('播放笔顺动画') }

// 单词导航
const prevWord = () => { if (currentWordIndex.value > 0) currentWordIndex.value-- }
const nextWord = () => { if (currentWordIndex.value < vocabularyList.value.length - 1) currentWordIndex.value++ }

// 错题导航
const prevWrong = () => { if (currentWrongIndex.value > 0) currentWrongIndex.value-- }
const nextWrong = () => { if (currentWrongIndex.value < wrongList.value.length - 1) currentWrongIndex.value++ }

// 口算批改
const captureMath = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.capture = 'environment'
  input.onchange = (e) => {
    const file = e.target?.files?.[0]
    if (file) console.log('选择的图片:', file.name)
  }
  input.click()
}

// 错题出题
const generateFromWrong = () => {
  console.log('生成练习题:', { questionCount: questionCount.value, difficultyLevel: difficultyLevel.value })
}

// AI 直接问
const handleDirectAsk = () => {
  if (!directAskInput.value.trim()) return
  chatHistory.value.push({ role: 'user', content: directAskInput.value })
  // TODO: 调用 AI API
  setTimeout(() => {
    chatHistory.value.push({ role: 'assistant', content: '这是一个模拟回复，AI 功能正在开发中...' })
  }, 500)
  directAskInput.value = ''
}

const handleVoice = () => { console.log('语音输入') }
const handleCamera = () => { console.log('相机输入') }

// 错题拍照确认
const handlePhotoConfirm = (data) => {
  console.log('错题拍照确认:', data)
  // TODO: 处理拍照结果，调用OCR识别等
  // data.subject 是科目类型
  // data.images 是图片数组
}

// 古诗掌握程度变化
const handleMasteryChange = (data) => {
  console.log('古诗掌握程度变化:', data)
}

// 对话式古诗学习 - 诗歌准备就绪
const handlePoetryReady = (poetry) => {
  console.log('古诗准备就绪:', poetry)
  // 更新古诗列表
  poetryList.value = [poetry]
  currentPoetryIndex.value = 0
  // 切换到卡片展示页签
  poetryTab.value = 'card'
}

// 组件挂载时不自动加载古诗，由用户交互触发
onMounted(() => {
  // 可以在这里加载其他初始数据
})
</script>

<style scoped>
.ai-learn-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #F0FDF4 0%, #F8FAFC 100%);
  padding: 20px 16px;
  padding-bottom: 80px;
}

/* 小 E 老师欢迎区 */
.teacher-welcome-section {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 20px;
}

.teacher-avatar {
  position: relative;
  width: 64px;
  height: 64px;
  flex-shrink: 0;
}

.avatar-glow {
  position: absolute;
  inset: -4px;
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.3) 0%, rgba(45, 212, 191, 0.3) 100%);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

.avatar-icon {
  position: relative;
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #14B8A6 0%, #2DD4BF 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  box-shadow: 0 4px 12px rgba(20, 184, 166, 0.3);
}

.welcome-speech {
  flex: 1;
  position: relative;
}

.speech-bubble {
  background: #FFFFFF;
  border-radius: 16px;
  padding: 14px 18px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  position: relative;
}

.speech-text {
  margin: 0;
  font-size: 15px;
  color: #1E293B;
  line-height: 1.5;
}

.speech-tail {
  position: absolute;
  left: -8px;
  top: 16px;
  width: 0;
  height: 0;
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-right: 8px solid #FFFFFF;
}

/* 固定底部 AI 按钮 */
.ai-fixed-bottom {
  position: fixed;
  bottom: 70px;
  left: 16px;
  right: 16px;
  z-index: 99;
  cursor: pointer;
}

.ai-btn-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: linear-gradient(135deg, #14B8A6 0%, #2DD4BF 100%);
  border-radius: 50px;
  padding: 14px 24px;
  box-shadow: 0 4px 20px rgba(20, 184, 166, 0.4);
  transition: all 0.3s;
}

.ai-btn-inner:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 24px rgba(20, 184, 166, 0.5);
}

.ai-btn-inner:active {
  transform: scale(0.98);
}

.ai-btn-icon {
  font-size: 20px;
}

.ai-btn-text {
  font-size: 15px;
  font-weight: 600;
  color: #FFFFFF;
}

.ai-btn-arrow {
  color: rgba(255, 255, 255, 0.9);
}

/* 学科选择区 */
.subject-section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 17px;
  font-weight: 600;
  color: #1E293B;
  margin: 0;
}

.subject-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.subject-card {
  background: #FFFFFF;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s;
  border: 1px solid transparent;
}

.subject-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.subject-card.expanded {
  border-color: rgba(20, 184, 166, 0.3);
}

.subject-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  cursor: pointer;
}

.subject-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.subject-icon-wrapper.chinese {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(248, 113, 113, 0.1) 100%);
}

.subject-icon-wrapper.math {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.1) 100%);
}

.subject-icon-wrapper.english {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(167, 139, 250, 0.1) 100%);
}

.subject-icon {
  font-size: 24px;
}

.subject-info {
  flex: 1;
}

.subject-name {
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
  margin: 0 0 2px 0;
}

.subject-count {
  font-size: 12px;
  color: #94A3B8;
}

.subject-expand-icon svg {
  color: #CBD5E1;
  transition: transform 0.3s;
}

.subject-expand-icon svg.rotated {
  transform: rotate(180deg);
  color: #14B8A6;
}

/* 功能网格 */
.function-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding: 0 16px 16px;
}

.function-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  background: #F8FAFC;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.function-item:hover {
  background: #F1F5F9;
  transform: translateY(-2px);
}

.function-item.p0 {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.05) 0%, rgba(45, 212, 191, 0.05) 100%);
}

.function-item.p0:hover {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.1) 0%, rgba(45, 212, 191, 0.1) 100%);
}

.func-icon {
  font-size: 20px;
}

.func-name {
  font-size: 12px;
  color: #1E293B;
  text-align: center;
  line-height: 1.3;
}

.func-badge {
  position: absolute;
  top: 4px;
  right: 4px;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 8px;
  font-weight: 500;
}

.func-badge.p0 {
  background: #14B8A6;
  color: #FFFFFF;
}

/* 快捷学习 */
.quick-modes-section {
  margin-bottom: 24px;
}

.quick-modes-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.quick-mode-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 10px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.quick-mode-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.quick-mode-icon {
  font-size: 22px;
}

.quick-mode-name {
  font-size: 12px;
  color: #FFFFFF;
  font-weight: 500;
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

/* 功能内容 */
.func-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* 古诗卡片 */
.poetry-card {
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-radius: 16px;
  padding: 24px;
}

.poetry-title {
  font-size: 22px;
  font-weight: 700;
  color: #1E293B;
  text-align: center;
  margin-bottom: 4px;
}

.poetry-title-pinyin {
  font-size: 14px;
  color: #8B5CF6;
  text-align: center;
  margin-bottom: 6px;
  font-family: 'Times New Roman', serif;
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

.poetry-line-wrapper {
  margin-bottom: 12px;
}

.poetry-line-pinyin {
  font-size: 12px;
  color: #8B5CF6;
  margin-bottom: 4px;
  font-family: 'Times New Roman', serif;
  letter-spacing: 1px;
}

.poetry-line {
  font-size: 17px;
  color: #1E293B;
  line-height: 1.6;
  font-weight: 500;
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

/* 古诗加载状态 */
.poetry-loading, .poetry-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #94A3B8;
}

.poetry-loading .loading-icon, .poetry-empty .empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

/* 古诗页签 */
.poetry-tabs {
  display: flex;
  background: #F1F5F9;
  border-radius: 12px;
  padding: 4px;
  margin-bottom: 16px;
}

.poetry-tab {
  flex: 1;
  text-align: center;
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  color: #64748B;
  cursor: pointer;
  transition: all 0.3s;
}

.poetry-tab.active {
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  color: #FFFFFF;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
}

.poetry-tab:hover:not(.active) {
  background: #E2E8F0;
}

.poetry-tab-content {
  min-height: 400px;
}

/* 易错字卡片 */
.char-card {
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-radius: 16px;
  padding: 24px;
}

.char-main {
  text-align: center;
  margin-bottom: 20px;
}

.char-text {
  font-size: 48px;
  font-weight: 700;
  color: #1E293B;
}

.char-pinyin {
  font-size: 18px;
  color: #64748B;
  margin-top: 4px;
}

.char-tips {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 16px;
}

.tip-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 10px;
}

.tip-item:last-child {
  margin-bottom: 0;
}

.tip-label {
  font-size: 13px;
  color: #64748B;
  flex-shrink: 0;
}

.tip-value {
  font-size: 14px;
  color: #1E293B;
}

.stroke-animation {
  display: flex;
  justify-content: center;
}

/* 口算批改 */
.math-capture {
  text-align: center;
}

.capture-area {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.1) 100%);
  border: 2px dashed #3B82F6;
  border-radius: 16px;
  padding: 40px;
  cursor: pointer;
  transition: all 0.3s;
}

.capture-area:hover {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(96, 165, 250, 0.15) 100%);
}

.capture-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.capture-text {
  font-size: 15px;
  color: #3B82F6;
  font-weight: 500;
}

.capture-tips {
  margin-top: 16px;
}

.capture-tips p {
  font-size: 13px;
  color: #94A3B8;
  margin: 4px 0;
}

/* 错题出题 */
.wrong-gen-card {
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-radius: 16px;
  padding: 20px;
}

.wrong-gen-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.wrong-gen-icon {
  font-size: 24px;
}

.wrong-gen-title {
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
}

.wrong-gen-options {
  margin-bottom: 20px;
}

.option-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #E2E8F0;
}

.option-row:last-child {
  border-bottom: none;
}

.option-label {
  font-size: 14px;
  color: #64748B;
}

/* 单词卡片 */
.word-card {
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-radius: 16px;
  padding: 24px;
}

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
}

.word-meaning {
  font-size: 17px;
  color: #1E293B;
  text-align: center;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(139, 92, 246, 0.1);
  border-radius: 10px;
}

.word-example {
  font-size: 14px;
  color: #64748B;
  line-height: 1.6;
  padding: 14px;
  background: #FFFFFF;
  border-radius: 10px;
  border-left: 3px solid #8B5CF6;
}

/* 错题卡片 */
.wrong-card {
  background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
  border-radius: 16px;
  padding: 24px;
}

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

.wrong-analysis {
  padding: 14px;
  border-radius: 12px;
  background: rgba(245, 158, 11, 0.1);
  border-left: 3px solid #F59E0B;
}

.analysis-title {
  font-size: 13px;
  font-weight: 600;
  color: #F59E0B;
  margin-bottom: 8px;
}

.analysis-text {
  font-size: 14px;
  color: #64748B;
  line-height: 1.6;
}

/* 开发中提示 */
.coming-soon {
  text-align: center;
  padding: 40px;
}

.coming-soon-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}

.coming-soon-text {
  font-size: 15px;
  color: #94A3B8;
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

/* AI 直接问弹窗 */
.direct-ask-modal {
  max-width: 480px;
}

.chat-history {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-message {
  max-width: 85%;
  padding: 12px 16px;
  border-radius: 16px;
}

.chat-message.user {
  align-self: flex-end;
  background: #14B8A6;
  color: #FFFFFF;
}

.chat-message.assistant {
  align-self: flex-start;
  background: #F1F5F9;
  color: #1E293B;
}

.message-content {
  font-size: 14px;
  line-height: 1.5;
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

.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.expand-enter-to,
.expand-leave-from {
  max-height: 500px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .function-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .quick-modes-grid {
    grid-template-columns: repeat(4, 1fr);
  }

  .quick-mode-card {
    padding: 12px 8px;
  }

  .quick-mode-icon {
    font-size: 18px;
  }

  .quick-mode-name {
    font-size: 11px;
  }
}
</style>