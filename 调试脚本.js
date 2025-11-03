// 调试脚本 - 在浏览器控制台运行
// 检查应用是否正常加载

console.log('=== 应用调试信息 ===');
console.log('1. 检查根元素:', document.getElementById('root'));
console.log('2. 检查是否有React错误:', window.__REACT_DEVTOOLS_GLOBAL_HOOK__);
console.log('3. 检查LocalStorage:', localStorage.getItem('api_config'));
console.log('4. 检查是否有JavaScript错误: 查看Console标签页');

// 检查Supabase配置
const config = JSON.parse(localStorage.getItem('api_config') || '{}');
console.log('5. Supabase配置:', config.supabase);

// 检查是否有React渲染
setTimeout(() => {
  const root = document.getElementById('root');
  console.log('6. Root元素内容:', root?.innerHTML);
  console.log('7. Root元素子元素数量:', root?.children.length);
}, 1000);

