import { describe, it, expect } from 'vitest';
import { MapService, AIService } from '../src/services/api';
import { loadApiConfig, validateApiConfig } from '../src/utils/config';

// 单元测试示例
// 注意：需要安装 vitest: npm install -D vitest

describe('API配置管理', () => {
  it('应该能够加载和保存配置', () => {
    const config = {
      xunfei: {
        appId: 'test',
        apiSecret: 'test',
        apiKey: 'test',
      },
    };
    
    // 测试保存和加载
    localStorage.setItem('api_config', JSON.stringify(config));
    const loaded = loadApiConfig();
    expect(loaded.xunfei?.appId).toBe('test');
  });

  it('应该能够验证配置完整性', () => {
    const completeConfig = {
      xunfei: { appId: 'test', apiSecret: 'test', apiKey: 'test' },
      amap: { webServiceKey: 'test', jsApiKey: 'test', jsApiSecret: 'test' },
      ai: { baseUrl: 'test', apiKey: 'test' },
      supabase: { url: 'test', anonKey: 'test' },
    };
    
    const incompleteConfig = {
      xunfei: { appId: 'test', apiSecret: 'test', apiKey: 'test' },
    };
    
    expect(validateApiConfig(completeConfig).valid).toBe(true);
    expect(validateApiConfig(incompleteConfig).valid).toBe(false);
  });
});

describe('地图服务', () => {
  it('应该能够初始化地图服务', () => {
    localStorage.setItem('api_config', JSON.stringify({
      amap: {
        webServiceKey: 'test',
        jsApiKey: 'test',
        jsApiSecret: 'test',
      },
    }));
    
    const mapService = new MapService();
    expect(mapService).toBeDefined();
  });
});

describe('AI服务', () => {
  it('应该能够初始化AI服务', () => {
    localStorage.setItem('api_config', JSON.stringify({
      ai: {
        baseUrl: 'test',
        apiKey: 'test',
      },
    }));
    
    const aiService = new AIService();
    expect(aiService).toBeDefined();
  });
});

// 注意：实际API调用测试需要真实的API密钥
// 建议在集成测试中进行

