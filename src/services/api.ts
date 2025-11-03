import axios from 'axios';
import CryptoJS from 'crypto-js';
import { getApiConfig } from '../utils/config';

// 科大讯飞语音识别服务
export class VoiceService {
  private config: ReturnType<typeof getApiConfig<'xunfei'>>;

  constructor() {
    this.config = getApiConfig('xunfei');
  }


  // 识别语音（简化版本，实际需要使用WebSocket流式传输）
  async recognize(audioBlob: Blob): Promise<string> {
    if (!this.config) {
      throw new Error('请先配置科大讯飞API');
    }

    // 注意：完整的科大讯飞语音识别需要使用WebSocket流式传输
    // 这里提供一个基础实现框架
    // 实际使用时需要处理音频格式转换（PCM 16bit 16kHz）和流式传输
    
    return new Promise((_resolve, reject) => {
      // 由于浏览器端WebSocket实现复杂，这里提供一个简化的实现
      // 实际项目中建议使用后端服务来处理语音识别
      
      const reader = new FileReader();
      reader.onload = async () => {
        try {
          // 简化实现：直接提示用户使用文字输入
          // 完整实现需要：
          // 1. 将音频转换为PCM格式（16bit, 16kHz）
          // 2. 建立WebSocket连接
          // 3. 分片发送音频数据
          // 4. 接收并解析识别结果
          
          console.warn('完整的语音识别功能需要后端服务支持');
          reject(new Error('语音识别功能需要后端服务支持，请使用文字输入'));
        } catch (error) {
          reject(error);
        }
      };
      reader.onerror = reject;
      reader.readAsArrayBuffer(audioBlob);
    });
  }
}

// 高德地图服务
export class MapService {
  private config: ReturnType<typeof getApiConfig<'amap'>>;

  constructor() {
    this.config = getApiConfig('amap');
  }

  // 搜索地点
  async searchPlace(keyword: string): Promise<any[]> {
    if (!this.config?.webServiceKey) {
      throw new Error('高德地图API配置未设置');
    }

    try {
      const response = await axios.get(
        'https://restapi.amap.com/v3/place/text',
        {
          params: {
            key: this.config.webServiceKey,
            keywords: keyword,
            output: 'json',
          },
        }
      );

      if (response.data.status === '1') {
        return response.data.pois || [];
      }
      return [];
    } catch (error) {
      console.error('地点搜索失败:', error);
      return [];
    }
  }

  // 地理编码
  async geocode(address: string): Promise<{ lng: number; lat: number } | null> {
    if (!this.config?.webServiceKey) {
      throw new Error('高德地图API配置未设置');
    }

    try {
      const response = await axios.get(
        'https://restapi.amap.com/v3/geocode/geo',
        {
          params: {
            key: this.config.webServiceKey,
            address: address,
          },
        }
      );

      if (response.data.status === '1' && response.data.geocodes.length > 0) {
        const location = response.data.geocodes[0].location.split(',');
        return {
          lng: parseFloat(location[0]),
          lat: parseFloat(location[1]),
        };
      }
      return null;
    } catch (error) {
      console.error('地理编码失败:', error);
      return null;
    }
  }
}

// AI服务（大语言模型）
export class AIService {
  private config: ReturnType<typeof getApiConfig<'ai'>>;

  constructor() {
    this.config = getApiConfig('ai');
  }

  // 生成行程规划
  async generateTravelPlan(requirements: string): Promise<any> {
    if (!this.config) {
      throw new Error('大语言模型API配置未设置');
    }

    const prompt = `你是一个专业的旅行规划师。请根据用户的以下需求，生成一份详细的旅行计划：

用户需求：${requirements}

请以JSON格式返回，包含以下字段：
{
  "title": "行程标题",
  "destination": "目的地",
  "start_date": "开始日期",
  "end_date": "结束日期",
  "budget": 预算金额,
  "travelers": 人数,
  "itinerary": [
    {
      "day": 1,
      "date": "日期",
      "activities": [
        {
          "type": "attraction|restaurant|accommodation|transport",
          "name": "活动名称",
          "description": "描述",
          "location": "地点名称",
          "time": "时间",
          "duration": "时长",
          "cost": 费用
        }
      ]
    }
  ]
}`;

    try {
      // 开发环境使用代理避免CORS问题，生产环境需要后端代理
      const apiUrl = import.meta.env.DEV 
        ? '/api/ai/chat/completions'  // 开发环境使用Vite代理
        : `${this.config.baseUrl}/chat/completions`;  // 生产环境需要后端代理处理CORS

      const response = await axios.post(
        apiUrl,
        {
          model: 'xop3qwen1b7',  // 使用Qwen3-1.7B模型
          messages: [
            {
              role: 'user',
              content: prompt,
            },
          ],
          temperature: 0.7,
        },
        {
          headers: {
            'Authorization': `Bearer ${this.config.apiKey}`,
            'Content-Type': 'application/json',
          },
        }
      );

      const content = response.data.choices[0]?.message?.content;
      if (content) {
        // 尝试解析JSON
        try {
          return JSON.parse(content);
        } catch {
          // 如果返回的不是纯JSON，尝试提取JSON部分
          const jsonMatch = content.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            return JSON.parse(jsonMatch[0]);
          }
          throw new Error('无法解析AI返回的行程数据');
        }
      }
      throw new Error('AI返回内容为空');
    } catch (error: any) {
      console.error('AI行程规划失败:', error);
      const errorMessage = error.response?.data?.error?.message 
        || error.message 
        || 'AI服务调用失败';
      
      // 如果是CORS错误，提供更友好的提示
      if (error.message?.includes('CORS') || error.code === 'ERR_NETWORK' || error.message?.includes('Access-Control-Allow-Origin')) {
        throw new Error('AI服务调用失败：CORS跨域问题。由于浏览器安全限制，无法直接调用AI API。建议：1) 使用后端代理服务；2) 配置CORS允许的域名；3) 使用支持CORS的API服务。');
      }
      
      throw new Error(`AI服务调用失败：${errorMessage}`);
    }
  }
}