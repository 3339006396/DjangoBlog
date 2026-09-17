import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresGuest: true }
  },
  {
    path: '/blog/:id',
    name: 'BlogDetail',
    component: () => import('../views/BlogDetail.vue')
  },
  {
    path: '/publish',
    name: 'PublishBlog',
    component: () => import('../views/PublishBlog.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 需要登录的页面
  if (to.meta.requiresAuth && !userStore.token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  }
  // 需要管理员权限的页面
  else if (to.meta.requiresAdmin && !userStore.userInfo?.is_superuser) {
    next({ name: 'Home' })
  }
  // 已登录用户不能访问登录/注册页
  else if (to.meta.requiresGuest && userStore.token) {
    next({ name: 'Home' })
  }
  else {
    next()
  }
})

export default router