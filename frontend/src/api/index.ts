/**
 * AI 伴学小程序 - API 服务
 */

// API 基础地址 - 使用相对路径，通过Vite代理转发
const API_BASE = '/api/v1'

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

// 古诗相关 API（AI动态生成）
export const poetryApi = {
  // AI对话推荐古诗
  chat: async (data: {
    message: string
    student_id?: string
    grade?: number
    textbook?: string
  }): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/poetry/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取AI推荐古诗
  recommend: async (params?: {
    student_id?: string
    grade?: number
    textbook?: string
  }): Promise<ApiResponse<any>> => {
    try {
      const query = new URLSearchParams()
      if (params?.student_id) query.append('student_id', params.student_id)
      if (params?.grade) query.append('grade', params.grade.toString())
      if (params?.textbook) query.append('textbook', params.textbook)

      const url = query.toString()
        ? `${API_BASE}/poetry/recommend?${query.toString()}`
        : `${API_BASE}/poetry/recommend`

      const res = await fetch(url)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取古诗列表（兼容旧API，返回AI生成的推荐）
  list: async (params?: {
    grade?: number
    semester?: string
    textbook?: string
  }): Promise<ApiResponse<any[]>> => {
    try {
      const query = new URLSearchParams()
      if (params?.grade) query.append('grade', params.grade.toString())
      if (params?.semester) query.append('semester', params.semester)
      if (params?.textbook) query.append('textbook', params.textbook)

      const url = query.toString()
        ? `${API_BASE}/poetry/list?${query.toString()}`
        : `${API_BASE}/poetry/list`

      const res = await fetch(url)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取古诗详情
  get: async (poetryId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/poetry/${poetryId}`)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取古诗内容（新API）
  getContent: async (title: string, author?: string): Promise<ApiResponse<any>> => {
    try {
      const query = new URLSearchParams()
      query.append('title', title)
      if (author) query.append('author', author)

      const res = await fetch(`${API_BASE}/poetry/content?${query.toString()}`)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 记录学习古诗（新API）
  learn: async (data: {
    student_id: string
    title: string
    author?: string
    dynasty?: string
    grade?: number
    textbook?: string
    mastery_level: 'new' | 'unfamiliar' | 'familiar' | 'mastered'
  }): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/poetry/learn`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 获取学生的学习记录列表
  getMemoryList: async (studentId: string): Promise<ApiResponse<any[]>> => {
    try {
      const res = await fetch(`${API_BASE}/poetry/memory/${studentId}`)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 提交学习状态（兼容旧API）
  submitMemory: async (data: {
    student_id: string
    poetry_id: string
    mastery_level: 'new' | 'unfamiliar' | 'familiar' | 'mastered'
  }): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/poetry/memory`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  }

// 精读推荐相关 API
export const readingRecommendApi = {
  // 获取今日精读推荐
  get: async (studentId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/reading/${studentId}/recommend`)
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 完成精读
  complete: async (studentId: string, data: {
    duration_minutes?: number
    liked?: boolean
  }): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/reading/${studentId}/recommend/complete`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  },

  // 换一篇精读
  new: async (studentId: string): Promise<ApiResponse<any>> => {
    try {
      const res = await fetch(`${API_BASE}/reading/${studentId}/recommend/new`, {
        method: 'POST'
      })
      return { data: await res.json() }
    } catch (e: any) {
      return { error: e.message }
    }
  }
}