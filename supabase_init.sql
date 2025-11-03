-- Supabase 数据库初始化脚本

-- 创建 travel_plans 表
CREATE TABLE IF NOT EXISTS travel_plans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  title TEXT NOT NULL,
  destination TEXT NOT NULL,
  start_date DATE,
  end_date DATE,
  budget DECIMAL,
  travelers INTEGER,
  preferences JSONB DEFAULT '{}',
  itinerary JSONB DEFAULT '[]',
  location JSONB, -- 存储 {lng: number, lat: number}
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建 budget_records 表
CREATE TABLE IF NOT EXISTS budget_records (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  plan_id UUID REFERENCES travel_plans(id) ON DELETE CASCADE NOT NULL,
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  category TEXT NOT NULL,
  amount DECIMAL NOT NULL,
  description TEXT,
  date DATE DEFAULT CURRENT_DATE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 创建 api_configs 表（可选，也可以使用localStorage）
CREATE TABLE IF NOT EXISTS api_configs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  ai_api_url TEXT,
  ai_api_key TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  UNIQUE(user_id)
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_travel_plans_user_id ON travel_plans(user_id);
CREATE INDEX IF NOT EXISTS idx_travel_plans_created_at ON travel_plans(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_budget_records_plan_id ON budget_records(plan_id);
CREATE INDEX IF NOT EXISTS idx_budget_records_user_id ON budget_records(user_id);

-- 启用 Row Level Security (RLS)
ALTER TABLE travel_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget_records ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_configs ENABLE ROW LEVEL SECURITY;

-- 创建策略：用户可以查看自己的数据
CREATE POLICY "Users can view own travel plans"
  ON travel_plans FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own travel plans"
  ON travel_plans FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own travel plans"
  ON travel_plans FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own travel plans"
  ON travel_plans FOR DELETE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own budget records"
  ON budget_records FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own budget records"
  ON budget_records FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own budget records"
  ON budget_records FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own budget records"
  ON budget_records FOR DELETE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can view own api configs"
  ON api_configs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own api configs"
  ON api_configs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own api configs"
  ON api_configs FOR UPDATE
  USING (auth.uid() = user_id);

-- 创建更新 updated_at 的触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 为 travel_plans 表创建触发器
CREATE TRIGGER update_travel_plans_updated_at
  BEFORE UPDATE ON travel_plans
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- 为 api_configs 表创建触发器
CREATE TRIGGER update_api_configs_updated_at
  BEFORE UPDATE ON api_configs
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

