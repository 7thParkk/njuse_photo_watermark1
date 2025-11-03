import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';
import { supabase, TABLES } from '../services/supabase';
import { TravelPlan } from '../types';

export default function Home() {
  const navigate = useNavigate();
  const { user, signOut } = useAuthStore();
  const [plans, setPlans] = useState<TravelPlan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPlans();
  }, [user]);

  const loadPlans = async () => {
    if (!user) return;
    
    try {
      const { data, error } = await supabase
        .from(TABLES.TRAVEL_PLANS)
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false });

      if (error) throw error;
      setPlans(data || []);
    } catch (error) {
      console.error('加载行程失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除这个行程吗？')) return;

    try {
      const { error } = await supabase
        .from(TABLES.TRAVEL_PLANS)
        .delete()
        .eq('id', id);

      if (error) throw error;
      loadPlans();
    } catch (error) {
      console.error('删除失败:', error);
      alert('删除失败');
    }
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
              {user && (
                <span className="text-sm text-gray-600">
                  当前账号：{user.email}
                </span>
              )}
              <button
                onClick={() => navigate('/planner')}
                className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
              >
                创建新行程
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

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h2 className="text-2xl font-bold mb-6">我的行程</h2>

        {loading ? (
          <div className="text-center py-12">加载中...</div>
        ) : plans.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">还没有行程计划</p>
            <button
              onClick={() => navigate('/planner')}
              className="bg-primary-600 text-white px-6 py-3 rounded-lg hover:bg-primary-700"
            >
              创建第一个行程
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {plans.map((plan) => (
              <div
                key={plan.id}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => navigate(`/planner?id=${plan.id}`)}
              >
                <h3 className="text-xl font-semibold mb-2">{plan.title}</h3>
                <p className="text-gray-600 mb-4">目的地：{plan.destination}</p>
                {plan.start_date && plan.end_date && (
                  <p className="text-sm text-gray-500 mb-2">
                    {plan.start_date} 至 {plan.end_date}
                  </p>
                )}
                {plan.budget && (
                  <p className="text-sm text-gray-500 mb-4">预算：¥{plan.budget}</p>
                )}
                <div className="flex justify-between items-center mt-4">
                  <span className="text-xs text-gray-400">
                    {new Date(plan.created_at).toLocaleDateString()}
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(plan.id);
                    }}
                    className="text-red-600 hover:text-red-700 text-sm"
                  >
                    删除
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

