import axios from 'axios'
import { useUserStore } from '../stores/user'
import router from '../router'

const api = axios.create({
  baseURL: '/',
  timeout: 10000
})

// 请求拦截器：添加 JWT Token
api.interceptors.request.use(
  (config) => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器：处理 Token 过期和错误
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    const originalRequest = error.config

    // 如果是 401 错误且不是刷新 Token 请求
    if (
      error.response?.status === 401 &&
      !originalRequest.url?.includes('refresh') &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true

      try {
        const userStore = useUserStore()
        // 尝试刷新 Token
        const newToken = await userStore.refreshAccessToken()
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return api(originalRequest)
      } catch (refreshError) {
        // 刷新失败，跳转到登录页
        const userStore = useUserStore()
        userStore.logout()
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }

    // 处理业务错误
    if (error.response?.data?.msg) {
      console.error('API Error:', error.response.data.msg)
    }

    return Promise.reject(error)
  }
)

export default api