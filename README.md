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

### 方式一：使用 Docker（推荐）

#### 使用 Docker Compose（最简单）

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down
```

访问 http://localhost:3000

#### 使用 Docker 命令

```bash
# 构建镜像
docker build -t ai-travel-planner .

# 运行容器
docker run -d -p 3000:80 --name ai-travel-planner ai-travel-planner

# 查看日志
docker logs -f ai-travel-planner

# 停止容器
docker stop ai-travel-planner
docker rm ai-travel-planner
```

#### 从 Docker Hub 拉取（如果有发布）

```bash
docker pull your-username/ai-travel-planner:latest
docker run -d -p 3000:80 --name ai-travel-planner your-username/ai-travel-planner:latest
```

### 方式二：本地开发

#### 安装依赖

```bash
npm install
```

#### 配置 API

1. 启动应用后，访问设置页面
2. 输入各 API 的密钥（参考 prepare.md 文件）
3. 保存配置

#### 运行开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

#### 构建生产版本

```bash
npm run build
```

生产文件将输出到 `dist` 目录

## Docker 部署

### 方式一：使用 GitHub Actions 自动构建（推荐）

项目已配置 GitHub Actions，可以自动构建并推送到阿里云容器镜像仓库。

**配置步骤：**

1. 在 GitHub 仓库中添加 Secrets：
   - `ALIYUN_USERNAME`: 阿里云 AccessKey ID
   - `ALIYUN_PASSWORD`: 阿里云 AccessKey Secret

2. 修改 `.github/workflows/docker-build.yml` 中的命名空间：
   ```yaml
   env:
     NAMESPACE: your-namespace  # 改为你的阿里云命名空间
     IMAGE_NAME: ai-travel-planner  # 改为你的镜像仓库名称
   ```

3. 推送代码到 travel_planner 分支，GitHub Actions 会自动构建并推送镜像

**详细配置说明请参考：** [GITHUB_ACTIONS.md](./GITHUB_ACTIONS.md)

**⚠️ 常见问题：** 如果遇到认证失败，请确保：
- 使用 AccessKey ID（不是账号邮箱）作为 `ALIYUN_USERNAME`
- 使用 AccessKey Secret（不是账号密码）作为 `ALIYUN_PASSWORD`
- AccessKey 有容器镜像服务的读写权限

### 方式二：本地构建

**⚠️ 重要：** 需要先安装 Docker Desktop

- **Windows/Mac**: 下载安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: 参考 [DOCKER_INSTALL.md](./DOCKER_INSTALL.md) 中的安装说明

安装完成后，确保 Docker Desktop 正在运行，然后执行以下命令。

#### 使用 Docker Compose（最简单）

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down
```

#### 使用 Docker 命令

```bash
# 构建镜像
docker build -t ai-travel-planner .

# 运行容器
docker run -d -p 3000:80 --name ai-travel-planner ai-travel-planner
```

#### 从阿里云镜像仓库拉取

```bash
# 登录阿里云镜像仓库（首次需要）
docker login --username=你的AccessKey_ID registry.cn-hangzhou.aliyuncs.com

# 拉取镜像
docker pull registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest

# 运行容器
docker run -d -p 3000:80 --name ai-travel-planner \
  registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest
```

详细的 Docker 构建、发布和使用说明请参考 [DOCKER.md](./DOCKER.md)

如果遇到 Docker 未安装的错误，请参考 [DOCKER_INSTALL.md](./DOCKER_INSTALL.md)

## 注意事项

⚠️ **重要**：
- API 密钥不会提交到代码库，请通过设置页面配置
- 使用 Docker 部署时，配置信息存储在浏览器的 localStorage 中
- 建议在生产环境中使用环境变量或配置管理服务

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
