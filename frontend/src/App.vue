<template>
  <n-config-provider :theme="lightTheme">
    <n-message-provider>
      <div class="app-container">
        <n-layout-header bordered class="header">
          <h1>🎓 AI 助学小程序</h1>
          <p class="subtitle">智能计划表 · 错题本 · 每日出题</p>
        </n-layout-header>
        
        <n-layout-content class="content">
          <n-card title="📅 今日计划" size="medium">
            <n-space vertical>
              <n-input
                v-model:value="newTask"
                placeholder="输入自然语言添加任务，例如：'明天早上 8 点练琴 30 分钟'"
                clearable
                @keyup.enter="addTask"
              >
                <template #suffix>
                  <n-button type="primary" @click="addTask">添加</n-button>
                </template>
              </n-input>
              
              <n-divider />
              
              <n-empty v-if="tasks.length === 0" description="今天还没有计划，添加一个吧~" />
              
              <n-card
                v-for="(task, index) in tasks"
                :key="task.id"
                size="small"
                class="task-card"
              >
                <n-space justify="space-between" align="center">
                  <div>
                    <n-tag :type="task.type" size="small">{{ task.time }}</n-tag>
                    <span class="task-text">{{ task.content }}</span>
                  </div>
                  <n-button quaternary circle @click="removeTask(index)">
                    <template #icon>✕</template>
                  </n-button>
                </n-space>
              </n-card>
            </n-space>
          </n-card>
          
          <n-card title="💬 试试这样说" size="medium" class="examples">
            <n-space vertical>
              <n-tag type="info" variant="outline">"下周一带彩纸、剪刀、胶水"</n-tag>
              <n-tag type="success" variant="outline">"暑假每天加 1 小时阅读"</n-tag>
              <n-tag type="warning" variant="outline">"把周三的画画课改到周五"</n-tag>
            </n-space>
          </n-card>
        </n-layout-content>
      </div>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { NConfigProvider, NMessageProvider, NLayout, NLayoutHeader, NLayoutContent, 
         NCard, NInput, NButton, NSpace, NTag, NDivider, NEmpty } from 'naive-ui'
import { lightTheme } from 'naive-ui'

interface Task {
  id: number
  time: string
  content: string
  type: 'info' | 'success' | 'warning' | 'error'
}

const newTask = ref('')
const tasks = ref<Task[]>([
  { id: 1, time: '08:00', content: '晨读 20 分钟', type: 'info' },
  { id: 2, time: '09:00', content: '数学练习 3 道', type: 'success' },
  { id: 3, time: '15:00', content: '练琴 30 分钟', type: 'warning' },
])

let nextId = 4

const addTask = () => {
  if (!newTask.value.trim()) return
  
  // TODO: 调用 AI 解析自然语言
  tasks.value.push({
    id: nextId++,
    time: '待定',
    content: newTask.value,
    type: 'info'
  })
  newTask.value = ''
}

const removeTask = (index: number) => {
  tasks.value.splice(index, 1)
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #f5f7f9;
}

.header {
  padding: 24px;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
}

.subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

.content {
  padding: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.task-card {
  transition: all 0.3s;
}

.task-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.task-text {
  margin-left: 12px;
  font-size: 15px;
}

.examples {
  margin-top: 24px;
}
</style>
