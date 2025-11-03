// 类型定义
export interface User {
  id: string;
  email: string;
  created_at?: string;
}

export interface TravelPlan {
  id: string;
  user_id: string;
  title: string;
  destination: string;
  start_date: string | null;
  end_date: string | null;
  budget: number | null;
  travelers: number | null;
  preferences: Record<string, any>;
  itinerary: ItineraryDay[];
  location?: { lng: number; lat: number } | null;
  created_at: string;
  updated_at: string;
}

export interface ItineraryDay {
  day: number;
  date: string;
  activities: Activity[];
}

export interface Activity {
  type: 'transport' | 'attraction' | 'restaurant' | 'accommodation' | 'other';
  name: string;
  description?: string;
  location?: {
    name: string;
    lng: number;
    lat: number;
  };
  time?: string;
  duration?: string;
  cost?: number;
}

export interface BudgetRecord {
  id: string;
  plan_id: string;
  user_id: string;
  category: string;
  amount: number;
  description?: string;
  date: string;
  created_at: string;
}

export interface ApiConfig {
  xunfei?: {
    appId: string;
    apiSecret: string;
    apiKey: string;
  };
  amap?: {
    webServiceKey: string;
    jsApiKey: string;
    jsApiSecret: string;
  };
  ai?: {
    baseUrl: string;
    apiKey: string;
  };
  supabase?: {
    url: string;
    anonKey: string;
  };
}

