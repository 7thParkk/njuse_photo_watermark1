import { Routes, Route, Navigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { useAuthStore } from './stores/authStore';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Planner from './pages/Planner';
import Settings from './pages/Settings';

function App() {
  const { user, loading, checkAuth } = useAuthStore();
  const [initError, setInitError] = useState<string | null>(null);

  useEffect(() => {
    // 添加超时保护，避免无限加载
    const timeoutId = setTimeout(() => {
      if (loading) {
        console.warn('认证检查超时，强制显示登录页面');
        setInitError('认证检查超时，请检查网络连接或Supabase配置');
      }
    }, 5000);

    // 添加错误边界
    const init = async () => {
      try {
        await checkAuth();
      } catch (err: any) {
        console.error('初始化失败:', err);
        setInitError(err.message || '初始化失败');
      } finally {
        clearTimeout(timeoutId);
      }
    };
    init();
  }, [checkAuth, loading]);

  // 如果有初始化错误，显示错误信息
  if (initError) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md">
          <h1 className="text-2xl font-bold text-red-600 mb-4">初始化错误</h1>
          <p className="text-gray-700 mb-4">{initError}</p>
          <p className="text-sm text-gray-500 mb-4">
            请检查浏览器控制台（F12）获取更多信息
          </p>
          <div className="space-y-2">
            <button
              onClick={() => {
                setInitError(null);
                checkAuth();
              }}
              className="w-full bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
            >
              重试
            </button>
            <button
              onClick={() => window.location.reload()}
              className="w-full bg-gray-200 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-300"
            >
              刷新页面
            </button>
          </div>
        </div>
      </div>
    );
  }

  // 如果还在加载，显示加载状态，但设置超时后强制显示登录页面
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="text-lg text-gray-600 mb-2">加载中...</div>
          <div className="text-sm text-gray-400">正在初始化应用</div>
          <div className="mt-4">
            <button
              onClick={() => {
                // 强制跳过加载，直接显示登录页面
                useAuthStore.setState({ loading: false, user: null });
              }}
              className="text-sm text-primary-600 hover:text-primary-700 underline"
            >
              跳过加载
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      {/* 设置页面允许未登录访问，用于配置API */}
      <Route path="/settings" element={<Settings />} />
      <Route
        path="/planner"
        element={user ? <Planner /> : <Navigate to="/login" />}
      />
      <Route
        path="/"
        element={user ? <Home /> : <Navigate to="/login" />}
      />
    </Routes>
  );
}

export default App;
