<template>
  <div class="admin-dashboard">
    <!-- 顶部导航 -->
    <div class="admin-header">
      <div class="header-left">
        <h1 class="admin-title">⚙️ 后台管理</h1>
        <span class="env-badge" :class="envInfo.env">{{ envInfo.env }}</span>
      </div>
      <div class="header-right">
        <n-button @click="refreshData">🔄 刷新</n-button>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="admin-content">
      <!-- AI 模型管理 -->
      <div class="admin-card">
        <div class="card-header">
          <h2>🤖 AI 模型配置</h2>
          <n-button type="primary" size="small" @click="saveModelConfig">
            💾 保存配置
          </n-button>
        </div>
        
        <div class="model-list">
          <div 
            v-for="model in models" 
            :key="model.id"
            class="model-item"
            :class="{ active: model.is_active }"
            @click="selectModel(model)">
            <div class="model-info">
              <div class="model-name">{{ model.model_name }}</div>
              <div class="model-type">{{ model.model_type }}</div>
            </div>
            <div class="model-status">
              <n-tag :type="model.is_active ? 'success' : 'default'" size="small">
                {{ model.is_active ? '✅ 使用中' : '⏸ 未激活' }}
              </n-tag>
            </div>
          </div>
        </div>

        <div class="model-tips">
          💡 点击选择要使用的 AI 模型，切换后即时生效
        </div>
      </div>

      <!-- 系统设置 -->
      <div class="admin-card">
        <div class="card-header">
          <h2>⚙️ 系统设置</h2>
        </div>
        
        <div class="settings-list">
          <div class="setting-item">
            <label class="setting-label">调试模式</label>
            <n-switch v-model:value="settings.debug" />
          </div>
          <div class="setting-item">
            <label class="setting-label">打印功能</label>
            <n-switch v-model:value="settings.print" />
          </div>
          <div class="setting-item">
            <label class="setting-label">语音输入</label>
            <n-switch v-model:value="settings.voice" />
          </div>
        </div>
      </div>

      <!-- 数据库信息 -->
      <div class="admin-card">
        <div class="card-header">
          <h2>📊 数据库信息</h2>
        </div>
        
        <div class="db-info">
          <div class="info-item">
            <span class="info-label">环境</span>
            <span class="info-value">{{ envInfo.env }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">数据库路径</span>
            <span class="info-value db-path">{{ healthInfo.database }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">服务状态</span>
            <n-tag type="success">✅ 正常运行</n-tag>
          </div>
          <div class="info-item">
            <span class="info-label">最后检查</span>
            <span class="info-value">{{ healthInfo.timestamp }}</span>
          </div>
        </div>
      </div>

      <!-- 快速操作 -->
      <div class="admin-card">
        <div class="card-header">
          <h2>⚡ 快速操作</h2>
        </div>
        
        <div class="quick-actions">
          <n-button block @click="clearCache">🗑️ 清除缓存</n-button>
          <n-button block type="warning" @click="backupData">📦 备份数据</n-button>
          <n-button block type="error" @click="resetDatabase">⚠️ 重置数据库</n-button>
        </div>
      </div>
    </div>

    <!-- 移动端底部导航 -->
    <div class="mobile-nav" v-if="isMobile">
      <div class="nav-item" @click="showSection = 'models'">
        <span class="nav-icon">🤖</span>
        <span class="nav-text">模型</span>
      </div>
      <div class="nav-item" @click="showSection = 'settings'">
        <span class="nav-icon">⚙️</span>
        <span class="nav-text">设置</span>
      </div>
      <div class="nav-item" @click="showSection = 'database'">
        <span class="nav-icon">📊</span>
        <span class="nav-text">数据库</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { NButton, NTag, NSwitch } from 'naive-ui'

const isMobile = ref(window.innerWidth < 768)
const showSection = ref('all')

const envInfo = ref({ env: 'loading', title: '', debug: false })
const healthInfo = ref({ status: '', database: '', timestamp: '' })
const models = ref([])
const settings = ref({
  debug: false,
  print: true,
  voice: false
})

// 检测移动端
window.addEventListener('resize', () => {
  isMobile.value = window.innerWidth < 768
})

// 加载数据
async function loadData() {
  try {
    // 获取环境信息
    const envRes = await fetch('/api/env')
    envInfo.value = await envRes.json()
    
    // 获取健康状态
    const healthRes = await fetch('/api/health')
    healthInfo.value = await healthRes.json()
    
    // 获取 AI 模型列表
    const modelsRes = await fetch('/api/admin/models')
    models.value = await modelsRes.json()
    
    // 获取系统设置
    const settingsRes = await fetch('/api/admin/settings')
    const settingsList = await settingsRes.json()
    settings.value = {
      debug: settingsList.find(s => s.key === 'debug')?.value === 'true' || false,
      print: settingsList.find(s => s.key === 'print')?.value === 'true' || true,
      voice: settingsList.find(s => s.key === 'voice')?.value === 'true' || false
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 刷新数据
function refreshData() {
  loadData()
}

// 选择模型
function selectModel(model) {
  models.value.forEach(m => {
    m.is_active = (m.id === model.id)
  })
}

// 保存模型配置
async function saveModelConfig() {
  try {
    const activeModel = models.value.find(m => m.is_active)
    if (!activeModel) {
      alert('请选择一个模型')
      return
    }
    
    await fetch(`/api/admin/models/${activeModel.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: true })
    })
    
    alert('✅ 模型配置已保存')
  } catch (error) {
    alert('❌ 保存失败：' + error.message)
  }
}

// 清除缓存
function clearCache() {
  if (confirm('确定要清除缓存吗？')) {
    localStorage.clear()
    alert('✅ 缓存已清除')
  }
}

// 备份数据
function backupData() {
  alert('📦 数据备份功能开发中...')
}

// 重置数据库
function resetDatabase() {
  if (confirm('⚠️ 警告：此操作将清空所有数据！确定要继续吗？')) {
    alert('⚠️ 重置数据库功能开发中...')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: #F8FAFC;
  padding: 16px;
  padding-bottom: 80px;
}

/* 顶部导航 */
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.admin-title {
  font-size: 20px;
  font-weight: 700;
  color: #1E293B;
  margin: 0;
}

.env-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.env-badge.development {
  background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
  color: white;
}

.env-badge.production {
  background: linear-gradient(135deg, #10B981 0%, #059669 100%);
  color: white;
}

/* 主要内容 */
.admin-content {
  display: grid;
  gap: 16px;
}

.admin-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: #1E293B;
  margin: 0;
}

/* 模型列表 */
.model-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.model-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: #F8FAFC;
  border-radius: 12px;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.3s;
}

.model-item:hover {
  background: #F1F5F9;
  transform: translateX(4px);
}

.model-item.active {
  border-color: #10B981;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(5, 150, 105, 0.05) 100%);
}

.model-info {
  flex: 1;
}

.model-name {
  font-size: 15px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 4px;
}

.model-type {
  font-size: 13px;
  color: #64748B;
}

.model-tips {
  margin-top: 12px;
  padding: 12px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(37, 99, 235, 0.05) 100%);
  border-radius: 8px;
  font-size: 13px;
  color: #3B82F6;
}

/* 系统设置 */
.settings-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #F1F5F9;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  font-size: 15px;
  color: #1E293B;
}

/* 数据库信息 */
.db-info {
  display: grid;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #F8FAFC;
  border-radius: 8px;
}

.info-label {
  font-size: 14px;
  color: #64748B;
}

.info-value {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
}

.db-path {
  font-family: monospace;
  font-size: 12px;
  color: #3B82F6;
}

/* 快速操作 */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 移动端导航 */
.mobile-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: none;
  background: white;
  border-top: 1px solid #E2E8F0;
  padding: 8px 0;
  padding-bottom: calc(8px + env(safe-area-inset-bottom, 0));
  z-index: 100;
}

.mobile-nav .nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px;
  cursor: pointer;
}

.nav-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.nav-text {
  font-size: 11px;
  color: #64748B;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 12px;
  }
  
  .admin-header {
    padding: 12px;
  }
  
  .admin-title {
    font-size: 18px;
  }
  
  .admin-card {
    padding: 16px;
  }
  
  .card-header h2 {
    font-size: 15px;
  }
  
  .mobile-nav {
    display: flex;
  }
  
  .admin-content {
    padding-bottom: 80px;
  }
}
</style>
