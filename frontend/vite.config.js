import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    // ⬇️ 关键：支持 SPA history 模式刷新不跳 Django
    historyApiFallback: true,
    proxy: {
      // blog 模块
      '/blogs': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/categories': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      // auth 模块
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      // ⬇️ admin API 加前缀避免和前端路由 /admin-panel 冲突
      '/admin_api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/admin_api/, '/admin')
      },
      // 媒体文件
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})