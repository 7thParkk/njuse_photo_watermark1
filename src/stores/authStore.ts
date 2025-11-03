import { create } from 'zustand';
import { User } from '@supabase/supabase-js';
import { supabase } from '../services/supabase';

interface AuthState {
  user: User | null;
  loading: boolean;
  checkAuth: () => Promise<void>;
  signIn: (email: string, password: string) => Promise<{ error: any }>;
  signUp: (email: string, password: string) => Promise<{ error: any }>;
  signOut: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: true,
  
  checkAuth: async () => {
    try {
      // 检查是否有有效的 Supabase 配置
      const config = JSON.parse(localStorage.getItem('api_config') || '{}');
      const hasConfig = config.supabase?.url && config.supabase?.anonKey;
      
      if (!hasConfig) {
        console.warn('Supabase未配置，跳过认证检查');
        set({ user: null, loading: false });
        return;
      }

      // 添加超时保护
      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('认证检查超时')), 3000);
      });

      const sessionPromise = supabase.auth.getSession();
      
      const result = await Promise.race([
        sessionPromise,
        timeoutPromise,
      ]) as any;
      
      if (result.error) {
        console.warn('获取会话失败:', result.error.message);
        set({ user: null, loading: false });
        return;
      }
      
      set({ user: result.data?.session?.user ?? null, loading: false });
      
      // 监听认证状态变化
      supabase.auth.onAuthStateChange((_event, session) => {
        set({ user: session?.user ?? null });
      });
    } catch (error: any) {
      console.error('检查认证状态失败:', error);
      // 即使出错也设置 loading 为 false，让用户可以访问登录页面
      set({ user: null, loading: false });
    }
  },
  
  signIn: async (email: string, password: string) => {
    // 检查 Supabase 配置
    const config = JSON.parse(localStorage.getItem('api_config') || '{}');
    const hasConfig = config.supabase?.url && config.supabase?.anonKey;
    
    if (!hasConfig) {
      return { 
        error: { 
          message: 'Supabase未配置，请前往设置页面配置Supabase信息' 
        } 
      };
    }

    try {
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });
      
      if (!error) {
        const { data: { session } } = await supabase.auth.getSession();
        set({ user: session?.user ?? null });
      }
      
      return { error };
    } catch (err: any) {
      return { 
        error: { 
          message: err.message || '登录失败，请检查网络连接或Supabase配置' 
        } 
      };
    }
  },
  
  signUp: async (email: string, password: string) => {
    // 检查 Supabase 配置
    const config = JSON.parse(localStorage.getItem('api_config') || '{}');
    const hasConfig = config.supabase?.url && config.supabase?.anonKey;
    
    if (!hasConfig) {
      return { 
        error: { 
          message: 'Supabase未配置，请前往设置页面配置Supabase信息' 
        } 
      };
    }

    try {
      const { error } = await supabase.auth.signUp({
        email,
        password,
      });
      
      return { error };
    } catch (err: any) {
      return { 
        error: { 
          message: err.message || '注册失败，请检查网络连接或Supabase配置' 
        } 
      };
    }
  },
  
  signOut: async () => {
    await supabase.auth.signOut();
    set({ user: null });
  },
}));

