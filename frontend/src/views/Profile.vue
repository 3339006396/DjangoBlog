<template>
  <div class="profile-container">
    <!-- 用户信息卡片 -->
    <div class="user-card">
      <div class="avatar-section">
        <div class="avatar-wrapper" @click="triggerUpload">
          <img :src="userInfo?.avatar" class="avatar-img" alt="头像" />
          <div class="avatar-overlay">{{ uploading ? '上传中...' : '点击更换' }}</div>
        </div>
        <input ref="fileInput" type="file" accept="image/*" hidden @change="handleFileChange" />
      </div>
      <div class="user-info">
        <h2 class="username">{{ userInfo?.username }}</h2>
        <p class="email">{{ userInfo?.email }}</p>
        <div class="tags">
          <span v-if="userInfo?.is_staff" class="tag admin">管理员</span>
          <span v-if="userInfo?.is_active" class="tag active">正常</span>
        </div>
        <p v-if="uploadError" class="upload-error">{{ uploadError }}</p>
      </div>
    </div>

    <!-- 我的博客 -->
    <div class="my-blogs-section">
      <h3 class="section-title">我的博客</h3>

      <div v-loading="blogsLoading" class="blog-list">
        <div
          v-for="blog in myBlogs"
          :key="blog.id"
          class="blog-card"
          @click="goToDetail(blog.id)"
        >
          <div class="blog-info">
            <h4 class="blog-title">{{ blog.title }}</h4>
            <div class="blog-meta">
              <span>{{ blog.category_name }}</span>
              <span>{{ formatTime(blog.pub_time) }}</span>
              <span>💬 {{ blog.comment_count }}</span>
            </div>
          </div>
          <button
            @click.stop="deleteBlog(blog.id)"
            class="delete-btn"
          >
            删除
          </button>
        </div>

        <div v-if="myBlogs.length === 0 && !blogsLoading" class="empty">
          还没有发布博客，
          <router-link to="/publish" class="link">立即发布一篇</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'

const router = useRouter()
const userStore = useUserStore()

const userInfo = ref(userStore.userInfo)
const myBlogs = ref([])
const blogsLoading = ref(false)
const fileInput = ref(null)
const uploading = ref(false)
const uploadError = ref('')

function triggerUpload() {
  fileInput.value.click()
}

async function handleFileChange(e) {
  const file = e.target.files[0]
  if (!file) return
  if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
    uploadError.value = '请选择 JPG/PNG/GIF 格式'
    return
  }
  if (file.size > 2 * 1024 * 1024) {
    uploadError.value = '图片不能超过 2MB'
    return
  }
  uploadError.value = ''
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('avatar', file)
    const res = await api.put('/auth/user/info/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    userInfo.value.avatar = res.avatar
    userStore.userInfo = userInfo.value
    localStorage.setItem('user_info', JSON.stringify(userInfo.value))
    alert('头像更新成功')
  } catch (err) {
    uploadError.value = err.response?.data?.msg || '上传失败'
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}

async function fetchMyBlogs() {
  blogsLoading.value = true
  try {
    const response = await api.get('/blogs/my/')
    myBlogs.value = response.data.results
  } catch (error) {
    console.error('获取我的博客失败:', error)
  } finally {
    blogsLoading.value = false
  }
}

async function deleteBlog(id) {
  if (!confirm('确定删除这篇博客吗？')) return

  try {
    await api.delete(`/blogs/${id}/delete/`)
    myBlogs.value = myBlogs.value.filter(b => b.id !== id)
  } catch (error) {
    alert(error.response?.data?.msg || '删除失败')
  }
}

function goToDetail(id) {
  router.push(`/blog/${id}`)
}

function formatTime(timeStr) {
  const date = new Date(timeStr)
  return date.toLocaleDateString('zh-CN')
}

onMounted(async () => {
  await userStore.fetchUserInfo()
  userInfo.value = userStore.userInfo
  fetchMyBlogs()
})
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
}

/* 用户卡片 */
.user-card {
  background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
  border: 2px solid #ffd700;
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  gap: 2rem;
  align-items: center;
  margin-bottom: 2rem;
}

.avatar-section {
  flex-shrink: 0;
}

.avatar-wrapper {
  width: 100px;
  height: 100px;
  position: relative;
  cursor: pointer;
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ffd700;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffd700;
  font-size: 0.75rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.upload-error {
  color: #ff4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.user-info {
  flex: 1;
}

.username {
  color: #ffd700;
  margin: 0 0 0.5rem 0;
}

.email {
  color: #aaa;
  margin: 0 0 1rem 0;
}

.tags {
  display: flex;
  gap: 0.5rem;
}

.tag {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
}

.tag.admin {
  background-color: #ffd700;
  color: #000;
}

.tag.active {
  background-color: #44ff44;
  color: #000;
}

/* 博客列表 */
.my-blogs-section {
  background: #111;
  border: 1px solid #333;
  border-radius: 12px;
  padding: 2rem;
}

.section-title {
  color: #ffd700;
  margin-bottom: 1.5rem;
}

.blog-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.blog-card {
  background-color: #1a1a1a;
  border: 1px solid #333;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s;
}

.blog-card:hover {
  border-color: #ffd700;
}

.blog-info {
  flex: 1;
}

.blog-title {
  color: #fff;
  margin: 0 0 0.5rem 0;
}

.blog-meta {
  display: flex;
  gap: 1rem;
  color: #888;
  font-size: 0.875rem;
}

.delete-btn {
  padding: 0.5rem 1rem;
  background-color: transparent;
  border: 1px solid #ff4444;
  color: #ff4444;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.delete-btn:hover {
  background-color: #ff4444;
  color: #fff;
}

.empty {
  text-align: center;
  padding: 2rem;
  color: #666;
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