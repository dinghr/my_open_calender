<template>
  <!-- 打印预览弹窗 -->
  <n-modal v-model:show="showModal" preset="card" title="📄 打印预览" style="width: 600px; max-width: 95vw;">
    <div class="print-preview-content">
      <!-- 语文部分 -->
      <div v-if="content.chinese.length > 0" class="print-section">
        <h3 style="color: #667eea; border-bottom: 2px solid #667eea; padding-bottom: 8px;">
          📖 语文每日一练
        </h3>

        <!-- 古诗 -->
        <div v-if="poetryContent" class="print-block">
          <h4>【古诗背诵】</h4>
          <div class="poetry-box">
            <div class="poetry-title">{{ poetryContent.title }}</div>
            <div class="poetry-author">{{ poetryContent.author }}</div>
            <div class="poetry-content" v-html="poetryContent.content"></div>
          </div>
          <p class="print-hint">请在下方空白处默写：</p>
          <div class="writing-lines">
            <div class="line" v-for="i in 4" :key="i"></div>
          </div>
        </div>

        <!-- 易错字 -->
        <div v-if="characters.length > 0" class="print-block">
          <h4>【易错字练写】</h4>
          <n-space>
            <div v-for="char in characters" :key="char" class="character-box">
              <div class="char-display">{{ char }}</div>
              <div class="char-grid">
                <div class="grid-cell" v-for="i in 5" :key="i"></div>
              </div>
            </div>
          </n-space>
        </div>

        <!-- 好句精读 -->
        <div v-if="content.chinese.includes('好句精读')" class="print-block">
          <h4>【好句精读】</h4>
          <div class="sentence-box">
            <p>“床前明月光，疑是地上霜。”</p>
            <p class="sentence-hint">—— 李白《静夜思》</p>
          </div>
          <p class="print-hint">这句话的意思是：_______________________</p>
          <div class="writing-lines">
            <div class="line"></div>
          </div>
        </div>
      </div>

      <!-- 数学部分 -->
      <div v-if="content.math.length > 0" class="print-section" style="margin-top: 20px;">
        <h3 style="color: #e91e63; border-bottom: 2px solid #e91e63; padding-bottom: 8px;">
          🔢 数学每日一练
        </h3>

        <!-- 口算练习 -->
        <div v-if="oralQuestions.length > 0" class="print-block">
          <h4>【口算练习】</h4>
          <n-grid :cols="2" :x-gap="16">
            <n-gi v-for="(q, idx) in oralQuestions" :key="idx">
              <div class="question-item">
                <span class="q-num">{{ idx + 1 }}.</span>
                <span class="q-content">{{ q.question }} =</span>
                <span class="q-answer">________</span>
              </div>
            </n-gi>
          </n-grid>
        </div>

        <!-- 应用题 -->
        <div v-if="content.math.includes('应用题练习')" class="print-block">
          <h4>【应用题】</h4>
          <div class="app-question">
            <p><strong>题目：</strong>小明有 15 个苹果，给了小红 7 个，又买了 8 个。请问小明现在有多少个苹果？</p>
            <div class="answer-area">
              <p>答：_________________________________________</p>
              <div class="writing-lines">
                <div class="line" v-for="i in 3" :key="i"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 页脚信息 -->
      <div class="print-footer">
        <n-space justify="space-between">
          <n-text depth="3">姓名：__________</n-text>
          <n-text depth="3">日期：{{ todayDate }}</n-text>
          <n-text depth="3">用时：__________分钟</n-text>
        </n-space>
        <div class="parent-sign">
          <n-text depth="3">家长签字：__________</n-text>
        </div>
      </div>
    </div>

    <template #footer>
      <n-space justify="end">
        <n-button @click="showModal = false">关闭</n-button>
        <n-button type="primary" @click="handlePrint">
          🖨️ 打印
        </n-button>
      </n-space>
    </template>
  </n-modal>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  NModal, NSpace, NButton, NText, NGrid, NGi
} from 'naive-ui'

const props = defineProps<{
  show: boolean
  content: {
    chinese: string[]
    math: string[]
  }
  poetry?: { title: string; author: string; content: string } | null
  characters?: string[]
  oralType?: string
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
}>()

const showModal = computed({
  get: () => props.show,
  set: (val) => emit('update:show', val)
})

const todayDate = computed(() => {
  const now = new Date()
  return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`
})

const poetryContent = computed(() => {
  if (props.poetry) return props.poetry
  return {
    title: '静夜思',
    author: '【唐】李白',
    content: '床前明月光，疑是地上霜。<br>举头望明月，低头思故乡。'
  }
})

const characters = computed(() => props.characters || ['疑', '举', '床'])

const oralQuestions = computed(() => {
  const type = props.oralType || 'two-digit-add'
  const questions: { question: string }[] = []

  // 根据类型生成题目
  for (let i = 0; i < 10; i++) {
    const a = Math.floor(Math.random() * 90) + 10
    const b = Math.floor(Math.random() * 90) + 10

    if (type === 'two-digit-add') {
      questions.push({ question: `${a} + ${b}` })
    } else if (type === 'two-digit-sub') {
      questions.push({ question: `${Math.max(a, b)} - ${Math.min(a, b)}` })
    } else if (type === 'two-digit-mul') {
      const small = Math.floor(Math.random() * 9) + 2
      questions.push({ question: `${a} × ${small}` })
    } else {
      // mixed
      const ops = ['+', '-', '×']
      const op = ops[Math.floor(Math.random() * 3)]
      questions.push({ question: `${a} ${op} ${Math.min(b, a)}` })
    }
  }

  return questions
})

const handlePrint = () => {
  window.print()
}
</script>

<style scoped>
.print-preview-content {
  padding: 20px;
  background: white;
}

.print-section {
  margin-bottom: 24px;
}

.print-block {
  margin: 16px 0;
  padding: 12px;
  background: #fafafa;
  border-radius: 8px;
}

.print-block h4 {
  margin: 0 0 12px 0;
  color: #333;
}

.poetry-box {
  text-align: center;
  padding: 16px;
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  border-radius: 8px;
}

.poetry-title {
  font-size: 18px;
  font-weight: bold;
  color: #3730a3;
}

.poetry-author {
  font-size: 12px;
  color: #6366f1;
  margin: 4px 0 12px;
}

.poetry-content {
  font-size: 16px;
  line-height: 2;
  color: #1e1b4b;
}

.print-hint {
  font-size: 12px;
  color: #666;
  margin: 12px 0 8px;
}

.writing-lines {
  margin-top: 8px;
}

.writing-lines .line {
  height: 32px;
  border-bottom: 1px dashed #ccc;
  margin-bottom: 4px;
}

.character-box {
  text-align: center;
  padding: 8px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.char-display {
  font-size: 24px;
  font-weight: bold;
  color: #dc2626;
  margin-bottom: 8px;
}

.char-grid {
  display: grid;
  grid-template-columns: repeat(5, 24px);
  gap: 2px;
  justify-content: center;
}

.char-grid .grid-cell {
  width: 24px;
  height: 24px;
  border: 1px solid #d1d5db;
}

.sentence-box {
  padding: 12px;
  background: #fef3c7;
  border-radius: 8px;
  border-left: 4px solid #f59e0b;
}

.sentence-box p {
  margin: 0;
  font-size: 14px;
}

.sentence-hint {
  font-size: 12px !important;
  color: #92400e;
  margin-top: 4px !important;
}

.question-item {
  display: flex;
  align-items: center;
  padding: 8px;
  background: white;
  border-radius: 4px;
  margin-bottom: 8px;
}

.q-num {
  font-weight: bold;
  margin-right: 8px;
  color: #e91e63;
}

.q-content {
  font-size: 16px;
}

.q-answer {
  margin-left: 8px;
  border-bottom: 1px solid #333;
  min-width: 40px;
}

.app-question {
  padding: 12px;
  background: white;
  border-radius: 8px;
}

.answer-area {
  margin-top: 12px;
}

.print-footer {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 2px dashed #e5e7eb;
}

.parent-sign {
  margin-top: 12px;
  text-align: right;
}

/* 打印样式 */
@media print {
  body * {
    visibility: hidden;
  }

  .print-preview-content,
  .print-preview-content * {
    visibility: visible;
  }

  .print-preview-content {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    padding: 20px;
  }
}
</style>