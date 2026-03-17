<template>
  <div class="points-area">
    <div class="points-header">
      <div class="points-title">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align: middle; margin-right: 6px;">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
        </svg>
        我的积分
      </div>
      <span class="points-value">{{ points }}</span>
    </div>

    <!-- 等级进度 -->
    <div class="level-progress">
      <div class="level-badge star" :class="{ active: currentLevel === 'star' }">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
          <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
        </svg>
      </div>
      <div class="level-bar">
        <div class="level-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
      <div class="level-badge moon" :class="{ active: currentLevel === 'moon' }">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      </div>
      <div class="level-badge sun" :class="{ active: currentLevel === 'sun' }">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
          <circle cx="12" cy="12" r="5" />
          <line x1="12" y1="1" x2="12" y2="3" stroke="currentColor" stroke-width="2" />
          <line x1="12" y1="21" x2="12" y2="23" stroke="currentColor" stroke-width="2" />
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="currentColor" stroke-width="2" />
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="currentColor" stroke-width="2" />
          <line x1="1" y1="12" x2="3" y2="12" stroke="currentColor" stroke-width="2" />
          <line x1="21" y1="12" x2="23" y2="12" stroke="currentColor" stroke-width="2" />
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="currentColor" stroke-width="2" />
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="currentColor" stroke-width="2" />
        </svg>
      </div>
    </div>
    <div class="level-info">
      当前等级：<strong :style="{ color: levelColor }">{{ levelName }}</strong>
      <span class="level-next">→ 距离 {{ nextLevelIcon }} 还需 {{ pointsToNext }} 积分</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  points: number
}>()

const currentLevel = computed(() => {
  if (props.points >= 2000) return 'sun'
  if (props.points >= 700) return 'moon'
  return 'star'
})

const levelName = computed(() => {
  if (props.points >= 2000) return '☀️ 太阳 Lv.3'
  if (props.points >= 700) return '🌙 月亮 Lv.2'
  return '⭐ 星星 Lv.1'
})

const levelColor = computed(() => {
  if (props.points >= 2000) return '#F97316'
  if (props.points >= 700) return '#8B5CF6'
  return '#14B8A6'
})

const nextLevelIcon = computed(() => {
  if (props.points >= 2000) return '🏆 最高等级'
  if (props.points >= 700) return '☀️ 太阳'
  return '🌙 月亮'
})

const pointsToNext = computed(() => {
  if (props.points >= 2000) return 0
  if (props.points >= 700) return 2000 - props.points
  return 700 - props.points
})

const progressPercent = computed(() => {
  if (props.points >= 2000) return 100
  if (props.points >= 700) {
    return ((props.points - 700) / 1300) * 100
  }
  return (props.points / 700) * 100
})
</script>

<style scoped>
/* 薄荷绿主题变量 */
.points-area {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --accent: #F97316;
  --bg-light: #F8FAFC;
  --bg-card: #FFFFFF;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --radius-sm: 12px;
  --radius-md: 16px;

  background: linear-gradient(135deg, rgba(20, 184, 166, 0.08) 0%, rgba(45, 212, 191, 0.08) 100%);
  border: 1px solid rgba(20, 184, 166, 0.2);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  margin: 12px 0;
  box-shadow: var(--shadow-sm);
}

.points-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.points-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  display: flex;
  align-items: center;
}

.points-title svg {
  color: #F59E0B;
}

.points-value {
  font-size: 22px;
  font-weight: bold;
  background: linear-gradient(135deg, #F59E0B 0%, #FBBF24 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.level-progress {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.level-badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.35;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
}

.level-badge.star {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
  opacity: 1;
  box-shadow: 0 2px 6px rgba(20, 184, 166, 0.3);
}

.level-badge.star svg {
  width: 14px;
  height: 14px;
}

.level-badge.moon {
  background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
  color: white;
}

.level-badge.moon svg {
  width: 14px;
  height: 14px;
}

.level-badge.moon.active {
  opacity: 1;
  box-shadow: 0 2px 6px rgba(139, 92, 246, 0.3);
}

.level-badge.sun {
  background: linear-gradient(135deg, var(--accent) 0%, #FB923C 100%);
  color: white;
}

.level-badge.sun svg {
  width: 14px;
  height: 14px;
}

.level-badge.sun.active {
  opacity: 1;
  box-shadow: 0 2px 6px rgba(249, 115, 22, 0.3);
}

.level-bar {
  flex: 1;
  height: 8px;
  background: linear-gradient(90deg, #E2E8F0 0%, #F1F5F9 100%);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
}

.level-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 50%, #8B5CF6 100%);
}

.level-info {
  font-size: 11px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.level-info strong {
  font-weight: 600;
}

.level-next {
  color: var(--text-muted);
  margin-left: 4px;
}
</style>