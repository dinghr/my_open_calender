<template>
  <div class="dino-area" :class="[`stage-${evolutionStage}`, { 'grow-animation': isGrowing }]" @click="handleDinoClick">
    <!-- 动态背景装饰 -->
    <div class="bg-decorations">
      <span v-for="i in 12" :key="i" class="bg-star" :style="getBgStarStyle(i)">✦</span>
    </div>

    <!-- 进化光环（高等级专属） -->
    <div v-if="level >= 21" class="evolution-aura" :class="`aura-${evolutionStage}`"></div>

    <!-- 等级徽章 -->
    <div class="level-badge" :class="`badge-${evolutionStage}`">
      <span class="level-crown" v-if="level >= 50">👑</span>
      <span class="level-wings" v-else-if="level >= 21">✨</span>
      <span class="level-text">Lv.{{ level }}</span>
      <span class="stage-name">{{ stageNames[evolutionStage] }}</span>
    </div>

    <!-- 成就徽章环绕 -->
    <div class="achievements-ring" v-if="props.achievements && props.achievements.length > 0">
      <span
        v-for="(achievement, index) in visibleAchievements"
        :key="achievement.id"
        class="achievement-badge"
        :style="getAchievementStyle(index)"
        :title="achievement.name"
      >
        {{ achievement.icon }}
      </span>
    </div>

    <!-- 恐龙容器 -->
    <div class="dino-container" :class="{ 'dino-jump': isGrowing, [currentAction]: true }">
      <!-- 恐龙 SVG -->
      <svg
        class="spinosaurus"
        :class="[`color-${evolutionStage}`]"
        viewBox="0 0 200 120"
        :style="{ transform: `scale(${dinoScale})` }"
      >
        <!-- 身体主体 -->
        <ellipse cx="100" cy="75" rx="55" ry="30" :fill="bodyColor" class="dino-body"/>

        <!-- 尾巴 -->
        <g class="dino-tail" :class="{ 'tail-wiggle': isWiggling }">
          <path d="M155 75 Q180 70 195 80 Q180 85 155 80 Z" :fill="tailColor"/>
        </g>

        <!-- 背棘 - 根据阶段变化 -->
        <g class="spine-glow" :class="{ 'spine-burst': isGrowing, [`spine-${evolutionStage}`]: true }">
          <polygon v-for="(spine, idx) in spines" :key="idx" :points="spine.points" :fill="spine.color" class="spine"/>
        </g>

        <!-- 翅膀（远古龙及以上） -->
        <g v-if="level >= 21" class="dino-wings" :class="{ 'wings-flap': isFlying }">
          <ellipse cx="45" cy="70" rx="25" ry="12" :fill="wingColor" opacity="0.6"/>
          <ellipse cx="155" cy="70" rx="25" ry="12" :fill="wingColor" opacity="0.6"/>
        </g>

        <!-- 腿 -->
        <rect x="70" y="95" width="12" height="20" rx="4" :fill="legColor"/>
        <rect x="115" y="95" width="12" height="20" rx="4" :fill="legColor"/>
        <ellipse cx="76" cy="118" rx="8" ry="4" :fill="footColor"/>
        <ellipse cx="121" cy="118" rx="8" ry="4" :fill="footColor"/>

        <!-- 手臂 -->
        <ellipse cx="55" cy="80" rx="15" ry="8" :fill="armColor"/>
        <ellipse cx="145" cy="80" rx="15" ry="8" :fill="armColor"/>

        <!-- 头部 -->
        <ellipse cx="35" cy="60" rx="25" ry="18" :fill="headColor"/>
        <ellipse cx="35" cy="65" rx="20" ry="10" :fill="headDarkColor"/>

        <!-- 眼睛 - 根据阶段变化 -->
        <g class="dino-eye" :class="`eye-${evolutionStage}`">
          <circle cx="28" cy="55" r="5" fill="#fff"/>
          <circle cx="29" cy="55" :r="eyePupilSize" :fill="eyeColor"/>
          <circle cx="30" cy="54" r="1" fill="#fff"/>
          <!-- 高等级发光眼睛 -->
          <circle v-if="level >= 21" cx="28" cy="55" r="6" :fill="eyeGlowColor" opacity="0.3"/>
        </g>

        <!-- 鼻孔 -->
        <circle cx="15" cy="62" r="2" :fill="nostrilColor"/>

        <!-- 嘴巴 -->
        <path d="M15 70 Q25 75 45 68" :stroke="mouthColor" stroke-width="2" fill="none"/>

        <!-- 条纹装饰 -->
        <line v-for="i in 3" :key="'stripe-'+i" :x1="80 + (i-1)*20" y1="60" :x2="80 + (i-1)*20" y2="90" :stroke="stripeColor" stroke-width="2"/>

        <!-- 特殊装饰（高等级） -->
        <g v-if="level >= 50" class="crown-decoration">
          <polygon points="100,15 95,25 90,15 85,25 80,15 80,30 120,30 120,15 115,25 110,15 105,25" fill="url(#crownGradient)"/>
        </g>

        <!-- 渐变定义 -->
        <defs>
          <linearGradient id="crownGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFD700"/>
            <stop offset="50%" stop-color="#FFA500"/>
            <stop offset="100%" stop-color="#FFD700"/>
          </linearGradient>
          <linearGradient id="spineGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" :stop-color="spineColorLight"/>
            <stop offset="100%" :stop-color="spineColorDark"/>
          </linearGradient>
          <linearGradient v-if="level >= 21" id="wingGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" :stop-color="wingColor" stop-opacity="0.8"/>
            <stop offset="100%" :stop-color="wingColor" stop-opacity="0.3"/>
          </linearGradient>
        </defs>
      </svg>
    </div>

    <!-- 气泡对话 -->
    <transition name="bubble">
      <div v-if="showSpeech" class="speech-bubble" :class="`bubble-${evolutionStage}`">
        {{ speechText }}
      </div>
    </transition>

    <!-- 成长粒子效果 -->
    <div v-if="showParticles" class="particle-container">
      <span v-for="i in 12" :key="i" class="particle" :style="getParticleStyle(i)">{{ particleEmoji }}</span>
    </div>

    <!-- 攻击力浮动文字 -->
    <div v-if="showBonus" class="bonus-text" :class="`bonus-${evolutionStage}`">
      +{{ bonusAmount }} 攻击力！
    </div>

    <!-- 属性面板 -->
    <div class="dino-stats">
      <div class="dino-stat stat-attack">
        <div class="dino-stat-icon">⚔️</div>
        <div class="dino-stat-value">{{ attack }}</div>
        <div class="dino-stat-label">攻击力</div>
      </div>
      <div class="dino-stat stat-defense">
        <div class="dino-stat-icon">🛡️</div>
        <div class="dino-stat-value">{{ defense }}</div>
        <div class="dino-stat-label">防御力</div>
      </div>
      <div class="dino-stat stat-days">
        <div class="dino-stat-icon">🔥</div>
        <div class="dino-stat-value">{{ streakDays }}</div>
        <div class="dino-stat-label">连续天数</div>
      </div>
    </div>

    <!-- 经验条 -->
    <div class="exp-section">
      <div class="exp-bar">
        <div class="exp-fill" :class="`exp-${evolutionStage}`" :style="{ width: expPercent + '%' }"></div>
        <div class="exp-glow" :style="{ width: expPercent + '%' }"></div>
      </div>
      <div class="exp-info">
        <span class="exp-text">距离升级还需 {{ expToNext }} 经验</span>
        <span class="exp-percent">{{ expPercent }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// 成就类型定义
interface Achievement {
  id: string
  icon: string
  name: string
}

const props = defineProps<{
  level: number
  attack: number
  defense: number
  streakDays: number
  expPercent: number
  expToNext: number
  achievements?: Achievement[]
}>()

// ========== 进化系统 ==========
type EvolutionStage = 'egg' | 'baby' | 'juvenile' | 'ancient' | 'dragon_king'

const evolutionStage = computed<EvolutionStage>(() => {
  if (props.level < 6) return 'egg'
  if (props.level < 11) return 'baby'
  if (props.level < 21) return 'juvenile'
  if (props.level < 51) return 'ancient'
  return 'dragon_king'
})

const stageNames: Record<EvolutionStage, string> = {
  egg: '恐龙蛋',
  baby: '小棘龙',
  juvenile: '大棘龙',
  ancient: '远古龙',
  dragon_king: '龙王'
}

// 恐龙缩放（随等级变大）
const dinoScale = computed(() => {
  const scales: Record<EvolutionStage, number> = {
    egg: 0.8,
    baby: 0.9,
    juvenile: 1.0,
    ancient: 1.15,
    dragon_king: 1.3
  }
  return scales[evolutionStage.value]
})

// ========== 颜色系统 ==========
const colorSchemes: Record<EvolutionStage, {
  body: string
  tail: string
  head: string
  headDark: string
  spine: string[]
  spineGlow: string
  eye: string
  eyeGlow: string
  leg: string
  arm: string
  stripe: string
  wing: string
}> = {
  egg: {
    body: '#9CA3AF',
    tail: '#6B7280',
    head: '#9CA3AF',
    headDark: '#6B7280',
    spine: ['#9CA3AF', '#9CA3AF', '#9CA3AF', '#9CA3AF', '#9CA3AF'],
    spineGlow: 'rgba(156, 163, 175, 0.3)',
    eye: '#1F2937',
    eyeGlow: 'rgba(156, 163, 175, 0.5)',
    leg: '#6B7280',
    arm: '#6B7280',
    stripe: '#6B7280',
    wing: '#6B7280'
  },
  baby: {
    body: '#5EEAD4',
    tail: '#2DD4BF',
    head: '#5EEAD4',
    headDark: '#14B8A6',
    spine: ['#14B8A6', '#2DD4BF', '#5EEAD4', '#2DD4BF', '#14B8A6'],
    spineGlow: 'rgba(45, 212, 191, 0.5)',
    eye: '#0D9488',
    eyeGlow: 'rgba(45, 212, 191, 0.5)',
    leg: '#2DD4BF',
    arm: '#2DD4BF',
    stripe: '#14B8A6',
    wing: '#5EEAD4'
  },
  juvenile: {
    body: '#34D399',
    tail: '#10B981',
    head: '#34D399',
    headDark: '#059669',
    spine: ['#059669', '#10B981', '#34D399', '#FCD34D', '#F59E0B'],
    spineGlow: 'rgba(16, 185, 129, 0.5)',
    eye: '#047857',
    eyeGlow: 'rgba(52, 211, 153, 0.5)',
    leg: '#10B981',
    arm: '#10B981',
    stripe: '#059669',
    wing: '#34D399'
  },
  ancient: {
    body: '#A78BFA',
    tail: '#8B5CF6',
    head: '#A78BFA',
    headDark: '#7C3AED',
    spine: ['#7C3AED', '#8B5CF6', '#A78BFA', '#C4B5FD', '#DDD6FE'],
    spineGlow: 'rgba(139, 92, 246, 0.6)',
    eye: '#5B21B6',
    eyeGlow: 'rgba(167, 139, 250, 0.6)',
    leg: '#8B5CF6',
    arm: '#8B5CF6',
    stripe: '#7C3AED',
    wing: '#C4B5FD'
  },
  dragon_king: {
    body: 'url(#rainbowBody)',
    tail: '#F472B6',
    head: '#FBBF24',
    headDark: '#F59E0B',
    spine: ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6'],
    spineGlow: 'rgba(251, 191, 36, 0.8)',
    eye: '#7C2D12',
    eyeGlow: 'rgba(251, 191, 36, 0.8)',
    leg: '#F472B6',
    arm: '#A78BFA',
    stripe: '#FBBF24',
    wing: '#FDE68A'
  }
}

// 获取当前颜色
const currentColors = computed(() => colorSchemes[evolutionStage.value])
const bodyColor = computed(() => currentColors.value.body)
const tailColor = computed(() => currentColors.value.tail)
const headColor = computed(() => currentColors.value.head)
const headDarkColor = computed(() => currentColors.value.headDark)
const legColor = computed(() => currentColors.value.leg)
const footColor = computed(() => currentColors.value.leg)
const armColor = computed(() => currentColors.value.arm)
const wingColor = computed(() => currentColors.value.wing || currentColors.value.body)
const stripeColor = computed(() => currentColors.value.stripe)
const eyeColor = computed(() => currentColors.value.eye)
const eyeGlowColor = computed(() => currentColors.value.eyeGlow)
const nostrilColor = computed(() => currentColors.value.headDark)
const mouthColor = computed(() => currentColors.value.headDark)
const spineColorLight = computed(() => currentColors.value.spine[2])
const spineColorDark = computed(() => currentColors.value.spine[0])

// 眼睛瞳孔大小（高等级更大更有神）
const eyePupilSize = computed(() => {
  const sizes: Record<EvolutionStage, number> = {
    egg: 2,
    baby: 3,
    juvenile: 3,
    ancient: 3.5,
    dragon_king: 4
  }
  return sizes[evolutionStage.value]
})

// 背棘配置
const spines = computed(() => {
  const colors = currentColors.value.spine
  return [
    { points: '60,75 65,35 70,75', color: colors[0] },
    { points: '75,72 82,28 89,72', color: colors[1] },
    { points: '92,70 100,22 108,70', color: colors[2] },
    { points: '111,72 118,30 125,72', color: colors[3] },
    { points: '128,74 134,40 140,74', color: colors[4] }
  ]
})

// ========== 成就系统 ==========
const visibleAchievements = computed(() => props.achievements?.slice(0, 6) || [])

const getAchievementStyle = (index: number) => {
  const angle = (index * 60 - 90) * (Math.PI / 180)
  const radius = 100
  const x = Math.cos(angle) * radius
  const y = Math.sin(angle) * radius
  return {
    transform: `translate(${x}px, ${y}px)`,
    animationDelay: `${index * 0.1}s`
  }
}

// ========== 动画状态 ==========
const isGrowing = ref(false)
const showParticles = ref(false)
const showBonus = ref(false)
const showSpeech = ref(false)
const bonusAmount = ref(0)
const speechText = ref('')
const currentAction = ref('')
const isWiggling = ref(false)
const isFlying = ref(false)

// 粒子表情
const particleEmoji = computed(() => {
  const emojis: Record<EvolutionStage, string> = {
    egg: '✨',
    baby: '🌱',
    juvenile: '⭐',
    ancient: '💫',
    dragon_king: '👑'
  }
  return emojis[evolutionStage.value] || '✨'
})

// ========== 点击互动 ==========
const handleDinoClick = () => {
  const actions = ['jump', 'wiggle', 'blink', 'spin', 'sparkle']
  const randomAction = actions[Math.floor(Math.random() * actions.length)]
  playAnimation(randomAction)

  // 随机说一句话
  const quotes = getQuotes()
  const randomQuote = quotes[Math.floor(Math.random() * quotes.length)]
  if (randomQuote) {
    showSpeechBubble(randomQuote)
  }
}

const getQuotes = () => {
  const stageQuotes: Record<EvolutionStage, string[]> = {
    egg: ['咔咔...', '我要出来了...', '等等我...', '壳好硬...'],
    baby: ['嗷呜～', '我好开心！', '继续加油哦！', '我们一起成长！', '摸摸头～'],
    juvenile: ['我要变强！', '今天也很棒！', '坚持下去！', '你是最棒的！', '冲冲冲！'],
    ancient: ['力量涌上来了！', '我感觉到了远古的力量！', '没有什么能阻挡我们！', '让我们飞得更高！'],
    dragon_king: ['朕乃龙王！', '天下无敌！', '与我同行吧！', '荣耀属于我们！', '传说的力量！']
  }
  return stageQuotes[evolutionStage.value] || []
}

const playAnimation = (action: string = 'jump') => {
  currentAction.value = `action-${action}`

  if (action === 'wiggle') {
    isWiggling.value = true
    setTimeout(() => { isWiggling.value = false }, 500)
  }

  if (action === 'sparkle') {
    showParticles.value = true
    setTimeout(() => { showParticles.value = false }, 1000)
  }

  if (action === 'jump') {
    isGrowing.value = true
    setTimeout(() => { isGrowing.value = false }, 600)
  }

  if (action === 'spin') {
    setTimeout(() => { currentAction.value = '' }, 800)
    return
  }

  setTimeout(() => { currentAction.value = '' }, 500)
}

const showSpeechBubble = (text: string = '') => {
  speechText.value = text
  showSpeech.value = true
  setTimeout(() => { showSpeech.value = false }, 2500)
}

// 成长动画方法（暴露给父组件）
const growUp = (bonus: number) => {
  bonusAmount.value = bonus

  isGrowing.value = true
  showParticles.value = true
  showBonus.value = true

  setTimeout(() => { isGrowing.value = false }, 600)
  setTimeout(() => { showParticles.value = false }, 1000)
  setTimeout(() => { showBonus.value = false }, 1500)
}

// 背景星星样式
const getBgStarStyle = (index: number) => ({
  left: `${Math.random() * 100}%`,
  top: `${Math.random() * 100}%`,
  fontSize: `${4 + Math.random() * 8}px`,
  animationDelay: `${index * 0.3}s`,
  opacity: 0.2 + Math.random() * 0.3
})

// 粒子位置生成
const getParticleStyle = (index: number) => {
  const angle = (index - 1) * 30
  const radius = 80 + Math.random() * 40
  const x = Math.cos(angle * Math.PI / 180) * radius
  const y = Math.sin(angle * Math.PI / 180) * radius

  return {
    '--tx': `${x}px`,
    '--ty': `${y}px`,
    animationDelay: `${index * 0.05}s`
  }
}

defineExpose({ growUp })
</script>

<style scoped>
/* ========== 基础容器 ========== */
.dino-area {
  text-align: center;
  padding: 30px 20px;
  border-radius: 24px;
  margin-bottom: 15px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 阶段背景 */
.dino-area.stage-egg {
  background: linear-gradient(180deg, #374151 0%, #1F2937 50%, #111827 100%);
}

.dino-area.stage-baby {
  background: linear-gradient(180deg, #0D9488 0%, #115E59 50%, #134E4A 100%);
}

.dino-area.stage-juvenile {
  background: linear-gradient(180deg, #059669 0%, #047857 50%, #064E3B 100%);
}

.dino-area.stage-ancient {
  background: linear-gradient(180deg, #7C3AED 0%, #5B21B6 50%, #3B0764 100%);
}

.dino-area.stage-dragon_king {
  background: linear-gradient(135deg, #EF4444 0%, #F59E0B 25%, #10B981 50%, #3B82F6 75%, #8B5CF6 100%);
  background-size: 400% 400%;
  animation: rainbowBg 8s ease infinite;
}

@keyframes rainbowBg {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* ========== 背景装饰 ========== */
.bg-decorations {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
}

.bg-star {
  position: absolute;
  color: rgba(255, 255, 255, 0.4);
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.2); }
}

/* ========== 进化光环 ========== */
.evolution-aura {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  border-radius: 50%;
  pointer-events: none;
  animation: auraPulse 2s ease-in-out infinite;
}

.aura-ancient {
  background: radial-gradient(circle, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
  box-shadow: 0 0 60px rgba(139, 92, 246, 0.4);
}

.aura-dragon_king {
  background: radial-gradient(circle, rgba(251, 191, 36, 0.3) 0%, transparent 70%);
  box-shadow: 0 0 80px rgba(251, 191, 36, 0.5), 0 0 120px rgba(239, 68, 68, 0.3);
}

@keyframes auraPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.8; }
  50% { transform: translate(-50%, -50%) scale(1.1); opacity: 1; }
}

/* ========== 等级徽章 ========== */
.level-badge {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.badge-egg {
  background: rgba(156, 163, 175, 0.2);
  border: 1px solid rgba(156, 163, 175, 0.3);
}

.badge-baby {
  background: rgba(45, 212, 191, 0.2);
  border: 1px solid rgba(45, 212, 191, 0.3);
}

.badge-juvenile {
  background: rgba(16, 185, 129, 0.2);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.badge-ancient {
  background: rgba(139, 92, 246, 0.2);
  border: 1px solid rgba(139, 92, 246, 0.3);
  box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}

.badge-dragon_king {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.3) 0%, rgba(239, 68, 68, 0.2) 100%);
  border: 2px solid rgba(251, 191, 36, 0.5);
  box-shadow: 0 0 30px rgba(251, 191, 36, 0.4);
  animation: badgeGlow 2s ease-in-out infinite;
}

@keyframes badgeGlow {
  0%, 100% { box-shadow: 0 0 20px rgba(251, 191, 36, 0.4); }
  50% { box-shadow: 0 0 40px rgba(251, 191, 36, 0.6); }
}

.level-crown {
  font-size: 18px;
  animation: crownFloat 2s ease-in-out infinite;
}

@keyframes crownFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

.level-wings {
  font-size: 16px;
  animation: wingsPulse 1.5s ease-in-out infinite;
}

@keyframes wingsPulse {
  0%, 100% { opacity: 0.7; }
  50% { opacity: 1; }
}

.level-text {
  font-weight: 700;
  font-size: 16px;
  color: #fff;
}

.stage-name {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  padding-left: 8px;
  border-left: 1px solid rgba(255, 255, 255, 0.3);
}

/* ========== 成就徽章 ========== */
.achievements-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  pointer-events: none;
}

.achievement-badge {
  position: absolute;
  font-size: 20px;
  animation: badgeFloat 3s ease-in-out infinite;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

@keyframes badgeFloat {
  0%, 100% { transform: translate(var(--tx, 0), var(--ty, 0)) scale(1); }
  50% { transform: translate(var(--tx, 0), var(--ty, 0)) scale(1.1); }
}

/* ========== 恐龙容器 ========== */
.dino-container {
  position: relative;
  display: inline-block;
  margin-bottom: 15px;
  transition: transform 0.3s ease;
}

.spinosaurus {
  width: 180px;
  height: 140px;
  animation: breathe 3s ease-in-out infinite;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  transition: filter 0.3s ease;
}

.spinosaurus.color-dragon_king {
  filter: drop-shadow(0 4px 12px rgba(251, 191, 36, 0.4));
}

@keyframes breathe {
  0%, 100% { transform: scale(1) translateY(0); }
  50% { transform: scale(1.03) translateY(-3px); }
}

/* 恐龙部件动画 */
.dino-tail {
  animation: tailWag 2s ease-in-out infinite;
  transform-origin: left center;
}

@keyframes tailWag {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(5deg); }
  75% { transform: rotate(-5deg); }
}

.dino-eye {
  animation: blink 4s ease-in-out infinite;
}

@keyframes blink {
  0%, 45%, 55%, 100% { transform: scaleY(1); }
  50% { transform: scaleY(0.1); }
}

.eye-dragon_king {
  filter: drop-shadow(0 0 6px rgba(251, 191, 36, 0.8));
}

.spine-glow {
  animation: spinePulse 2s ease-in-out infinite;
}

@keyframes spinePulse {
  0%, 100% { opacity: 0.9; }
  50% { opacity: 1; }
}

.spine-ancient .spine {
  filter: drop-shadow(0 0 4px rgba(139, 92, 246, 0.6));
}

.spine-dragon_king .spine {
  filter: drop-shadow(0 0 8px rgba(251, 191, 36, 0.8));
  animation: spineRainbow 2s ease-in-out infinite;
}

@keyframes spineRainbow {
  0%, 100% { filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.8)); }
  33% { filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.8)); }
  66% { filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.8)); }
}

.dino-wings {
  animation: wingsFloat 3s ease-in-out infinite;
}

@keyframes wingsFloat {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.8; }
}

.wings-flap {
  animation: wingsFlap 0.3s ease-in-out;
}

@keyframes wingsFlap {
  0%, 100% { transform: scaleX(1); }
  50% { transform: scaleX(1.2); }
}

/* ========== 点击动作动画 ========== */
.action-jump {
  animation: dinoJump 0.5s ease-out;
}

@keyframes dinoJump {
  0%, 100% { transform: translateY(0); }
  30% { transform: translateY(-15px); }
  50% { transform: translateY(-20px); }
  70% { transform: translateY(-10px); }
}

.action-wiggle {
  animation: dinoWiggle 0.5s ease-out;
}

@keyframes dinoWiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-10deg); }
  75% { transform: rotate(10deg); }
}

.action-blink {
  animation: dinoBlink 0.3s ease-out;
}

@keyframes dinoBlink {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.action-spin {
  animation: dinoSpin 0.8s ease-out;
}

@keyframes dinoSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.action-sparkle {
  animation: dinoSparkle 0.5s ease-out;
}

@keyframes dinoSparkle {
  0%, 100% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.1); filter: brightness(1.3); }
}

.tail-wiggle {
  animation: tailWiggleFast 0.3s ease-in-out infinite;
}

@keyframes tailWiggleFast {
  0%, 100% { transform: rotate(0deg); }
  50% { transform: rotate(10deg); }
}

/* ========== 气泡对话 ========== */
.speech-bubble {
  position: absolute;
  top: 10%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  padding: 10px 18px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 100;
  white-space: nowrap;
}

.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-left: 8px solid transparent;
  border-right: 8px solid transparent;
  border-top: 10px solid rgba(255, 255, 255, 0.95);
}

.bubble-enter-active {
  animation: bubbleIn 0.3s ease-out;
}

.bubble-leave-active {
  animation: bubbleOut 0.3s ease-in;
}

@keyframes bubbleIn {
  from { opacity: 0; transform: translateX(-50%) translateY(-10px) scale(0.8); }
  to { opacity: 1; transform: translateX(-50%) translateY(0) scale(1); }
}

@keyframes bubbleOut {
  from { opacity: 1; transform: translateX(-50%) scale(1); }
  to { opacity: 0; transform: translateX(-50%) scale(0.8); }
}

/* ========== 属性面板 ========== */
.dino-stats {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.dino-stat {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 12px 16px;
  border-radius: 16px;
  text-align: center;
  min-width: 75px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.dino-stat:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.15);
}

.dino-stat-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.dino-stat-value {
  font-size: 22px;
  font-weight: bold;
}

.stat-attack .dino-stat-value { color: #FF6B6B; }
.stat-defense .dino-stat-value { color: #2DD4BF; }
.stat-days .dino-stat-value { color: #FFD93D; }

.dino-stat-label {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.7);
  margin-top: 2px;
}

/* ========== 经验条 ========== */
.exp-section {
  margin-top: 10px;
}

.exp-bar {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  height: 10px;
  overflow: hidden;
  position: relative;
}

.exp-fill {
  height: 100%;
  transition: width 0.5s ease;
  border-radius: 10px;
  position: relative;
  z-index: 2;
}

.exp-egg { background: linear-gradient(90deg, #9CA3AF, #D1D5DB); }
.exp-baby { background: linear-gradient(90deg, #14B8A6, #2DD4BF, #5EEAD4); }
.exp-juvenile { background: linear-gradient(90deg, #059669, #10B981, #34D399); }
.exp-ancient { background: linear-gradient(90deg, #7C3AED, #8B5CF6, #A78BFA); }
.exp-dragon_king {
  background: linear-gradient(90deg, #EF4444, #F59E0B, #10B981, #3B82F6, #8B5CF6);
  background-size: 200% 100%;
  animation: expRainbow 2s linear infinite;
}

@keyframes expRainbow {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

.exp-glow {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.3);
  filter: blur(4px);
  z-index: 1;
}

.exp-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 6px;
  padding: 0 2px;
}

.exp-text {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

.exp-percent {
  font-size: 12px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

/* ========== 成长动画 ========== */
.grow-animation {
  animation: areaPulse 0.6s ease-out;
}

@keyframes areaPulse {
  0% { box-shadow: inset 0 0 0 0 rgba(139, 92, 246, 0.4); }
  50% { box-shadow: inset 0 0 50px 10px rgba(139, 92, 246, 0.6); }
  100% { box-shadow: inset 0 0 0 0 rgba(139, 92, 246, 0); }
}

.dino-jump {
  animation: dinoJumpAnim 0.6s ease-out;
}

@keyframes dinoJumpAnim {
  0%, 100% { transform: scale(1) translateY(0); }
  30% { transform: scale(1.05) translateY(-10px); }
  50% { transform: scale(1.08) translateY(-15px); }
  70% { transform: scale(1.05) translateY(-8px); }
}

.spine-burst {
  animation: spineBurst 0.6s ease-out;
}

@keyframes spineBurst {
  0% { filter: brightness(1); }
  50% { filter: brightness(1.5) drop-shadow(0 0 15px rgba(251, 191, 36, 0.8)); }
  100% { filter: brightness(1); }
}

/* ========== 粒子效果 ========== */
.particle-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 10;
}

.particle {
  position: absolute;
  font-size: 24px;
  animation: particleFly 1s ease-out forwards;
}

@keyframes particleFly {
  0% {
    opacity: 1;
    transform: translate(0, 0) scale(0.5) rotate(0deg);
  }
  100% {
    opacity: 0;
    transform: translate(var(--tx), var(--ty)) scale(1.2) rotate(180deg);
  }
}

/* ========== 攻击力浮动文字 ========== */
.bonus-text {
  position: absolute;
  top: 25%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 22px;
  font-weight: bold;
  text-shadow: 0 0 15px currentColor, 0 2px 4px rgba(0, 0, 0, 0.3);
  animation: bonusFloat 1.5s ease-out forwards;
  z-index: 20;
}

.bonus-egg { color: #D1D5DB; }
.bonus-baby { color: #5EEAD4; }
.bonus-juvenile { color: #34D399; }
.bonus-ancient { color: #A78BFA; }
.bonus-dragon_king {
  background: linear-gradient(90deg, #FFD700, #FFA500);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes bonusFloat {
  0% {
    opacity: 0;
    transform: translateX(-50%) translateY(0) scale(0.5);
  }
  20% {
    opacity: 1;
    transform: translateX(-50%) translateY(-10px) scale(1.2);
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) translateY(-60px) scale(1);
  }
}
</style>