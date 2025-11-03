import { useState, useEffect } from 'react';
import { supabase, TABLES } from '../../services/supabase';
import { BudgetRecord } from '../../types';
import { useAuthStore } from '../../stores/authStore';

interface BudgetManagerProps {
  planId: string;
}

export default function BudgetManager({ planId }: BudgetManagerProps) {
  const { user } = useAuthStore();
  const [records, setRecords] = useState<BudgetRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');

  useEffect(() => {
    if (planId) {
      loadRecords();
    }
  }, [planId]);

  const loadRecords = async () => {
    try {
      const { data, error } = await supabase
        .from(TABLES.BUDGET_RECORDS)
        .select('*')
        .eq('plan_id', planId)
        .order('created_at', { ascending: false });

      if (error) throw error;
      setRecords(data || []);
    } catch (error) {
      console.error('加载预算记录失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || !category || !amount) return;

    try {
      const { error } = await supabase
        .from(TABLES.BUDGET_RECORDS)
        .insert({
          plan_id: planId,
          user_id: user.id,
          category,
          amount: parseFloat(amount),
          description: description || null,
        });

      if (error) throw error;
      
      setCategory('');
      setAmount('');
      setDescription('');
      setShowForm(false);
      loadRecords();
    } catch (error) {
      console.error('添加预算记录失败:', error);
      alert('添加失败');
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除这条记录吗？')) return;

    try {
      const { error } = await supabase
        .from(TABLES.BUDGET_RECORDS)
        .delete()
        .eq('id', id);

      if (error) throw error;
      loadRecords();
    } catch (error) {
      console.error('删除失败:', error);
      alert('删除失败');
    }
  };

  const totalAmount = records.reduce((sum, record) => sum + Number(record.amount), 0);
  const categories = ['交通', '住宿', '餐饮', '景点', '购物', '其他'];

  if (loading) {
    return <div className="text-center py-4">加载中...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">费用记录</h3>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 text-sm"
        >
          {showForm ? '取消' : '添加记录'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="bg-gray-50 p-4 rounded-lg space-y-3">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">类别</label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="">请选择</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">金额</label>
            <input
              type="number"
              step="0.01"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              placeholder="0.00"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <input
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              placeholder="可选"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-primary-600 text-white py-2 rounded-lg hover:bg-primary-700"
          >
            保存
          </button>
        </form>
      )}

      <div className="bg-white rounded-lg p-4">
        <div className="flex justify-between items-center mb-4">
          <span className="font-medium">总支出</span>
          <span className="text-xl font-bold text-red-600">¥{totalAmount.toFixed(2)}</span>
        </div>

        {records.length === 0 ? (
          <div className="text-center text-gray-500 py-4">暂无记录</div>
        ) : (
          <div className="space-y-2">
            {records.map((record) => (
              <div
                key={record.id}
                className="flex justify-between items-center p-2 hover:bg-gray-50 rounded"
              >
                <div className="flex-1">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">{record.category}</span>
                    <span className="text-gray-500 text-sm">
                      {new Date(record.date).toLocaleDateString()}
                    </span>
                  </div>
                  {record.description && (
                    <div className="text-sm text-gray-600">{record.description}</div>
                  )}
                </div>
                <div className="flex items-center space-x-3">
                  <span className="font-medium">¥{Number(record.amount).toFixed(2)}</span>
                  <button
                    onClick={() => handleDelete(record.id)}
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

