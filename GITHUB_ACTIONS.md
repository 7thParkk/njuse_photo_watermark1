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

**重要：** 阿里云容器镜像服务需要使用 **AccessKey** 进行认证

#### 方法一：使用 AccessKey（推荐）

**步骤 1：登录阿里云控制台**

1. 访问 https://ecs.console.aliyun.com/
2. 使用你的阿里云账号登录

**步骤 2：进入 AccessKey 管理页面**

有两种方式：

**方式 A：通过右上角头像**
1. 点击页面右上角的**头像图标**
2. 在下拉菜单中选择 **"AccessKey管理"**

**方式 B：直接访问**
1. 访问 https://ram.console.aliyun.com/manage/ak
2. 会提示你登录（如果未登录）

**步骤 3：创建 AccessKey**

1. 在 AccessKey 管理页面，你会看到：
   - 如果已经有 AccessKey，会显示已有的 AccessKey ID
   - 如果没有，会显示"创建 AccessKey"按钮

2. 点击 **"创建 AccessKey"** 按钮

3. 安全验证：
   - 可能需要输入手机验证码或进行其他安全验证
   - 完成验证后，会显示 AccessKey 信息

4. **重要：保存 AccessKey 信息**
   - **AccessKey ID**：类似于 `LTAI5txxxxxxxxxxxxx`（会一直显示）
   - **AccessKey Secret**：类似于 `xxxxxxxxxxxxxxxxxxxxxxxxxxxx`（**只显示一次**，必须立即保存）

⚠️ **安全提示**：
- AccessKey Secret **只显示一次**，关闭页面后无法再次查看
- 请立即复制并安全保存 AccessKey ID 和 Secret
- 建议将 Secret 保存在密码管理器或安全的地方
- 不要将 AccessKey 提交到代码仓库

**步骤 4：验证 AccessKey 权限**

创建 AccessKey 后，需要确保它有容器镜像服务的权限：

1. 进入"访问控制 RAM" → "用户"
2. 找到你的用户（通常是主账号）
3. 点击用户名进入详情页
4. 查看"权限"标签页
5. 确认是否有以下权限之一：
   - `AliyunContainerRegistryFullAccess`（容器镜像服务全部权限）**推荐**
   - `AliyunContainerRegistryReadWriteAccess`（读写权限）

**如果没有权限，添加权限：**

1. 在用户详情页，点击 **"添加权限"** 按钮
2. 选择 **"为当前用户授权"**
3. 在权限策略列表中，搜索 `ContainerRegistry`
4. 勾选 `AliyunContainerRegistryFullAccess`
5. 点击 **"确定"** 完成授权

**步骤 5：测试 AccessKey（可选但推荐）**

在本地测试 AccessKey 是否可以正常使用：

```bash
# 使用你的 AccessKey ID 和 Secret 登录
docker login --username=你的AccessKey_ID registry.cn-hangzhou.aliyuncs.com
# 输入密码时粘贴 AccessKey Secret
```

如果登录成功，说明 AccessKey 配置正确。

#### 方法二：使用 Docker 登录密码（不推荐）

如果你启用了 Docker 登录密码功能：

1. 进入"容器镜像服务 ACR" → "访问凭证"
2. 设置 Docker 登录密码
3. 使用你的阿里云账号和设置的密码登录

**注意：** 推荐使用方法一（AccessKey），更安全且更灵活，GitHub Actions 也需要使用 AccessKey。

## 配置 GitHub Secrets

### Repository Secrets（推荐，简单直接）

**适用场景：** 大多数情况，简单直接

1. 进入你的 GitHub 仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**，添加以下两个密钥：

   | Secret 名称 | 值 | 说明 |
   |------------|-----|------|
   | `ALIYUN_USERNAME` | 你的 AccessKey ID | 阿里云 AccessKey ID（不是账号名） |
   | `ALIYUN_PASSWORD` | 你的 AccessKey Secret | 阿里云 AccessKey Secret |

**重要提示：**
- `ALIYUN_USERNAME` 必须是 **AccessKey ID**，不是你的阿里云账号邮箱
- `ALIYUN_PASSWORD` 必须是 **AccessKey Secret**，不是账号密码
- 确保 AccessKey 有容器镜像服务的读写权限

### 验证 AccessKey 权限

1. 登录阿里云控制台
2. 进入"访问控制 RAM" → "用户"
3. 找到对应的用户
4. 检查是否有以下权限：
   - `AliyunContainerRegistryFullAccess`（容器镜像服务全部权限）
   - 或至少 `AliyunContainerRegistryReadWriteAccess`（读写权限）

如果没有权限，需要：
1. 进入"访问控制 RAM" → "用户"
2. 点击用户 → "添加权限"
3. 添加 `AliyunContainerRegistryFullAccess` 权限

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
  NAMESPACE: your-namespace                    # ⚠️ 改为你的阿里云命名空间名称
  IMAGE_NAME: ai-travel-planner                # ⚠️ 改为你的阿里云镜像仓库名称
```

**重要说明：**
- `NAMESPACE`：必须是你在**阿里云容器镜像服务**中创建的**命名空间**名称
- `IMAGE_NAME`：必须是你在**阿里云容器镜像服务**中创建的**镜像仓库**名称
- ⚠️ 这两个名称是**阿里云**上的配置，**不是** GitHub 仓库名称

**查找方法：**
1. 登录阿里云控制台
2. 进入"容器镜像服务 ACR" → "命名空间" → 查看你的命名空间名称
3. 进入"容器镜像服务 ACR" → "镜像仓库" → 查看你的仓库名称

**可用的阿里云镜像仓库地址：**
- `registry.cn-hangzhou.aliyuncs.com` - 华东1（杭州）
- `registry.cn-shanghai.aliyuncs.com` - 华东2（上海）
- `registry.cn-beijing.aliyuncs.com` - 华北2（北京）
- `registry.cn-shenzhen.aliyuncs.com` - 华南1（深圳）

**示例：**
假设你在阿里云上：
- 命名空间名称：`space_7thpark`
- 镜像仓库名称：`llm4se`

那么配置应该是：
```yaml
env:
  REGISTRY: registry.cn-hangzhou.aliyuncs.com
  NAMESPACE: space_7thpark
  IMAGE_NAME: llm4se
```

最终推送的镜像地址将是：`registry.cn-hangzhou.aliyuncs.com/space_7thpark/llm4se:latest`

## 使用方式

### 方式一：推送到 travel_planner 分支自动构建

```bash
git add .
git commit -m "feat: add docker build workflow"
git push origin travel_planner
```

推送后，GitHub Actions 会自动：
1. 构建 Docker 镜像
2. 推送到阿里云镜像仓库
3. 标签为 `travel_planner` 和 commit SHA

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

### 1. 认证失败：unauthorized: authentication required

**可能原因：**
- AccessKey ID 或 Secret 不正确
- AccessKey 没有容器镜像服务的权限
- 使用了错误的用户名（应该用 AccessKey ID，不是账号邮箱）

**解决方案：**
1. 检查 GitHub Secrets 中的值是否正确
2. 确认使用的是 AccessKey ID（不是账号邮箱）
3. 确认 AccessKey Secret 正确（注意不要有多余的空格）
4. 检查 AccessKey 是否有容器镜像服务的权限
5. 尝试重新创建 AccessKey

**验证方法：**
```bash
# 在本地测试登录
docker login --username=你的AccessKey_ID registry.cn-hangzhou.aliyuncs.com
# 输入 AccessKey Secret
```

### 2. 推送失败：权限不足

**解决方案：**
- 确认 AccessKey 有容器镜像服务的读写权限
- 检查命名空间是否为当前账号所有
- 确认镜像仓库已创建

### 3. 构建超时

**解决方案：**
- GitHub Actions 免费版有 6 小时限制
- 如果经常超时，可以考虑使用简化版工作流
- 或升级到 GitHub Pro

### 4. 如何更新镜像

只需推送代码到 travel_planner 分支，GitHub Actions 会自动构建新镜像。

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
5. **不要泄露 AccessKey**：永远不要在代码中硬编码 AccessKey
