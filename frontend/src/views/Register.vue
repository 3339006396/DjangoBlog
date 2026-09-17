<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1 class="auth-title">注 册</h1>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>用户名 (2-14位)</label>
          <input
            v-model="formData.username"
            type="text"
            placeholder="请输入用户名"
            required
            minlength="2"
            maxlength="14"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>邮箱</label>
          <input
            v-model="formData.email"
            type="email"
            placeholder="请输入邮箱"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>密码 (6-16位)</label>
          <input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            required
            minlength="6"
            maxlength="16"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>确认密码</label>
          <input
            v-model="formData.confirm_password"
            type="password"
            placeholder="请再次输入密码"
            required
            minlength="6"
            maxlength="16"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>验证码</label>
          <div class="captcha-row">
            <input
              v-model="formData.captcha"
              type="text"
              placeholder="请输入验证码"
              required
              maxlength="6"
              class="form-input"
            />
            <button
              type="button"
              @click="sendCaptcha"
              :disabled="countdown > 0"
              class="captcha-btn"
            >
              {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
            </button>
          </div>
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>

        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? '注册中...' : '注 册' }}
        </button>
      </form>

      <div class="auth-footer">
        <p>已有账号？</p>
        <router-link to="/login" class="link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'

const router = useRouter()
const userStore = useUserStore()

const formData = ref({
  username: '',
  email: '',
  password: '',
  confirm_password: '',
  captcha: ''
})
const loading = ref(false)
const error = ref('')
const countdown = ref(0)

async function sendCaptcha() {
  if (!formData.value.email) {
    error.value = '请先输入邮箱'
    return
  }

  try {
    await api.get('/auth/captcha/', { params: { email: formData.value.email } })
    error.value = ''
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (err) {
    error.value = err.response?.data?.msg || '验证码发送失败'
  }
}

async function handleRegister() {
  if (formData.value.password !== formData.value.confirm_password) {
    error.value = '两次密码不一致'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await userStore.register({
      username: formData.value.username,
      email: formData.value.email,
      password: formData.value.password,
      confirm_password: formData.value.confirm_password,
      captcha: formData.value.captcha
    })
    router.push('/login')
  } catch (err) {
    error.value = err.response?.data?.msg || '注册失败，请重试'
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
  padding: 2rem 3rem;
  width: 100%;
  max-width: 450px;
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
  gap: 1rem;
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

.captcha-row {
  display: flex;
  gap: 0.5rem;
}

.captcha-row .form-input {
  flex: 1;
}

.captcha-btn {
  padding: 0.75rem 1rem;
  background-color: #333;
  border: 1px solid #ffd700;
  color: #ffd700;
  border-radius: 8px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s;
}

.captcha-btn:hover:not(:disabled) {
  background-color: #ffd700;
  color: #000;
}

.captcha-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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