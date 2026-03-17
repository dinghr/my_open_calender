<template>
  <n-card title="📚 每日一练配置" size="medium" class="config-card">
    <template #header-extra>
      <n-button type="primary" size="small" class="generate-btn" @click="generatePractice">
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M23 4v6h-6M1 20v-6h6M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
          </svg>
        </template>
        生成今日推荐
      </n-button>
    </template>

    <!-- 学科卡片选择 -->
    <div class="subject-cards">
      <!-- 语文卡片 -->
      <div
        class="subject-card chinese"
        :class="{ selected: selectedSubjects.chinese }"
        @click="toggleSubject('chinese')"
      >
        <div class="card-header">
          <div class="card-icon chinese-icon">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              <path d="M8 7h8M8 11h6" />
            </svg>
          </div>
          <div class="card-title">
            <span class="title-text">语文</span>
            <span class="title-sub">Chinese</span>
          </div>
          <div class="card-check" :class="{ checked: selectedSubjects.chinese }">
            <svg v-if="selectedSubjects.chinese" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
        </div>

        <div class="card-content">
          <div class="content-item">
            <span class="item-label">古诗背诵</span>
            <span class="item-value">{{ config.chinese.poetry.current?.title || '《静夜思》' }}</span>
          </div>
          <div class="content-item">
            <span class="item-label">生字练习</span>
            <span class="item-value">{{ config.chinese.characters.list.join('、') || '暂无' }}</span>
          </div>
        </div>

        <div class="card-footer">
          <span class="footer-tag">权重: {{ config.chinese.poetry.weight + config.chinese.characters.weight + config.chinese.reading.weight }}</span>
        </div>
      </div>

      <!-- 数学卡片 -->
      <div
        class="subject-card math"
        :class="{ selected: selectedSubjects.math }"
        @click="toggleSubject('math')"
      >
        <div class="card-header">
          <div class="card-icon math-icon">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="1" x2="12" y2="23" />
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
            </svg>
          </div>
          <div class="card-title">
            <span class="title-text">数学</span>
            <span class="title-sub">Math</span>
          </div>
          <div class="card-check" :class="{ checked: selectedSubjects.math }">
            <svg v-if="selectedSubjects.math" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
        </div>

        <div class="card-content">
          <div class="content-item">
            <span class="item-label">口算练习</span>
            <span class="item-value">{{ getOralTypeLabel() }}</span>
          </div>
          <div class="content-item">
            <span class="item-label">应用题</span>
            <span class="item-value">{{ config.math.application.enabled ? '已开启' : '未开启' }}</span>
          </div>
        </div>

        <div class="card-footer">
          <span class="footer-tag">权重: {{ config.math.oral.weight + config.math.application.weight }}</span>
        </div>
      </div>
    </div>

    <!-- 详细配置区域 -->
    <n-collapse-transition :show="showDetail">
      <!-- 语文详细配置 -->
      <div v-if="selectedSubjects.chinese" class="detail-section chinese-section">
        <div class="section-header">
          <span class="section-title">📖 语文详细配置</span>
        </div>

        <div class="config-grid">
          <!-- 古诗推荐 -->
          <div class="config-item">
            <div class="config-row">
              <n-checkbox v-model:checked="config.chinese.poetry.enabled" />
              <span class="config-label">古诗推荐</span>
              <n-tag size="small" type="info" class="weight-tag">权重: {{ config.chinese.poetry.weight }}</n-tag>
              <n-slider v-model:value="config.chinese.poetry.weight" :min="1" :max="10" :step="1" class="weight-slider" />
            </div>
            <div v-if="config.chinese.poetry.enabled" class="config-preview">
              <div class="preview-card">
                <div class="preview-title">{{ config.chinese.poetry.current?.title || '《静夜思》' }}</div>
                <div class="preview-author">{{ config.chinese.poetry.current?.author || '李白' }}</div>
                <n-button size="tiny" type="primary" ghost @click="changePoetry">换一首</n-button>
              </div>
            </div>
          </div>

          <!-- 易错字练写 -->
          <div class="config-item">
            <div class="config-row">
              <n-checkbox v-model:checked="config.chinese.characters.enabled" />
              <span class="config-label">易错字练写</span>
              <n-tag size="small" type="warning" class="weight-tag">权重: {{ config.chinese.characters.weight }}</n-tag>
              <n-slider v-model:value="config.chinese.characters.weight" :min="1" :max="10" :step="1" class="weight-slider" />
            </div>
            <div v-if="config.chinese.characters.enabled" class="config-preview">
              <div class="character-tags">
                <n-tag v-for="char in config.chinese.characters.list" :key="char" size="small" closable type="info" @close="removeCharacter(char)">
                  {{ char }}
                </n-tag>
                <n-input v-model:value="newCharacter" size="tiny" placeholder="添加生字" class="add-input" @keyup.enter="addCharacter" />
              </div>
            </div>
          </div>

          <!-- 好句精读 -->
          <div class="config-item">
            <div class="config-row">
              <n-checkbox v-model:checked="config.chinese.reading.enabled" />
              <span class="config-label">好句精读</span>
              <n-tag size="small" type="success" class="weight-tag">权重: {{ config.chinese.reading.weight }}</n-tag>
              <n-slider v-model:value="config.chinese.reading.weight" :min="1" :max="10" :step="1" class="weight-slider" />
            </div>
          </div>
        </div>
      </div>

      <!-- 数学详细配置 -->
      <div v-if="selectedSubjects.math" class="detail-section math-section">
        <div class="section-header">
          <span class="section-title">🔢 数学详细配置</span>
        </div>

        <div class="config-grid">
          <!-- 口算练习 -->
          <div class="config-item">
            <div class="config-row">
              <n-checkbox v-model:checked="config.math.oral.enabled" />
              <span class="config-label">口算练习</span>
              <n-tag size="small" type="info" class="weight-tag">权重: {{ config.math.oral.weight }}</n-tag>
              <n-slider v-model:value="config.math.oral.weight" :min="1" :max="10" :step="1" class="weight-slider" />
            </div>
            <div v-if="config.math.oral.enabled" class="config-preview">
              <n-select v-model:value="config.math.oral.type" :options="oralOptions" size="small" class="type-select" />
            </div>
          </div>

          <!-- 应用题 -->
          <div class="config-item">
            <div class="config-row">
              <n-checkbox v-model:checked="config.math.application.enabled" />
              <span class="config-label">应用题</span>
              <n-tag size="small" type="warning" class="weight-tag">权重: {{ config.math.application.weight }}</n-tag>
              <n-slider v-model:value="config.math.application.weight" :min="1" :max="10" :step="1" class="weight-slider" />
            </div>
          </div>
        </div>
      </div>
    </n-collapse-transition>

    <!-- 展开/收起按钮 -->
    <n-button
      text
      type="primary"
      class="toggle-detail-btn"
      @click="showDetail = !showDetail"
    >
      {{ showDetail ? '收起详细配置' : '展开详细配置' }}
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" :style="{ transform: showDetail ? 'rotate(180deg)' : '' }">
        <polyline points="6 9 12 15 18 9" />
      </svg>
    </n-button>

    <!-- 今日推荐预览 -->
    <div class="preview-section">
      <div class="section-header">
        <span class="section-title">📋 今日推荐预览</span>
      </div>

      <div class="preview-content">
        <div v-if="generatedContent.chinese.length > 0" class="preview-group chinese">
          <span class="group-label">语文</span>
          <div class="tag-list">
            <span v-for="item in generatedContent.chinese" :key="item" class="preview-tag chinese-tag">{{ item }}</span>
          </div>
        </div>
        <div v-if="generatedContent.math.length > 0" class="preview-group math">
          <span class="group-label">数学</span>
          <div class="tag-list">
            <span v-for="item in generatedContent.math" :key="item" class="preview-tag math-tag">{{ item }}</span>
          </div>
        </div>
        <n-empty v-if="generatedContent.chinese.length === 0 && generatedContent.math.length === 0" description="点击生成今日推荐按钮生成内容" size="small" />
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <n-button class="action-btn secondary" @click="resetConfig">
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
            <path d="M3 3v5h5" />
          </svg>
        </template>
        重置
      </n-button>
      <n-button type="primary" class="action-btn primary" @click="saveConfig">
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
            <polyline points="17 21 17 13 7 13 7 21" />
            <polyline points="7 3 7 8 15 8" />
          </svg>
        </template>
        保存配置
      </n-button>
      <n-button type="success" class="action-btn success" @click="printPreview">
        <template #icon>
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 6 2 18 2 18 9" />
            <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2" />
            <rect x="6" y="14" width="12" height="8" />
          </svg>
        </template>
        打印预览
      </n-button>
    </div>

    <!-- 打印预览弹窗 -->
    <PrintPreview
      v-model:show="showPrintPreview"
      :content="generatedContent"
      :poetry="poetryContent"
      :characters="config.chinese.characters.list"
      :oral-type="config.math.oral.type"
    />
  </n-card>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import {
  NCard, NButton, NCheckbox, NTag, NSlider, NSelect, NInput, NEmpty, NCollapseTransition, useMessage
} from 'naive-ui'
import PrintPreview from './PrintPreview.vue'

const message = useMessage()

const showPrintPreview = ref(false)
const showDetail = ref(false)

const selectedSubjects = reactive({
  chinese: true,
  math: true
})

const config = reactive({
  chinese: {
    poetry: { enabled: true, weight: 5, current: { title: '《静夜思》', author: '李白' } as { title: string; author: string } | null },
    characters: { enabled: true, weight: 4, list: ['疑', '举', '床'] as string[] },
    reading: { enabled: false, weight: 3 }
  },
  math: {
    oral: { enabled: true, weight: 5, type: 'two-digit-add' as string },
    application: { enabled: true, weight: 4 }
  }
})

const generatedContent = reactive({
  chinese: [] as string[],
  math: [] as string[]
})

const newCharacter = ref('')

const oralOptions = [
  { label: '两位数加法', value: 'two-digit-add' },
  { label: '两位数减法', value: 'two-digit-sub' },
  { label: '两位数乘法', value: 'two-digit-mul' },
  { label: '混合运算', value: 'mixed' }
]

const poetryList = [
  { title: '《静夜思》', author: '李白', content: '床前明月光，疑是地上霜。<br>举头望明月，低头思故乡。' },
  { title: '《春晓》', author: '孟浩然', content: '春眠不觉晓，处处闻啼鸟。<br>夜来风雨声，花落知多少。' },
  { title: '《登鹳雀楼》', author: '王之涣', content: '白日依山尽，黄河入海流。<br>欲穷千里目，更上一层楼。' },
  { title: '《咏鹅》', author: '骆宾王', content: '鹅鹅鹅，曲项向天歌。<br>白毛浮绿水，红掌拨清波。' },
  { title: '《悯农》', author: '李绅', content: '锄禾日当午，汗滴禾下土。<br>谁知盘中餐，粒粒皆辛苦。' }
]

const poetryContent = computed(() => {
  const current = config.chinese.poetry.current
  if (!current) return null
  const found = poetryList.find(p => p.title === current.title)
  return found || poetryList[0]
})

const getOralTypeLabel = () => {
  return oralOptions.find(o => o.value === config.math.oral.type)?.label || '两位数加法'
}

const toggleSubject = (subject: 'chinese' | 'math') => {
  selectedSubjects[subject] = !selectedSubjects[subject]
}

const changePoetry = () => {
  const currentIndex = poetryList.findIndex(p => p.title === config.chinese.poetry.current?.title)
  const nextIndex = (currentIndex + 1) % poetryList.length
  const nextPoetry = poetryList[nextIndex]
  if (nextPoetry) {
    config.chinese.poetry.current = nextPoetry
    message.info(`已切换到：${nextPoetry.title}`)
  }
}

const addCharacter = () => {
  if (newCharacter.value && !config.chinese.characters.list.includes(newCharacter.value)) {
    config.chinese.characters.list.push(newCharacter.value)
    newCharacter.value = ''
  }
}

const removeCharacter = (char: string) => {
  const index = config.chinese.characters.list.indexOf(char)
  if (index > -1) {
    config.chinese.characters.list.splice(index, 1)
  }
}

const generatePractice = () => {
  generatedContent.chinese = []
  generatedContent.math = []

  if (selectedSubjects.chinese) {
    if (config.chinese.poetry.enabled) {
      generatedContent.chinese.push(config.chinese.poetry.current?.title || '古诗背诵')
    }
    if (config.chinese.characters.enabled) {
      generatedContent.chinese.push(`易错字：${config.chinese.characters.list.join('、')}`)
    }
    if (config.chinese.reading.enabled) {
      generatedContent.chinese.push('好句精读')
    }
  }

  if (selectedSubjects.math) {
    if (config.math.oral.enabled) {
      const typeLabel = oralOptions.find(o => o.value === config.math.oral.type)?.label || '口算练习'
      generatedContent.math.push(typeLabel)
    }
    if (config.math.application.enabled) {
      generatedContent.math.push('应用题练习')
    }
  }

  message.success('已生成今日推荐')
}

const resetConfig = () => {
  config.chinese.poetry.weight = 5
  config.chinese.characters.weight = 4
  config.chinese.reading.weight = 3
  config.math.oral.weight = 5
  config.math.application.weight = 4
  message.info('已重置配置')
}

const saveConfig = () => {
  message.success('配置已保存')
}

const printPreview = () => {
  if (generatedContent.chinese.length === 0 && generatedContent.math.length === 0) {
    message.warning('请先生成今日推荐')
    return
  }
  showPrintPreview.value = true
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.config-card {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --accent: #F97316;
  --accent-light: #FB923C;
  --bg-light: #F8FAFC;
  --bg-card: #FFFFFF;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --radius-sm: 12px;
  --radius-md: 16px;
  --radius-lg: 20px;

  margin-bottom: 16px;
}

.generate-btn {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border: none;
  font-weight: 500;
}

.generate-btn:hover {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
}

/* 学科卡片 */
.subject-cards {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 16px;
}

.subject-card {
  background: var(--bg-card);
  border: 2px solid #E2E8F0;
  border-radius: var(--radius-md);
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.subject-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: #E2E8F0;
  transition: all 0.3s;
}

.subject-card.chinese::before {
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
  opacity: 0.3;
}

.subject-card.math::before {
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent-light) 100%);
  opacity: 0.3;
}

.subject-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

.subject-card.selected.chinese {
  border-color: var(--primary);
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.05) 0%, rgba(45, 212, 191, 0.05) 100%);
}

.subject-card.selected.chinese::before {
  opacity: 1;
}

.subject-card.selected.math {
  border-color: var(--accent);
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.05) 0%, rgba(251, 146, 60, 0.05) 100%);
}

.subject-card.selected.math::before {
  opacity: 1;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.card-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon.chinese-icon {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
}

.card-icon.math-icon {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%);
  color: white;
}

.card-title {
  flex: 1;
}

.title-text {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.title-sub {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
}

.card-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #E2E8F0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.card-check.checked {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border-color: var(--primary);
  color: white;
}

.card-content {
  margin-bottom: 12px;
}

.content-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px dashed #E2E8F0;
}

.content-item:last-child {
  border-bottom: none;
}

.item-label {
  font-size: 12px;
  color: var(--text-secondary);
}

.item-value {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-primary);
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-footer {
  padding-top: 8px;
  border-top: 1px solid #E2E8F0;
}

.footer-tag {
  font-size: 11px;
  color: var(--text-muted);
  background: var(--bg-light);
  padding: 4px 8px;
  border-radius: 8px;
}

/* 详细配置区域 */
.detail-section {
  margin-top: 16px;
  padding: 16px;
  border-radius: var(--radius-md);
  margin-bottom: 16px;
}

.chinese-section {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.04) 0%, rgba(45, 212, 191, 0.04) 100%);
  border: 1px solid rgba(20, 184, 166, 0.15);
}

.math-section {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.04) 0%, rgba(251, 146, 60, 0.04) 100%);
  border: 1px solid rgba(249, 115, 22, 0.15);
}

.section-header {
  margin-bottom: 12px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.config-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.config-item {
  background: white;
  padding: 12px;
  border-radius: var(--radius-sm);
}

.config-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.config-label {
  font-weight: 500;
  min-width: 80px;
  font-size: 13px;
  color: var(--text-primary);
}

.weight-tag {
  font-size: 10px;
}

.weight-slider {
  width: 80px;
  flex-shrink: 0;
}

.config-preview {
  margin-top: 10px;
  padding-left: 28px;
}

.preview-card {
  background: var(--bg-light);
  padding: 10px;
  border-radius: 8px;
}

.preview-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.preview-author {
  font-size: 11px;
  color: var(--text-secondary);
  margin-bottom: 8px;
}

.character-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.add-input {
  width: 60px;
}

.type-select {
  width: 150px;
}

/* 展开/收起按钮 */
.toggle-detail-btn {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.toggle-detail-btn svg {
  transition: transform 0.3s;
}

/* 预览区域 */
.preview-section {
  background: var(--bg-light);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 16px;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.preview-group {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.group-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  min-width: 40px;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preview-tag {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
}

.chinese-tag {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.15) 0%, rgba(45, 212, 191, 0.15) 100%);
  color: var(--primary-dark);
}

.math-tag {
  background: linear-gradient(135deg, rgba(249, 115, 22, 0.15) 0%, rgba(251, 146, 60, 0.15) 100%);
  color: #C2410C;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 100px;
  height: 40px;
  font-weight: 500;
}

.action-btn.primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  border: none;
}

.action-btn.primary:hover {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
}

.action-btn.secondary {
  border: 1px solid #E2E8F0;
}

.action-btn.secondary:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.action-btn.success {
  background: linear-gradient(135deg, #10B981 0%, #34D399 100%);
  border: none;
}

.action-btn.success:hover {
  background: linear-gradient(135deg, #059669 0%, #10B981 100%);
}
</style>