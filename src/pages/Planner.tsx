import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { usePlanStore } from '../stores/planStore';
import VoiceInput from '../components/VoiceInput/VoiceInput';
import MapComponent from '../components/Map/MapComponent';
import BudgetManager from '../components/BudgetManager/BudgetManager';
import { AIService, MapService } from '../services/api';
import { supabase, TABLES } from '../services/supabase';
import { TravelPlan, ItineraryDay } from '../types';

export default function Planner() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const planId = searchParams.get('id');
  const { user, signOut } = useAuthStore();
  const { currentPlan, setCurrentPlan } = usePlanStore();
  const [destination, setDestination] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [budget, setBudget] = useState('');
  const [travelers, setTravelers] = useState('');
  const [preferences, setPreferences] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (planId) {
      loadPlan(planId);
    }
  }, [planId]);

  const loadPlan = async (id: string) => {
    try {
      const { data, error } = await supabase
        .from(TABLES.TRAVEL_PLANS)
        .select('*')
        .eq('id', id)
        .single();

      if (error) throw error;
      if (data) {
        setCurrentPlan(data);
        setDestination(data.destination || '');
        setStartDate(data.start_date || '');
        setEndDate(data.end_date || '');
        setBudget(data.budget?.toString() || '');
        setTravelers(data.travelers?.toString() || '');
        setPreferences(data.preferences?.description || '');
      }
    } catch (error) {
      console.error('加载行程失败:', error);
    }
  };

  const handleVoiceInput = (text: string) => {
    // 语音输入时，尝试解析并填充到表单字段
    setPreferences(text);
  };

  const handleSubmit = async () => {
    if (!destination.trim()) {
      setError('请输入目的地');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // 构建需求描述
      const requirements = [
        `目的地：${destination}`,
        startDate && `出发日期：${startDate}`,
        endDate && `返回日期：${endDate}`,
        budget && `预算：${budget}元`,
        travelers && `人数：${travelers}人`,
        preferences && `偏好：${preferences}`,
      ].filter(Boolean).join('，');

      const aiService = new AIService();
      const planData = await aiService.generateTravelPlan(requirements);

      // 如果提供了目的地，获取地理坐标
      const mapService = new MapService();
      let location = null;
      if (destination) {
        location = await mapService.geocode(destination);
      }

      // 保存到数据库（包含位置信息）
      const plan: Partial<TravelPlan> = {
        user_id: user!.id,
        title: planData.title || `${destination}旅行计划`,
        destination: destination,
        start_date: startDate || planData.start_date || null,
        end_date: endDate || planData.end_date || null,
        budget: budget ? parseFloat(budget) : (planData.budget || null),
        travelers: travelers ? parseInt(travelers) : (planData.travelers || null),
        preferences: {
          description: preferences,
        },
        itinerary: planData.itinerary || [],
        location: location ? { lng: location.lng, lat: location.lat } : null,
      };

      let savedPlan;
      if (planId) {
        // 更新现有行程
        const { data, error } = await supabase
          .from(TABLES.TRAVEL_PLANS)
          .update(plan)
          .eq('id', planId)
          .select()
          .single();
        if (error) throw error;
        savedPlan = data;
      } else {
        // 创建新行程
        const { data, error } = await supabase
          .from(TABLES.TRAVEL_PLANS)
          .insert(plan)
          .select()
          .single();
        if (error) throw error;
        savedPlan = data;
      }

      setCurrentPlan(savedPlan);
      alert('行程规划完成！');
      navigate(`/planner?id=${savedPlan.id}`);
    } catch (error: any) {
      console.error('行程规划失败:', error);
      setError(error.message || '行程规划失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-primary-700">AI 旅行规划师</h1>
            </div>
            <div className="flex items-center space-x-4">
              {user && (
                <span className="text-sm text-gray-600">
                  {user.email}
                </span>
              )}
              <button
                onClick={() => navigate('/')}
                className="text-gray-600 hover:text-gray-900"
              >
                首页
              </button>
              <button
                onClick={() => navigate('/settings')}
                className="text-gray-600 hover:text-gray-900"
              >
                设置
              </button>
              <button
                onClick={signOut}
                className="text-red-600 hover:text-red-700"
              >
                退出
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex-1 flex">
        {/* 左侧输入区域 */}
        <div className="w-96 bg-white shadow-lg p-6 overflow-y-auto">
          <h2 className="text-xl font-bold mb-4">行程规划</h2>
          
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {currentPlan && (
            <div className="mb-4 p-4 bg-primary-50 rounded-lg">
              <h3 className="font-semibold mb-2">{currentPlan.title}</h3>
              <p className="text-sm text-gray-600">目的地：{currentPlan.destination}</p>
              {currentPlan.budget && (
                <p className="text-sm text-gray-600">预算：¥{currentPlan.budget}</p>
              )}
            </div>
          )}
          
          <form onSubmit={(e) => { e.preventDefault(); handleSubmit(); }} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                目的地 <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                value={destination}
                onChange={(e) => setDestination(e.target.value)}
                required
                placeholder="例如：日本、北京、上海"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  出发日期
                </label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  返回日期
                </label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  min={startDate}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  预算（元）
                </label>
                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  placeholder="例如：10000"
                  min="0"
                  step="0.01"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  人数
                </label>
                <input
                  type="number"
                  value={travelers}
                  onChange={(e) => setTravelers(e.target.value)}
                  placeholder="例如：2"
                  min="1"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                旅行偏好（语音或文字）
              </label>
              <VoiceInput onResult={handleVoiceInput} />
              <textarea
                value={preferences}
                onChange={(e) => setPreferences(e.target.value)}
                placeholder="例如：喜欢美食和动漫，带孩子，想要深度游"
                className="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg h-24 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            <button
              type="submit"
              disabled={loading || !destination.trim()}
              className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '规划中...' : planId ? '更新行程' : '开始规划'}
            </button>
          </form>

          {currentPlan?.itinerary && currentPlan.itinerary.length > 0 && (
            <div className="mt-6">
              <h3 className="font-semibold mb-3">行程安排</h3>
              <div className="space-y-3 max-h-64 overflow-y-auto">
                {currentPlan.itinerary.map((day: ItineraryDay, index: number) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-3">
                    <div className="font-medium text-primary-700 mb-2">
                      第{day.day}天 {day.date && `(${day.date})`}
                    </div>
                    <div className="space-y-1">
                      {day.activities.map((activity, actIndex) => (
                        <div key={actIndex} className="text-sm text-gray-600">
                          <span className="font-medium">{activity.time || ''}</span> {' '}
                          {activity.name}
                          {activity.cost && ` - ¥${activity.cost}`}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {currentPlan && (
            <div className="mt-6">
              <BudgetManager planId={currentPlan.id} />
            </div>
          )}
        </div>

        {/* 右侧地图区域 */}
        <div className="flex-1">
          <MapComponent 
            destination={currentPlan?.destination || destination || null}
            location={currentPlan?.location || null}
          />
        </div>
      </div>
    </div>
  );
}

