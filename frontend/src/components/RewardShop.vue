<template>
  <n-modal v-model:show="showModal" preset="card" style="width: 90%; max-width: 400px;" class="reward-shop-modal">
    <template #header>
      <div class="modal-header">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 12 20 22 4 22 4 12" />
            <rect x="2" y="7" width="20" height="5" />
            <line x1="12" y1="22" x2="12" y2="7" />
            <path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z" />
            <path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z" />
          </svg>
        </div>
        <span class="header-title">奖励商城</span>
      </div>
    </template>

    <div class="reward-content">
      <!-- 当前积分 -->
      <div class="current-points">
        <span class="points-label">当前积分</span>
        <span class="points-value">{{ points }}</span>
      </div>

      <!-- 等级说明 -->
      <div class="level-guide">
        <div class="level-guide-title">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
            <path d="M18 20V10M12 20V4M6 20v-6" />
          </svg>
          等级说明
        </div>
        <div class="level-guide-item">
          <div class="level-badge star">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
          </div>
          <div class="level-guide-info">
            <div class="level-guide-name">星星等级</div>
            <div class="level-guide-range">0 - 700 积分</div>
          </div>
        </div>
        <div class="level-guide-item">
          <div class="level-badge moon">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
          </div>
          <div class="level-guide-info">
            <div class="level-guide-name">月亮等级</div>
            <div class="level-guide-range">700 - 2000 积分</div>
          </div>
        </div>
        <div class="level-guide-item">
          <div class="level-badge sun">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
              <circle cx="12" cy="12" r="5" />
            </svg>
          </div>
          <div class="level-guide-info">
            <div class="level-guide-name">太阳等级</div>
            <div class="level-guide-range">2000+ 积分</div>
          </div>
        </div>
      </div>

      <!-- 可兑换奖励 -->
      <div class="reward-title">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 4px;">
          <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
          <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
          <path d="M4 22h16" />
          <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" />
          <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
          <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z" />
        </svg>
        可兑换奖励
      </div>

      <div class="reward-list">
        <div v-for="reward in rewards" :key="reward.id" class="reward-item" :class="{ disabled: !canExchange(reward) }">
          <div class="reward-item-icon">{{ reward.icon }}</div>
          <div class="reward-item-info">
            <div class="reward-item-name">{{ reward.name }}</div>
            <div class="reward-item-desc">{{ reward.description }}</div>
          </div>
          <div class="reward-item-cost">{{ reward.cost }}</div>
          <n-button
            :type="canExchange(reward) ? 'primary' : 'default'"
            :disabled="!canExchange(reward)"
            size="small"
            class="exchange-btn"
            @click="handleExchange(reward)"
          >
            {{ getExchangeLabel(reward) }}
          </n-button>
        </div>
      </div>
    </div>
  </n-modal>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { NModal, NButton, useMessage } from 'naive-ui'

const props = defineProps<{
  show: boolean
  points: number
}>()

const emit = defineEmits<{
  (e: 'update:show', value: boolean): void
  (e: 'exchange', reward: any): void
}>()

const message = useMessage()

const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

interface Reward {
  id: number
  name: string
  icon: string
  description: string
  cost: number
  requiredLevel: 'star' | 'moon' | 'sun'
}

const rewards: Reward[] = [
  { id: 1, name: '冰淇淋一支', icon: '🍦', description: '任意口味，周末享用', cost: 50, requiredLevel: 'star' },
  { id: 2, name: '游戏时间 30 分钟', icon: '🎮', description: '周末使用，需家长同意', cost: 100, requiredLevel: 'star' },
  { id: 3, name: '看一部电影', icon: '🎬', description: '周末家庭电影夜', cost: 200, requiredLevel: 'star' },
  { id: 4, name: '游乐园一日游', icon: '🎢', description: '需要月亮等级解锁', cost: 500, requiredLevel: 'moon' },
  { id: 5, name: '心愿礼物（100元内）', icon: '🎁', description: '需要太阳等级解锁', cost: 1000, requiredLevel: 'sun' },
]

const currentLevel = computed(() => {
  if (props.points >= 2000) return 'sun'
  if (props.points >= 700) return 'moon'
  return 'star'
})

const canExchange = (reward: Reward) => {
  const levelOrder = { star: 1, moon: 2, sun: 3 }
  const hasLevel = levelOrder[currentLevel.value] >= levelOrder[reward.requiredLevel]
  const hasPoints = props.points >= reward.cost
  return hasLevel && hasPoints
}

const getExchangeLabel = (reward: Reward) => {
  const levelOrder = { star: 1, moon: 2, sun: 3 }
  if (levelOrder[currentLevel.value] < levelOrder[reward.requiredLevel]) {
    return '🔒 等级不足'
  }
  if (props.points < reward.cost) {
    return '积分不足'
  }
  return '兑换'
}

const handleExchange = (reward: Reward) => {
  if (canExchange(reward)) {
    emit('exchange', reward)
    message.success(`成功兑换「${reward.name}」！`)
  }
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.reward-shop-modal {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --accent: #F97316;
  --bg-light: #F8FAFC;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  --radius-sm: 12px;
  --radius-md: 16px;
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, var(--accent) 0%, #FB923C 100%);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.header-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-primary);
}

.reward-content {
  padding: 0;
}

.current-points {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 14px;
  background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
  border-radius: var(--radius-md);
  font-size: 14px;
}

.points-label {
  color: #92400E;
  font-weight: 500;
}

.points-value {
  font-size: 26px;
  font-weight: bold;
  color: #D97706;
}

.level-guide {
  background: var(--bg-light);
  border-radius: var(--radius-md);
  padding: 14px;
  margin-bottom: 16px;
}

.level-guide-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.level-guide-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.level-guide-item:last-child {
  margin-bottom: 0;
}

.level-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.level-badge.star {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
}

.level-badge.moon {
  background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
  color: white;
}

.level-badge.sun {
  background: linear-gradient(135deg, var(--accent) 0%, #FB923C 100%);
  color: white;
}

.level-guide-info {
  flex: 1;
}

.level-guide-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.level-guide-range {
  font-size: 11px;
  color: var(--text-muted);
}

.reward-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.reward-list {
  max-height: 320px;
  overflow-y: auto;
}

.reward-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  background: var(--bg-light);
  border-radius: var(--radius-md);
  margin-bottom: 10px;
  transition: all 0.3s;
}

.reward-item:last-child {
  margin-bottom: 0;
}

.reward-item:hover:not(.disabled) {
  background: rgba(20, 184, 166, 0.06);
  transform: translateX(4px);
}

.reward-item.disabled {
  opacity: 0.6;
}

.reward-item-icon {
  font-size: 28px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: var(--radius-sm);
  flex-shrink: 0;
}

.reward-item-info {
  flex: 1;
  min-width: 0;
}

.reward-item-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.reward-item-desc {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

.reward-item-cost {
  font-size: 16px;
  font-weight: bold;
  color: #D97706;
  flex-shrink: 0;
}

.exchange-btn {
  flex-shrink: 0;
  border-radius: 8px;
  font-weight: 500;
}
</style>