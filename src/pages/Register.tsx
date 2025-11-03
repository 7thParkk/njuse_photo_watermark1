import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { loadApiConfig } from '../utils/config';

export default function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showConfigHint, setShowConfigHint] = useState(false);
  const signUp = useAuthStore((state) => state.signUp);
  const navigate = useNavigate();

  useEffect(() => {
    // 检查 Supabase 配置
    const config = loadApiConfig();
    const hasConfig = config.supabase?.url && config.supabase?.anonKey;
    setShowConfigHint(!hasConfig);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('两次密码输入不一致');
      return;
    }

    if (password.length < 6) {
      setError('密码长度至少6位');
      return;
    }

    setLoading(true);
    const { error } = await signUp(email, password);
    
    if (error) {
      setError(error.message);
      setLoading(false);
    } else {
      setError('');
      alert('注册成功！请检查邮箱验证链接（如果有）');
      navigate('/login');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
      <div className="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6 text-primary-700">
          AI 旅行规划师
        </h1>
        <h2 className="text-xl font-semibold text-center mb-8 text-gray-700">
          注册
        </h2>
        
        {showConfigHint && (
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded mb-4">
            <p className="text-sm mb-2">
              <strong>提示：</strong>使用注册功能需要先配置 Supabase。
            </p>
            <Link 
              to="/settings" 
              className="text-primary-600 hover:text-primary-700 font-medium underline text-sm"
            >
              前往设置页面配置 →
            </Link>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              邮箱
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="请输入邮箱"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              密码
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="至少6位密码"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              确认密码
            </label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              placeholder="再次输入密码"
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? '注册中...' : '注册'}
          </button>
        </form>
        
        <p className="mt-6 text-center text-sm text-gray-600">
          已有账号？{' '}
          <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
            立即登录
          </Link>
        </p>
      </div>
    </div>
  );
}

