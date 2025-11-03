# GitHub Actions + 阿里云容器镜像服务配置指南

## 前置准备

### 1. 创建阿里云容器镜像服务命名空间

1. 登录阿里云控制台：https://ecs.console.aliyun.com/
2. 进入"容器镜像服务 ACR" → "命名空间"
3. 创建命名空间（例如：`ai-travel-planner`）
4. 记录命名空间名称

### 2. 创建镜像仓库

1. 进入"容器镜像服务 ACR" → "镜像仓库"
2. 点击"创建镜像仓库"
3. 选择命名空间
4. 填写仓库名称：`ai-travel-planner`
5. 选择仓库类型：**私有** 或 **公开**
6. 完成创建

### 3. 获取访问凭证

1. 在阿里云控制台，点击右上角头像 → "AccessKey管理"
2. 创建 AccessKey（如果还没有）
3. 记录 **AccessKey ID** 和 **AccessKey Secret**

⚠️ **安全提示**：AccessKey Secret 只显示一次，请妥善保存

## 配置 GitHub Secrets

### Repository Secrets（推荐，简单直接）

**适用场景：** 大多数情况，简单直接

1. 进入你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**，添加以下两个密钥：

   | Secret 名称 | 值 | 说明 |
   |------------|-----|------|
   | `ALIYUN_USERNAME` | 你的 AccessKey ID | 阿里云 AccessKey ID |
   | `ALIYUN_PASSWORD` | 你的 AccessKey Secret | 阿里云 AccessKey Secret |

**优点：**
- 配置简单，所有工作流都可以使用
- 适合单个仓库的场景
- 不需要额外的环境配置

### Environment Secrets（可选，适合多环境）

**适用场景：** 需要区分开发、测试、生产等不同环境

如果你需要为不同环境使用不同的镜像仓库，可以使用 Environment Secrets：

1. 进入 **Settings** → **Environments**
2. 创建环境（例如：`production`、`development`）
3. 在每个环境中添加 Secrets：
   - `ALIYUN_USERNAME`
   - `ALIYUN_PASSWORD`

4. 修改工作流文件，添加环境配置：
   ```yaml
   jobs:
     build-and-push:
       runs-on: ubuntu-latest
       environment: production  # 指定环境
       steps:
         # ...
   ```

**优点：**
- 可以为不同环境配置不同的密钥
- 支持环境保护规则（需要审批才能部署）
- 适合复杂的企业级场景

**推荐：** 对于大多数场景，使用 **Repository Secrets** 即可。

### 修改工作流配置

编辑 `.github/workflows/docker-build.yml` 或 `.github/workflows/docker-build-simple.yml`：

```yaml
env:
  REGISTRY: registry.cn-hangzhou.aliyuncs.com  # 根据你的地域选择
  NAMESPACE: your-namespace                    # 改为你的命名空间
  IMAGE_NAME: ai-travel-planner
```

**可用的阿里云镜像仓库地址：**
- `registry.cn-hangzhou.aliyuncs.com` - 华东1（杭州）
- `registry.cn-shanghai.aliyuncs.com` - 华东2（上海）
- `registry.cn-beijing.aliyuncs.com` - 华北2（北京）
- `registry.cn-shenzhen.aliyuncs.com` - 华南1（深圳）

## 使用方式

### 方式一：推送到 main 分支自动构建

```bash
git add .
git commit -m "feat: add docker build workflow"
git push origin main
```

推送后，GitHub Actions 会自动：
1. 构建 Docker 镜像
2. 推送到阿里云镜像仓库
3. 标签为 `latest` 和 commit SHA

### 方式二：手动触发构建

1. 进入 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择 "Build and Push Docker Image to Aliyun"
4. 点击 **Run workflow**
5. 选择分支和标签（可选）
6. 点击 **Run workflow**

### 方式三：通过标签发布版本

```bash
git tag v1.0.0
git push origin v1.0.0
```

会创建标签为 `v1.0.0`、`1.0.0`、`1.0`、`1` 的镜像

## 拉取和使用镜像

### 登录阿里云镜像仓库

```bash
docker login --username=你的AccessKey_ID registry.cn-hangzhou.aliyuncs.com
# 输入密码时使用 AccessKey Secret
```

### 拉取镜像

```bash
docker pull registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest
```

### 运行容器

```bash
docker run -d -p 3000:80 \
  --name ai-travel-planner \
  registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest
```

## 工作流文件说明

### docker-build.yml（完整版）

- 支持多平台构建（amd64, arm64）
- 支持语义化版本标签
- 支持缓存优化
- 支持 PR 构建

### docker-build-simple.yml（简化版）

- 只构建 amd64 平台
- 固定标签为 `latest` 和 commit SHA
- 构建速度更快

## 查看构建状态

1. 进入 GitHub 仓库
2. 点击 **Actions** 标签
3. 查看构建历史和日志

## 常见问题

### 1. 构建失败：认证失败

**解决方案：**
- 检查 GitHub Secrets 是否正确配置
- 确认 AccessKey ID 和 Secret 是否正确
- 确认命名空间和仓库名称是否正确

### 2. 推送失败：权限不足

**解决方案：**
- 确认 AccessKey 有容器镜像服务的读写权限
- 检查命名空间是否为当前账号所有

### 3. 构建超时

**解决方案：**
- GitHub Actions 免费版有 6 小时限制
- 如果经常超时，可以考虑使用简化版工作流
- 或升级到 GitHub Pro

### 4. 如何更新镜像

只需推送代码到 main 分支，GitHub Actions 会自动构建新镜像。

## 镜像使用示例

### Docker Compose

```yaml
version: '3.8'

services:
  ai-travel-planner:
    image: registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest
    container_name: ai-travel-planner
    ports:
      - "3000:80"
    restart: unless-stopped
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-travel-planner
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ai-travel-planner
  template:
    metadata:
      labels:
        app: ai-travel-planner
    spec:
      containers:
      - name: ai-travel-planner
        image: registry.cn-hangzhou.aliyuncs.com/your-namespace/ai-travel-planner:latest
        ports:
        - containerPort: 80
```

## 安全建议

1. **使用私有仓库**：敏感应用建议使用私有镜像仓库
2. **定期轮换密钥**：定期更换 AccessKey
3. **限制访问权限**：只给必要的账号授权
4. **监控使用情况**：定期检查镜像仓库的访问日志

