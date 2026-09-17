import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('user_info') || 'null'))

  const isLoggedIn = computed(() => !!token.value)

  async function login(credentials) {
    const response = await api.post('/auth/login/', credentials)
    // response 已经是后端返回的完整对象（axios拦截器剥过一层了）
    const { data, tokens } = response

    token.value = tokens.access
    refreshToken.value = tokens.refresh
    userInfo.value = {
      id: data.id,
      username: data.username,
      email: data.email,
      avatar: data.avatar,
      is_superuser: data.is_superuser || false
    }

    localStorage.setItem('access_token', tokens.access)
    localStorage.setItem('refresh_token', tokens.refresh)
    localStorage.setItem('user_info', JSON.stringify(userInfo.value))
  }

  async function register(userData) {
    await api.post('/auth/register/', userData)
  }

  async function fetchUserInfo() {
    const response = await api.get('/auth/user/info/')
    userInfo.value = response.data
    localStorage.setItem('user_info', JSON.stringify(userInfo.value))
  }

  function logout() {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = null

    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_info')
  }

  async function refreshAccessToken() {
    try {
      const response = await api.post('/auth/token/refresh/', {
        refresh: refreshToken.value
      })
      // response 已经是后端返回的对象，直接取字段
      token.value = response.access || response.data?.access
      localStorage.setItem('access_token', token.value)
      return token.value
    } catch (error) {
      logout()
      throw error
    }
  }

  return {
    token,
    refreshToken,
    userInfo,
    isLoggedIn,
    login,
    register,
    fetchUserInfo,
    logout,
    refreshAccessToken
  }
})