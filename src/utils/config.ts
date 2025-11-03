// API配置类型定义
export interface ApiConfig {
  // 科大讯飞语音识别
  xunfei?: {
    appId: string;
    apiSecret: string;
    apiKey: string;
  };
  
  // 高德地图
  amap?: {
    webServiceKey: string;
    jsApiKey: string;
    jsApiSecret: string;
  };
  
  // 大语言模型
  ai?: {
    baseUrl: string;
    apiKey: string;
  };
  
  // Supabase
  supabase?: {
    url: string;
    anonKey: string;
  };
}

// 从localStorage加载配置
export function loadApiConfig(): ApiConfig {
  const configStr = localStorage.getItem('api_config');
  if (!configStr) {
    return {};
  }
  
  try {
    return JSON.parse(configStr);
  } catch {
    return {};
  }
}

// 保存配置到localStorage
export function saveApiConfig(config: ApiConfig): void {
  localStorage.setItem('api_config', JSON.stringify(config));
}

// 获取配置值
export function getApiConfig<K extends keyof ApiConfig>(
  key: K
): ApiConfig[K] | undefined {
  const config = loadApiConfig();
  return config[key];
}

// 更新配置值
export function updateApiConfig<K extends keyof ApiConfig>(
  key: K,
  value: ApiConfig[K]
): void {
  const config = loadApiConfig();
  config[key] = value;
  saveApiConfig(config);
}

// 验证配置是否完整
export function validateApiConfig(config: ApiConfig): {
  valid: boolean;
  missing: string[];
} {
  const missing: string[] = [];
  
  if (!config.xunfei?.appId || !config.xunfei?.apiSecret || !config.xunfei?.apiKey) {
    missing.push('科大讯飞语音识别API');
  }
  
  if (!config.amap?.webServiceKey || !config.amap?.jsApiKey) {
    missing.push('高德地图API');
  }
  
  if (!config.ai?.baseUrl || !config.ai?.apiKey) {
    missing.push('大语言模型API');
  }
  
  if (!config.supabase?.url || !config.supabase?.anonKey) {
    missing.push('Supabase配置');
  }
  
  return {
    valid: missing.length === 0,
    missing
  };
}

