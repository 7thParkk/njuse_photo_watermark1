import { createClient, SupabaseClient } from '@supabase/supabase-js';
import { loadApiConfig } from '../utils/config';

// 动态获取 Supabase 配置
function getSupabaseConfig() {
  const config = loadApiConfig();
  return {
    url: config.supabase?.url || import.meta.env.VITE_SUPABASE_URL || '',
    anonKey: config.supabase?.anonKey || import.meta.env.VITE_SUPABASE_ANON_KEY || '',
  };
}

// 创建 Supabase 客户端的函数
function createSupabaseClient(): SupabaseClient {
  const { url, anonKey } = getSupabaseConfig();
  
  if (url && anonKey && url !== 'https://placeholder.supabase.co') {
    return createClient(
      url,
      anonKey,
      {
        auth: {
          persistSession: true,
          autoRefreshToken: true,
        },
      }
    );
  }
  
  // 返回一个虚拟客户端，但会在使用时检查配置
  return createClient(
    'https://placeholder.supabase.co',
    'placeholder-key',
    {
      auth: {
        persistSession: false,
        autoRefreshToken: false,
      },
    }
  );
}

// 检查 Supabase 是否已配置
export function isSupabaseConfigured(): boolean {
  const { url, anonKey } = getSupabaseConfig();
  return !!(url && anonKey && url !== 'https://placeholder.supabase.co');
}

// 动态创建客户端（每次调用时检查配置）
let supabaseInstance: SupabaseClient | null = null;

export function getSupabaseClient(): SupabaseClient {
  // 如果配置改变，重新创建客户端
  if (!supabaseInstance || !isSupabaseConfigured()) {
    supabaseInstance = createSupabaseClient();
  }
  return supabaseInstance;
}

// 数据库表名
export const TABLES = {
  TRAVEL_PLANS: 'travel_plans',
  BUDGET_RECORDS: 'budget_records',
  API_CONFIGS: 'api_configs',
} as const;

// 导出客户端（保持向后兼容）
export const supabase = getSupabaseClient();

