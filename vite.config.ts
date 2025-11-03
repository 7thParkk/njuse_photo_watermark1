import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: true,
    proxy: {
      '/api/ai': {
        target: 'https://maas-api.cn-huabei-1.xf-yun.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/ai/, '/v1'),
        secure: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})

