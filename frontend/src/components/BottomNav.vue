<template>
  <div class="bottom-nav">
    <div
      v-for="item in navItems"
      :key="item.key"
      class="nav-item"
      :class="{ active: activeKey === item.key }"
      @click="handleNav(item.key)"
    >
      <div class="nav-icon-wrapper">
        <!-- 首页图标 -->
        <svg v-if="item.key === 'home'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
          <polyline points="9 22 9 12 15 12 15 22" />
        </svg>
        <!-- 计划图标 -->
        <svg v-else-if="item.key === 'plan'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
          <line x1="16" y1="2" x2="16" y2="6" />
          <line x1="8" y1="2" x2="8" y2="6" />
          <line x1="3" y1="10" x2="21" y2="10" />
          <path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01M16 18h.01" />
        </svg>
        <!-- 阅读图标 -->
        <svg v-else-if="item.key === 'reading'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
          <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
        </svg>
        <!-- AI 出题图标 -->
        <svg v-else-if="item.key === 'ai'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 16v-4" />
          <path d="M12 8h.01" />
          <path d="M8 12h8" />
          <path d="M9.5 9.5l1 1" />
          <path d="M14.5 14.5l-1-1" />
        </svg>
        <!-- 家长图标 -->
        <svg v-else-if="item.key === 'parent'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
          <circle cx="9" cy="7" r="4" />
          <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
          <path d="M16 3.13a4 4 0 0 1 0 7.75" />
        </svg>
      </div>
      <span class="nav-label">{{ item.label }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
interface NavItem {
  key: string
  label: string
  icon?: string
}

const props = defineProps<{
  activeKey: string
}>()

const emit = defineEmits<{
  (e: 'change', key: string): void
}>()

const navItems: NavItem[] = [
  { key: 'home', label: '首页' },
  { key: 'plan', label: '计划' },
  { key: 'ai', label: 'AI 学习', icon: 'ai' },
  { key: 'reading', label: '阅读' },
  { key: 'parent', label: '家长' },
]

const handleNav = (key: string) => {
  if (key === 'parent') {
    // 家长专区需要密码验证
    emit('change', key)
  } else {
    emit('change', key)
  }
}
</script>

<style scoped>
/* 薄荷绿主题变量 */
.bottom-nav {
  --primary: #14B8A6;
  --primary-light: #2DD4BF;
  --primary-dark: #0D9488;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94A3B8;
  --bg-card: #FFFFFF;

  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-card);
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
  padding-bottom: calc(8px + env(safe-area-inset-bottom, 0));
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.06);
  z-index: 100;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: 16px;
  position: relative;
}

.nav-item:hover {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.08) 0%, rgba(45, 212, 191, 0.08) 100%);
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(20, 184, 166, 0.12) 0%, rgba(45, 212, 191, 0.12) 100%);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 24px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
  border-radius: 0 0 4px 4px;
}

.nav-icon-wrapper {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-icon {
  width: 24px;
  height: 24px;
  color: var(--text-muted);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover .nav-icon {
  color: var(--primary);
}

.nav-item.active .nav-icon-wrapper {
  transform: scale(1.1);
}

.nav-item.active .nav-icon {
  color: var(--primary);
  fill: rgba(20, 184, 166, 0.15);
}

.nav-label {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 500;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-item:hover .nav-label {
  color: var(--text-secondary);
}

.nav-item.active .nav-label {
  color: var(--primary-dark);
  font-weight: 600;
}

/* 点击波纹效果 */
.nav-item:active {
  transform: scale(0.95);
}
</style>