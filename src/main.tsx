import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import './index.css';

// 添加全局错误处理
window.addEventListener('error', (event) => {
  console.error('全局错误:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('未处理的Promise拒绝:', event.reason);
});

const rootElement = document.getElementById('root');

if (!rootElement) {
  throw new Error('找不到 root 元素，请检查 index.html');
}

try {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </React.StrictMode>
  );
  console.log('✅ 应用初始化成功');
} catch (error) {
  console.error('❌ 应用初始化失败:', error);
  
  // 显示错误信息
  rootElement.innerHTML = `
    <div style="display: flex; align-items: center; justify-content: center; height: 100vh; background: #f3f4f6; font-family: system-ui;">
      <div style="background: white; padding: 2rem; border-radius: 0.5rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px;">
        <h1 style="color: #dc2626; font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem;">应用初始化失败</h1>
        <p style="color: #374151; margin-bottom: 0.5rem;">错误信息：</p>
        <pre style="background: #f9fafb; padding: 1rem; border-radius: 0.25rem; overflow-x: auto; color: #dc2626; font-size: 0.875rem;">${error instanceof Error ? error.message : String(error)}</pre>
        <p style="color: #6b7280; font-size: 0.875rem; margin-top: 1rem;">请打开浏览器控制台（F12）查看详细错误信息</p>
        <button onclick="window.location.reload()" style="margin-top: 1rem; background: #0284c7; color: white; padding: 0.5rem 1rem; border-radius: 0.25rem; border: none; cursor: pointer;">
          刷新页面
        </button>
      </div>
    </div>
  `;
}
