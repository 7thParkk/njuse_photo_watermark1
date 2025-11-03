// 浏览器控制台测试脚本
// 使用方法：在浏览器控制台（F12 -> Console）中运行以下代码

// ==================== 测试1：API配置检查 ====================
console.log('=== 测试1：API配置检查 ===');
const config = JSON.parse(localStorage.getItem('api_config') || '{}');
console.log('当前配置:', config);
console.log('科大讯飞配置:', config.xunfei ? '✅ 已配置' : '❌ 未配置');
console.log('高德地图配置:', config.amap ? '✅ 已配置' : '❌ 未配置');
console.log('AI配置:', config.ai ? '✅ 已配置' : '❌ 未配置');
console.log('Supabase配置:', config.supabase ? '✅ 已配置' : '❌ 未配置');

// ==================== 测试2：Supabase连接测试 ====================
console.log('\n=== 测试2：Supabase连接测试 ===');
// 需要先导入 supabase 实例
// 在浏览器控制台中可能无法直接导入，需要通过应用内测试

// ==================== 测试3：地图服务测试 ====================
console.log('\n=== 测试3：地图服务测试 ===');
// 测试高德地图API（需要先配置）
async function testMapService() {
  try {
    const config = JSON.parse(localStorage.getItem('api_config') || '{}');
    if (!config.amap?.webServiceKey) {
      console.log('❌ 高德地图API未配置');
      return;
    }
    
    const response = await fetch(
      `https://restapi.amap.com/v3/geocode/geo?key=${config.amap.webServiceKey}&address=北京市天安门`
    );
    const data = await response.json();
    console.log('地理编码测试结果:', data);
    
    if (data.status === '1') {
      console.log('✅ 高德地图API调用成功');
    } else {
      console.log('❌ 高德地图API调用失败:', data.info);
    }
  } catch (error) {
    console.error('❌ 测试失败:', error);
  }
}
// 运行：testMapService()

// ==================== 测试4：AI服务测试 ====================
console.log('\n=== 测试4：AI服务测试 ===');
async function testAIService() {
  try {
    const config = JSON.parse(localStorage.getItem('api_config') || '{}');
    if (!config.ai?.baseUrl || !config.ai?.apiKey) {
      console.log('❌ AI API未配置');
      return;
    }
    
    const response = await fetch(`${config.ai.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${config.ai.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo',
        messages: [
          {
            role: 'user',
            content: '你好，请回复"测试成功"',
          },
        ],
        max_tokens: 50,
      }),
    });
    
    const data = await response.json();
    console.log('AI服务测试结果:', data);
    
    if (data.choices && data.choices.length > 0) {
      console.log('✅ AI服务调用成功');
      console.log('回复:', data.choices[0].message.content);
    } else {
      console.log('❌ AI服务调用失败:', data);
    }
  } catch (error) {
    console.error('❌ 测试失败:', error);
  }
}
// 运行：testAIService()

// ==================== 测试5：本地存储检查 ====================
console.log('\n=== 测试5：本地存储检查 ===');
console.log('API配置:', localStorage.getItem('api_config'));
console.log('其他存储项:', Object.keys(localStorage));

// ==================== 测试6：用户认证状态检查 ====================
console.log('\n=== 测试6：用户认证状态检查 ===');
// 需要在应用内检查，通过 React DevTools 查看状态

// ==================== 测试7：网络请求监控 ====================
console.log('\n=== 测试7：网络请求监控 ===');
console.log('打开 Network 标签页查看所有API请求');
console.log('检查以下请求是否成功：');
console.log('1. Supabase 认证请求');
console.log('2. Supabase 数据查询请求');
console.log('3. 高德地图API请求');
console.log('4. AI服务API请求');

// ==================== 测试8：错误检查 ====================
console.log('\n=== 测试8：错误检查 ===');
console.log('检查 Console 标签页是否有错误信息');
console.log('检查是否有红色错误提示');

// ==================== 使用说明 ====================
console.log('\n=== 使用说明 ===');
console.log('1. 复制上述测试函数到控制台');
console.log('2. 调用 testMapService() 测试地图服务');
console.log('3. 调用 testAIService() 测试AI服务');
console.log('4. 检查 Network 标签页查看所有API请求');
console.log('5. 检查 Application -> Local Storage 查看存储的数据');

