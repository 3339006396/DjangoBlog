<template>
  <div class="blog-detail-container">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error-msg">{{ error }}</div>
    <template v-else-if="detail">
      <!-- 博客内容 -->
      <article class="blog-article">
        <header class="blog-header">
          <h1 class="blog-title">{{ detail.blog.title }}</h1>
          <div class="blog-meta">
            <div class="author-info">
              <img :src="detail.blog.author_avatar" class="author-avatar" alt="头像" />
              <span class="author">{{ detail.blog.author_username }}</span>
            </div>
            <span class="time">🕐 {{ formatTime(detail.blog.pub_time) }}</span>
            <span class="category">🏷️ {{ detail.blog.category_name }}</span>
          </div>
        </header>

        <div class="blog-content">
          {{ detail.blog.content }}
        </div>
      </article>

      <!-- 评论区 -->
      <section class="comment-section">
        <h2 class="section-title">
          评论 ({{ detail.comments?.length || 0 }})
        </h2>

        <!-- 发表评论 -->
        <div v-if="isLoggedIn" class="comment-form">
          <textarea
            v-model="newComment"
            placeholder="发表你的评论..."
            rows="3"
            class="comment-textarea"
          ></textarea>
          <button
            @click="submitComment"
            :disabled="!newComment.trim() || submitting"
            class="submit-comment-btn"
          >
            {{ submitting ? '提交中...' : '发表评论' }}
          </button>
        </div>
        <div v-else class="login-tip">
          <router-link to="/login" class="link">登录</router-link>后即可发表评论
        </div>

        <!-- 评论列表 -->
        <div class="comment-list">
          <div
            v-for="comment in detail.comments"
            :key="comment.id"
            class="comment-item"
          >
            <div class="comment-header">
              <span class="comment-author">
                <img :src="comment.author_avatar" class="comment-avatar" alt="" />
                {{ comment.author_username }}
              </span>
              <span class="comment-time">{{ formatTime(comment.create_time) }}</span>
            </div>
            <p class="comment-content">{{ comment.comment }}</p>
          </div>

          <div v-if="!detail.comments?.length" class="empty-comments">
            暂无评论，来发表第一条评论吧！
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import api from '../api'

const route = useRoute()
const userStore = useUserStore()

const detail = ref(null)
const loading = ref(true)
const error = ref('')
const newComment = ref('')
const submitting = ref(false)

const isLoggedIn = computed(() => !!userStore.token)

async function fetchDetail() {
  loading.value = true
  error.value = ''

  try {
    const response = await api.get(`/blogs/${route.params.id}/`)
    detail.value = response.data
    console.log('博客详情返回:', response)
    console.log('author_avatar:', response.blog?.author_avatar)
  } catch (err) {
    error.value = err.response?.data?.msg || '获取博客详情失败'
  } finally {
    loading.value = false
  }
}

async function submitComment() {
  submitting.value = true

  try {
    await api.post(`/blogs/${route.params.id}/comment/`, {
      comment: newComment.value
    })
    newComment.value = ''
    fetchDetail()
  } catch (err) {
    error.value = err.response?.data?.msg || '评论失败'
  } finally {
    submitting.value = false
  }
}

function formatTime(timeStr) {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

onMounted(fetchDetail)
</script>

<style scoped>
.blog-detail-container {
  max-width: 800px;
  margin: 0 auto;
}

.loading, .error-msg {
  text-align: center;
  padding: 3rem;
  color: #888;
}

.error-msg {
  color: #ff4444;
}

/* 博客正文 */
.blog-article {
  background: linear-gradient(135deg, #1a1a1a 0%, #0d0d0d 100%);
  border: 1px solid #333;
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.blog-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #333;
}

.blog-title {
  font-size: 2rem;
  color: #fff;
  margin-bottom: 1rem;
}

.blog-meta {
  display: flex;
  gap: 1.5rem;
  color: #888;
  font-size: 0.875rem;
  align-items: center;
}

.author-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.author-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ffd700;
}

.blog-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #ddd;
  white-space: pre-wrap;
}

/* 评论区 */
.comment-section {
  background: #111;
  border: 1px solid #333;
  border-radius: 12px;
  padding: 2rem;
}

.section-title {
  color: #ffd700;
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.comment-form {
  margin-bottom: 2rem;
}

.comment-textarea {
  width: 100%;
  padding: 1rem;
  background-color: #1a1a1a;
  border: 2px solid #333;
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  resize: vertical;
  outline: none;
  margin-bottom: 1rem;
}

.comment-textarea:focus {
  border-color: #ffd700;
}

.submit-comment-btn {
  padding: 0.75rem 2rem;
  background-color: #ffd700;
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-comment-btn:hover:not(:disabled) {
  background-color: #ffed4e;
}

.submit-comment-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.login-tip {
  text-align: center;
  padding: 1rem;
  color: #888;
  margin-bottom: 2rem;
}

.link {
  color: #ffd700;
  text-decoration: none;
  font-weight: bold;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.comment-item {
  background-color: #1a1a1a;
  border-radius: 8px;
  padding: 1rem;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.comment-author {
  color: #ffd700;
  font-weight: bold;
}

.comment-avatar {
  display: inline-block;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ffd700;
  margin-right: 0.5rem;
  vertical-align: middle;
}

.avatar {
  display: inline-block;
  width: 24px;
  height: 24px;
  background-color: #ffd700;
  color: #000;
  border-radius: 50%;
  text-align: center;
  line-height: 24px;
  margin-right: 0.5rem;
  font-size: 0.75rem;
}

.comment-time {
  color: #666;
  font-size: 0.75rem;
}

.comment-content {
  color: #ddd;
  line-height: 1.6;
}

.empty-comments {
  text-align: center;
  padding: 2rem;
  color: #666;
}
</style>