/**
 * AI 伴学小程序 - API 服务
 */

// API 基础地址 - 根据环境自动切换
const API_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8000/api/v1'
  : 'http://8.130.161.121:8000/api/v1'

interface ApiResponse<T> {
  data?: T
  error?: string
}

// 邀请链接相关 API
export const inviteApi = {
  // 创建邀请链接
  create: async (data: {
    student_id: string
    expire_type: '7days' | '30days' | 'forever'
    usage_type: 'once' | 'multiple'
  }): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/invite-links`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取邀请链接列表
  list: async (studentId: string): Promise<ApiResponse<any[]>> => {
    try {
      const res = await fetch(`${API_BASE}/invite-links/${studentId}`)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 关闭邀请链接
  disable: async (code: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/invite-links/${code}/disable`, {
        method: 'POST'
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  }
}

// 账号绑定相关 API
export const bindingApi = {
  // 申请绑定
  create: async (data: {
    invite_code: string
    relation: string
  }): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/bindings`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取绑定列表
  list: async (): Promise<ApiResponse<any[]>> => {
    try {
      const res = await fetch(`${API_BASE}/bindings`)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 审批绑定
  approve: async (bindingId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/bindings/${bindingId}/approve`, {
        method: 'POST'
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  }
}

// 老师学习建议相关 API
export const teacherAdviceApi = {
  // 创建建议
  create: async (data: {
    student_id: string
    raw_content: string
  }): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/teacher-advices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // AI 解析
  parse: async (adviceId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/teacher-advices/${adviceId}/parse`, {
        method: 'POST'
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 确认建议
  confirm: async (adviceId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/teacher-advices/${adviceId}/confirm`, {
        method: 'POST'
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取建议列表
  list: async (studentId: string): Promise<ApiResponse<any[]>> => {
    try {
      const res = await fetch(`${API_BASE}/teacher-advices/${studentId}`)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  }
}

// 每日一练相关 API
export const dailyPracticeApi = {
  // 获取每日一练
  get: async (studentId: string, date?: string): Promise<ApiResponse<any[]>> => {
    try {
      const url = date
        ? `${API_BASE}/daily-practice/${studentId}?date=${date}`
        : `${API_BASE}/daily-practice/${studentId}`
      const res = await fetch(url)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 家长确认
  verify: async (recordId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/daily-practice/${recordId}/verify`, {
        method: 'POST'
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 完成练习
  complete: async (recordId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/daily-practice/${recordId}/complete`, {
        method: 'POST'
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  }
}