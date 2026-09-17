<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">登 录</h1>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>用户名</label>
          <input
            v-model="formData.username"
            type="text"
            placeholder="请输入用户名"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>密码</label>
          <input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            required
            minlength="6"
            class="form-input"
          />
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? '登录中...' : '登 录' }}
        </button>
      </form>

      <div class="auth-footer">
        <p>还没有账号？</p>
        <router-link to="/register" class="link">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formData = ref({
  username: '',
  password: ''
})
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await userStore.login(formData.value)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (err) {
    error.value = err.response?.data?.msg || '登录失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.auth-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
  border: 2px solid #ffd700;
  border-radius: 16px;
  padding: 3rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 32px rgba(255, 215, 0, 0.1);
}

.auth-title {
  text-align: center;
  color: #ffd700;
  font-size: 2rem;
  margin-bottom: 2rem;
  letter-spacing: 0.5rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  color: #ccc;
  font-size: 0.875rem;
}

.form-input {
  padding: 0.75rem 1rem;
  background-color: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.form-input:focus {
  border-color: #ffd700;
}

.form-input::placeholder {
  color: #555;
}

.error-msg {
  color: #ff4444;
  background-color: rgba(255, 68, 68, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  text-align: center;
}

.submit-btn {
  padding: 1rem;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #000;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  letter-spacing: 0.25rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(255, 215, 0, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  color: #888;
}

.link {
  color: #ffd700;
  text-decoration: none;
  font-weight: bold;
}

.link:hover {
  text-decoration: underline;
}
</style>