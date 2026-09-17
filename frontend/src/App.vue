<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <nav class="navbar">
      <div class="nav-content">
        <router-link to="/" class="logo">
          <span class="logo-icon">◆</span>
          <span class="logo-text">BLOG</span>
        </router-link>

        <div class="nav-links">
          <router-link to="/" class="nav-link">首页</router-link>
          <router-link to="/publish" v-if="isLoggedIn" class="nav-link">发布博客</router-link>
          <router-link to="/profile" v-if="isLoggedIn" class="nav-link">个人中心</router-link>
          <router-link to="/admin" v-if="isAdmin" class="nav-link admin-link">管理后台</router-link>
        </div>

        <div class="nav-user">
          <template v-if="isLoggedIn">
            <img :src="userStore.userInfo?.avatar" class="nav-avatar" alt="头像" />
            <span class="username">{{ userStore.userInfo?.username }}</span>
            <button class="btn-logout" @click="handleLogout">退出</button>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-link">登录</router-link>
            <router-link to="/register" class="btn-register">注册</router-link>
          </template>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>© 2026 黑黄博客 - 前后端分离项目</p>
    </footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => !!userStore.token)
const isAdmin = computed(() => userStore.userInfo?.is_superuser)

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #0a0a0a;
}

/* 导航栏 */
.navbar {
  background: linear-gradient(180deg, #1a1a1a 0%, #0d0d0d 100%);
  border-bottom: 2px solid #ffd700;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #ffd700;
  font-size: 1.5rem;
  font-weight: bold;
}

.logo-icon {
  color: #ffd700;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: #ffffff;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #000000;
  background-color: #ffd700;
}

.nav-link.admin-link {
  color: #ffd700;
  border: 1px solid #ffd700;
}

.nav-link.admin-link:hover,
.nav-link.admin-link.router-link-active {
  background-color: #ffd700;
  color: #000000;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  color: #ffd700;
}

.nav-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ffd700;
  cursor: pointer;
}

.btn-logout {
  background: transparent;
  border: 1px solid #ffd700;
  color: #ffd700;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-logout:hover {
  background-color: #ffd700;
  color: #000000;
}

.btn-register {
  background-color: #ffd700;
  color: #000000;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: bold;
  transition: all 0.3s;
}

.btn-register:hover {
  background-color: #ffed4e;
}

/* 主内容 */
.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

/* 页脚 */
.footer {
  background-color: #1a1a1a;
  border-top: 1px solid #333;
  text-align: center;
  padding: 1.5rem;
  color: #666;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>