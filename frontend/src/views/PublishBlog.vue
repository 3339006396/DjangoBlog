<template>
  <div class="publish-container">
    <div class="publish-card">
      <h1 class="page-title">发布博客</h1>

      <form @submit.prevent="handleSubmit" class="publish-form">
        <div class="form-group">
          <label>标题</label>
          <input
            v-model="formData.title"
            type="text"
            placeholder="请输入博客标题"
            required
            minlength="2"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>分类</label>
          <select v-model="formData.category" required class="form-select">
            <option :value="null" disabled>请选择分类</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>内容</label>
          <textarea
            v-model="formData.content"
            placeholder="请输入博客内容（至少10字）"
            rows="10"
            required
            minlength="10"
            class="form-textarea"
          ></textarea>
        </div>

        <div v-if="error" class="error-msg">{{ error }}</div>
        <div v-if="success" class="success-msg">{{ success }}</div>

        <button type="submit" :disabled="loading" class="submit-btn">
          {{ loading ? '发布中...' : '发布博客' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const formData = ref({
  title: '',
  category: null,
  content: ''
})
const categories = ref([])
const loading = ref(false)
const error = ref('')
const success = ref('')

async function fetchCategories() {
  try {
    const response = await api.get('/categories/')
    console.log('分类接口完整返回:', response)
    categories.value = response.data?.results || []
    console.log('解析后的 categories:', categories.value)
  } catch (err) {
    console.error('获取分类失败:', err)
    error.value = '加载分类失败，请刷新重试'
  }
}

async function handleSubmit() {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const response = await api.post('/blogs/create/', formData.value)
    success.value = '博客发布成功！'
    setTimeout(() => {
      router.push(`/blog/${response.data.id}`)
    }, 1500)
  } catch (err) {
    // 精确显示后端返回的错误信息
    const backendMsg = err.response?.data?.msg
    const backendErrors = err.response?.data?.data?.errors
    if (backendErrors) {
      // 把字段级错误拼起来显示
      error.value = Object.values(backendErrors).flat().join('；')
    } else {
      error.value = backendMsg || '发布失败，请重试'
    }
    console.error('发布博客失败详情:', err.response?.data)
  } finally {
    loading.value = false
  }
}

onMounted(fetchCategories)
</script>

<style scoped>
.publish-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.publish-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
  border: 2px solid #ffd700;
  border-radius: 16px;
  padding: 2rem 3rem;
}

.page-title {
  color: #ffd700;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.5rem;
}

.publish-form {
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

.form-input,
.form-select,
.form-textarea {
  padding: 0.75rem 1rem;
  background-color: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: #ffd700;
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: #555;
}

.form-select {
  cursor: pointer;
}

.form-select option {
  background-color: #1a1a1a;
  color: #fff;
}

.form-textarea {
  resize: vertical;
  min-height: 200px;
  font-family: inherit;
}

.error-msg {
  color: #ff4444;
  background-color: rgba(255, 68, 68, 0.1);
  padding: 0.75rem;
  border-radius: 8px;
  text-align: center;
}

.success-msg {
  color: #44ff44;
  background-color: rgba(68, 255, 68, 0.1);
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
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(255, 215, 0, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>