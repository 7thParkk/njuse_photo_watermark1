import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { useConfigStore } from '../stores/configStore';
import { validateApiConfig } from '../utils/config';

export default function Settings() {
  const navigate = useNavigate();
  const { user, signOut } = useAuthStore();
  const { config, updateConfig } = useConfigStore();
  
  const [xunfeiAppId, setXunfeiAppId] = useState(config.xunfei?.appId || '');
  const [xunfeiApiSecret, setXunfeiApiSecret] = useState(config.xunfei?.apiSecret || '');
  const [xunfeiApiKey, setXunfeiApiKey] = useState(config.xunfei?.apiKey || '');
  
  const [amapWebKey, setAmapWebKey] = useState(config.amap?.webServiceKey || '');
  const [amapJsKey, setAmapJsKey] = useState(config.amap?.jsApiKey || '');
  const [amapJsSecret, setAmapJsSecret] = useState(config.amap?.jsApiSecret || '');
  
  const [aiBaseUrl, setAiBaseUrl] = useState(config.ai?.baseUrl || '');
  const [aiApiKey, setAiApiKey] = useState(config.ai?.apiKey || '');
  
  const [supabaseUrl, setSupabaseUrl] = useState(config.supabase?.url || '');
  const [supabaseKey, setSupabaseKey] = useState(config.supabase?.anonKey || '');
  
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleSave = () => {
    updateConfig({
      xunfei: {
        appId: xunfeiAppId,
        apiSecret: xunfeiApiSecret,
        apiKey: xunfeiApiKey,
      },
      amap: {
        webServiceKey: amapWebKey,
        jsApiKey: amapJsKey,
        jsApiSecret: amapJsSecret,
      },
      ai: {
        baseUrl: aiBaseUrl,
        apiKey: aiApiKey,
      },
      supabase: {
        url: supabaseUrl,
        anonKey: supabaseKey,
      },
    });

    const validation = validateApiConfig({
      xunfei: { appId: xunfeiAppId, apiSecret: xunfeiApiSecret, apiKey: xunfeiApiKey },
      amap: { webServiceKey: amapWebKey, jsApiKey: amapJsKey, jsApiSecret: amapJsSecret },
      ai: { baseUrl: aiBaseUrl, apiKey: aiApiKey },
      supabase: { url: supabaseUrl, anonKey: supabaseKey },
    });

    if (validation.valid) {
      setMessage({ type: 'success', text: '配置保存成功！' });
      setTimeout(() => {
        setMessage(null);
        window.location.reload(); // 重新加载以应用新配置
      }, 1500);
    } else {
      setMessage({ type: 'error', text: `配置不完整：${validation.missing.join('、')}` });
    }
  };

  const handleLogout = async () => {
    await signOut();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-primary-700">AI 旅行规划师</h1>
            </div>
            <div className="flex items-center space-x-4">
              {user ? (
                <>
                  <button
                    onClick={() => navigate('/')}
                    className="text-gray-600 hover:text-gray-900"
                  >
                    首页
                  </button>
                  <button
                    onClick={() => navigate('/planner')}
                    className="text-gray-600 hover:text-gray-900"
                  >
                    规划行程
                  </button>
                  <button
                    onClick={handleLogout}
                    className="text-red-600 hover:text-red-700"
                  >
                    退出登录
                  </button>
                </>
              ) : (
                <>
                  <button
                    onClick={() => navigate('/login')}
                    className="text-gray-600 hover:text-gray-900"
                  >
                    登录
                  </button>
                  <button
                    onClick={() => navigate('/register')}
                    className="text-gray-600 hover:text-gray-900"
                  >
                    注册
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h2 className="text-2xl font-bold mb-6">API 配置</h2>
        
        {message && (
          <div className={`mb-4 p-4 rounded ${
            message.type === 'success' 
              ? 'bg-green-50 text-green-700 border border-green-200' 
              : 'bg-red-50 text-red-700 border border-red-200'
          }`}>
            {message.text}
          </div>
        )}

        <div className="space-y-6">
          {/* 科大讯飞配置 */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-4">科大讯飞语音识别API</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">APPID</label>
                <input
                  type="text"
                  value={xunfeiAppId}
                  onChange={(e) => setXunfeiAppId(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">APISecret</label>
                <input
                  type="text"
                  value={xunfeiApiSecret}
                  onChange={(e) => setXunfeiApiSecret(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">APIKey</label>
                <input
                  type="text"
                  value={xunfeiApiKey}
                  onChange={(e) => setXunfeiApiKey(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>

          {/* 高德地图配置 */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-4">高德地图API</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Web服务Key</label>
                <input
                  type="text"
                  value={amapWebKey}
                  onChange={(e) => setAmapWebKey(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">JavaScript API Key</label>
                <input
                  type="text"
                  value={amapJsKey}
                  onChange={(e) => setAmapJsKey(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">JavaScript API Secret</label>
                <input
                  type="text"
                  value={amapJsSecret}
                  onChange={(e) => setAmapJsSecret(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>

          {/* 大语言模型配置 */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-4">大语言模型API</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Base URL</label>
                <input
                  type="text"
                  value={aiBaseUrl}
                  onChange={(e) => setAiBaseUrl(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">API Key</label>
                <input
                  type="text"
                  value={aiApiKey}
                  onChange={(e) => setAiApiKey(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>

          {/* Supabase配置 */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold mb-4">Supabase配置</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Project URL</label>
                <input
                  type="text"
                  value={supabaseUrl}
                  onChange={(e) => setSupabaseUrl(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Anon Key</label>
                <input
                  type="text"
                  value={supabaseKey}
                  onChange={(e) => setSupabaseKey(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                />
              </div>
            </div>
          </div>

          <button
            onClick={handleSave}
            className="w-full bg-primary-600 text-white py-3 px-4 rounded-lg hover:bg-primary-700 transition-colors"
          >
            保存配置
          </button>
        </div>
      </div>
    </div>
  );
}

