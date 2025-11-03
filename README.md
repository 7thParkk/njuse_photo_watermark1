# AI 旅行规划师

Web 版 AI 旅行规划师，通过 AI 了解用户需求，自动生成详细的旅行路线和建议。

## 功能特性

- 🎤 **语音识别**：支持语音输入旅行需求
- 🗺️ **地图展示**：基于高德地图的交互式地图
- 🤖 **AI 规划**：智能生成个性化旅行路线
- 💰 **预算管理**：记录和分析旅行开销
- ☁️ **云端同步**：多设备数据同步

## 技术栈

- React + TypeScript
- Vite
- Tailwind CSS
- Zustand (状态管理)
- Supabase (认证和数据库)
- 科大讯飞 API (语音识别)
- 高德地图 API (地图服务)
- 大语言模型 API (行程规划)

## 快速开始

### 安装依赖

```bash
npm install
```

### 配置 API

1. 启动应用后，访问设置页面
2. 输入各 API 的密钥（参考 prepare.md 文件）
3. 保存配置

### 运行开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

## 注意事项

⚠️ **重要**：API 密钥不会提交到代码库，请通过设置页面配置。

## 项目结构

```
src/
├── components/    # 可复用组件
├── pages/        # 页面组件
├── services/     # API 服务层
├── stores/       # 状态管理
├── utils/        # 工具函数
└── types/        # 类型定义
```
