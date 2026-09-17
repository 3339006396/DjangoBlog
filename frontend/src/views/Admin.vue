<template>
  <div class="admin-container">
    <h1 class="page-title">管理后台</h1>

    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ stats.user_count }}</div>
        <div class="stat-label">用户总数</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.active_user_count }}</div>
        <div class="stat-label">活跃用户</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.blog_count }}</div>
        <div class="stat-label">博客总数</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.comment_count }}</div>
        <div class="stat-label">评论总数</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.category_count }}</div>
        <div class="stat-label">分类总数</div>
      </div>
    </div>

    <!-- Tab 切换 -->
    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab', { active: activeTab === tab.key }]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 用户管理 -->
    <div v-if="activeTab === 'users'" class="tab-content">
      <div class="search-bar">
        <input
          v-model="userSearch"
          type="text"
          placeholder="搜索用户名或邮箱..."
          @keyup.enter="searchUsers"
          class="search-input"
        />
        <button @click="searchUsers" class="search-btn">搜索</button>
      </div>

      <div class="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>用户名</th>
              <th>邮箱</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                  {{ user.is_active ? '正常' : '禁用' }}
                </span>
              </td>
              <td>
                <button
                  @click="toggleUserStatus(user)"
                  :class="['action-btn', user.is_active ? 'disable' : 'enable']"
                >
                  {{ user.is_active ? '禁用' : '启用' }}
                </button>
                <button @click="deleteUser(user.id)" class="action-btn delete">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 博客管理 -->
    <div v-if="activeTab === 'blogs'" class="tab-content">
      <div class="search-bar">
        <input
          v-model="blogSearch"
          type="text"
          placeholder="搜索博客..."
          @keyup.enter="searchBlogs"
          class="search-input"
        />
        <button @click="searchBlogs" class="search-btn">搜索</button>
      </div>

      <div class="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>标题</th>
              <th>作者</th>
              <th>分类</th>
              <th>发布时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="blog in blogs" :key="blog.id">
              <td>{{ blog.id }}</td>
              <td>{{ blog.title }}</td>
              <td>{{ blog.author_username }}</td>
              <td>{{ blog.category_name }}</td>
              <td>{{ formatTime(blog.pub_time) }}</td>
              <td>
                <button @click="deleteBlog(blog.id)" class="action-btn delete">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 分类管理 -->
    <div v-if="activeTab === 'categories'" class="tab-content">
      <div class="add-form">
        <input
          v-model="newCategoryName"
          type="text"
          placeholder="添加新分类"
          class="search-input"
        />
        <button @click="addCategory" class="search-btn">添加</button>
      </div>

      <div class="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>分类名</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cat in categories" :key="cat.id">
              <td>{{ cat.id }}</td>
              <td>{{ cat.name }}</td>
              <td>
                <button @click="deleteCategory(cat.id)" class="action-btn delete">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 评论管理 -->
    <div v-if="activeTab === 'comments'" class="tab-content">
      <div class="search-bar">
        <input
          v-model="commentSearch"
          type="text"
          placeholder="搜索评论..."
          @keyup.enter="searchComments"
          class="search-input"
        />
        <button @click="searchComments" class="search-btn">搜索</button>
      </div>

      <div class="data-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>评论内容</th>
              <th>博客</th>
              <th>作者</th>
              <th>时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comment in comments" :key="comment.id">
              <td>{{ comment.id }}</td>
              <td>{{ truncateText(comment.comment, 30) }}</td>
              <td>{{ comment.blog_title }}</td>
              <td>{{ comment.author_username }}</td>
              <td>{{ formatTime(comment.create_time) }}</td>
              <td>
                <button @click="deleteComment(comment.id)" class="action-btn delete">
                  删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const tabs = [
  { key: 'users', label: '用户管理' },
  { key: 'blogs', label: '博客管理' },
  { key: 'categories', label: '分类管理' },
  { key: 'comments', label: '评论管理' }
]

const activeTab = ref('users')
const stats = ref({})

// 用户
const users = ref([])
const userSearch = ref('')

// 博客
const blogs = ref([])
const blogSearch = ref('')

// 分类
const categories = ref([])
const newCategoryName = ref('')

// 评论
const comments = ref([])
const commentSearch = ref('')

async function fetchStats() {
  try {
    const response = await api.get('/admin_api/stats/')
    stats.value = response.data
  } catch (err) {
    console.error('获取统计数据失败:', err)
  }
}

async function fetchUsers() {
  try {
    const params = userSearch.value ? { keyword: userSearch.value } : {}
    const response = await api.get('/admin_api/users/', { params })
    users.value = response.data || []
  } catch (err) {
    console.error('获取用户列表失败:', err)
  }
}

async function fetchBlogs() {
  try {
    const params = blogSearch.value ? { keyword: blogSearch.value } : {}
    const response = await api.get('/admin_api/blogs/', { params })
    blogs.value = response.data || []
  } catch (err) {
    console.error('获取博客列表失败:', err)
  }
}

async function fetchCategories() {
  try {
    const response = await api.get('/admin_api/categories/')
    categories.value = response.data || []
  } catch (err) {
    console.error('获取分类列表失败:', err)
  }
}

async function fetchComments() {
  try {
    const params = commentSearch.value ? { keyword: commentSearch.value } : {}
    const response = await api.get('/admin_api/comments/', { params })
    comments.value = response.data || []
  } catch (err) {
    console.error('获取评论列表失败:', err)
  }
}

function searchUsers() {
  fetchUsers()
}

function searchBlogs() {
  fetchBlogs()
}

function searchComments() {
  fetchComments()
}

async function toggleUserStatus(user) {
  const action = user.is_active ? 'inactive' : 'active'
  try {
    await api.post(`/admin_api/users/${user.id}/toggle/?action=${action}`)
    fetchUsers()
    fetchStats()
  } catch (err) {
    alert(err.response?.data?.message || err.response?.data?.msg || '操作失败')
  }
}

async function deleteUser(id) {
  if (!confirm('确定删除该用户吗？')) return
  try {
    await api.delete(`/admin_api/users/${id}/`)
    fetchUsers()
    fetchStats()
  } catch (err) {
    alert(err.response?.data?.message || err.response?.data?.msg || '删除失败')
  }
}

async function deleteBlog(id) {
  if (!confirm('确定删除该博客吗？')) return
  try {
    await api.delete(`/admin_api/blogs/${id}/`)
    fetchBlogs()
    fetchStats()
  } catch (err) {
    alert(err.response?.data?.message || err.response?.data?.msg || '删除失败')
  }
}

async function addCategory() {
  if (!newCategoryName.value.trim()) return
  try {
    await api.post('/admin_api/categories/', { name: newCategoryName.value })
    newCategoryName.value = ''
    fetchCategories()
    fetchStats()
  } catch (err) {
    alert(err.response?.data?.message || err.response?.data?.msg || '添加失败')
  }
}

async function deleteCategory(id) {
  if (!confirm('确定删除该分类吗？')) return
  try {
    await api.delete(`/admin_api/categories/${id}/`)
    fetchCategories()
    fetchStats()
  } catch (err) {
    alert(err.response?.data?.message || err.response?.data?.msg || '删除失败')
  }
}

async function deleteComment(id) {
  if (!confirm('确定删除该评论吗？')) return
  try {
    await api.delete(`/admin_api/comments/${id}/`)
    fetchComments()
    fetchStats()
  } catch (err) {
    alert(err.response?.data?.message || err.response?.data?.msg || '删除失败')
  }
}

function formatTime(timeStr) {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

function truncateText(text, maxLen) {
  if (!text) return ''
  return text.length > maxLen ? text.substring(0, maxLen) + '...' : text
}

onMounted(() => {
  fetchStats()
  fetchUsers()
  fetchBlogs()
  fetchCategories()
  fetchComments()
})
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  color: #ffd700;
  margin-bottom: 2rem;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
  border: 1px solid #ffd700;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #ffd700;
}

.stat-label {
  color: #888;
  margin-top: 0.5rem;
}

/* Tab */
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #333;
}

.tab {
  padding: 0.75rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: #888;
  cursor: pointer;
  transition: all 0.3s;
}

.tab:hover {
  color: #fff;
}

.tab.active {
  color: #ffd700;
  border-bottom-color: #ffd700;
}

/* Tab 内容 */
.tab-content {
  background: #111;
  border: 1px solid #333;
  border-radius: 12px;
  padding: 1.5rem;
}

.search-bar,
.add-form {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  background-color: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  color: #fff;
  outline: none;
}

.search-input:focus {
  border-color: #ffd700;
}

.search-btn {
  padding: 0.75rem 1.5rem;
  background-color: #ffd700;
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #ffed4e;
}

/* 数据表格 */
.data-table {
  overflow-x: auto;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #333;
}

.data-table th {
  color: #ffd700;
  font-weight: 600;
  background-color: #1a1a1a;
}

.data-table td {
  color: #ccc;
}

.data-table tr:hover {
  background-color: rgba(255, 215, 0, 0.05);
}

/* 状态标签 */
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
}

.status-badge.active {
  background-color: rgba(68, 255, 68, 0.2);
  color: #44ff44;
}

.status-badge.inactive {
  background-color: rgba(255, 68, 68, 0.2);
  color: #ff4444;
}

/* 操作按钮 */
.action-btn {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  cursor: pointer;
  margin-right: 0.5rem;
  transition: all 0.3s;
}

.action-btn.enable {
  background-color: transparent;
  border: 1px solid #44ff44;
  color: #44ff44;
}

.action-btn.enable:hover {
  background-color: #44ff44;
  color: #000;
}

.action-btn.disable {
  background-color: transparent;
  border: 1px solid #ffaa00;
  color: #ffaa00;
}

.action-btn.disable:hover {
  background-color: #ffaa00;
  color: #000;
}

.action-btn.delete {
  background-color: transparent;
  border: 1px solid #ff4444;
  color: #ff4444;
}

.action-btn.delete:hover {
  background-color: #ff4444;
  color: #fff;
}
</style>