<template>
  <div class="home-container">
    <!-- 搜索框 -->
    <div class="search-section">
      <div class="search-box">
        <input
          v-model="keyword"
          type="text"
          placeholder="搜索博客标题、内容、作者..."
          @keyup.enter="handleSearch"
          class="search-input"
        />
        <button @click="handleSearch" class="search-btn">搜索</button>
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="category-section">
      <span
        v-for="cat in categories"
        :key="cat.id"
        :class="['category-tag', { active: selectedCategory === cat.id }]"
        @click="filterByCategory(cat.id)"
      >
        {{ cat.name }}
      </span>
    </div>

    <!-- 博客列表 -->
    <div class="blog-list" v-loading="loading">
      <div
        v-for="blog in blogs"
        :key="blog.id"
        class="blog-card"
        @click="goToDetail(blog.id)"
      >
        <div class="blog-header">
          <h2 class="blog-title">{{ blog.title }}</h2>
          <span class="blog-category">{{ blog.category_name }}</span>
        </div>
        <p class="blog-content">{{ truncateContent(blog.content) }}</p>
        <div class="blog-meta">
          <span class="author">👤 {{ blog.author_username }}</span>
          <span class="time">🕐 {{ formatTime(blog.pub_time) }}</span>
          <span class="comments">💬 {{ blog.comment_count }} 评论</span>
        </div>
      </div>

      <div v-if="blogs.length === 0 && !loading" class="empty-state">
        <p>暂无博客内容</p>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > pageSize">
      <button @click="prevPage" :disabled="page === 1" class="page-btn">上一页</button>
      <span class="page-info">{{ page }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="page >= totalPages" class="page-btn">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const blogs = ref([])
const categories = ref([])
const keyword = ref('')
const selectedCategory = ref(null)
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

async function fetchBlogs() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value
    }
    if (keyword.value) {
      params.keyword = keyword.value
    }
    const response = await api.get('/blogs/', { params })
    blogs.value = response.data.results
    total.value = response.data.total
  } catch (error) {
    console.error('获取博客失败:', error)
  } finally {
    loading.value = false
  }
}

async function fetchCategories() {
  try {
    const response = await api.get('/categories/')
    categories.value = response.data.results
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

function handleSearch() {
  page.value = 1
  fetchBlogs()
}

function filterByCategory(categoryId) {
  selectedCategory.value = selectedCategory.value === categoryId ? null : categoryId
}

function truncateContent(content) {
  if (!content) return ''
  return content.length > 100 ? content.substring(0, 100) + '...' : content
}

function formatTime(timeStr) {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

function goToDetail(id) {
  router.push(`/blog/${id}`)
}

function prevPage() {
  if (page.value > 1) {
    page.value--
    fetchBlogs()
  }
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++
    fetchBlogs()
  }
}

onMounted(() => {
  fetchBlogs()
  fetchCategories()
})
</script>

<style scoped>
.home-container {
  padding: 2rem 0;
}

/* 搜索 */
.search-section {
  margin-bottom: 2rem;
}

.search-box {
  display: flex;
  gap: 1rem;
  max-width: 600px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background-color: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #ffd700;
}

.search-input::placeholder {
  color: #666;
}

.search-btn {
  padding: 0.75rem 2rem;
  background-color: #ffd700;
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background-color: #ffed4e;
}

/* 分类标签 */
.category-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.category-tag {
  padding: 0.5rem 1rem;
  background-color: #1a1a1a;
  border: 1px solid #ffd700;
  border-radius: 20px;
  color: #ffd700;
  cursor: pointer;
  transition: all 0.3s;
}

.category-tag:hover,
.category-tag.active {
  background-color: #ffd700;
  color: #000;
}

/* 博客卡片 */
.blog-list {
  display: grid;
  gap: 1.5rem;
}

.blog-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #121212 100%);
  border: 1px solid #333;
  border-radius: 12px;
  padding: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
}

.blog-card:hover {
  border-color: #ffd700;
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(255, 215, 0, 0.1);
}

.blog-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
}

.blog-title {
  font-size: 1.4rem;
  color: #fff;
  margin: 0;
}

.blog-category {
  background-color: #ffd700;
  color: #000;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: bold;
}

.blog-content {
  color: #aaa;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.blog-meta {
  display: flex;
  gap: 1.5rem;
  color: #888;
  font-size: 0.875rem;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-btn {
  padding: 0.5rem 1rem;
  background-color: #1a1a1a;
  border: 1px solid #ffd700;
  color: #ffd700;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.page-btn:hover:not(:disabled) {
  background-color: #ffd700;
  color: #000;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #ffd700;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #666;
}
</style>