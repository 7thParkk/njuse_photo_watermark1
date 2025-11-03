# Docker 构建和发布指南

## 构建 Docker 镜像

### 本地构建

```bash
# 构建镜像
docker build -t ai-travel-planner:latest .

# 查看镜像
docker images | grep ai-travel-planner
```

### 构建多平台镜像（可选）

```bash
# 需要先安装 buildx
docker buildx create --use

# 构建多平台镜像
docker buildx build --platform linux/amd64,linux/arm64 -t ai-travel-planner:latest .
```

## 发布到 Docker Hub

### 1. 登录 Docker Hub

```bash
docker login
```

### 2. 打标签

```bash
docker tag ai-travel-planner:latest YOUR_USERNAME/ai-travel-planner:latest
docker tag ai-travel-planner:latest YOUR_USERNAME/ai-travel-planner:v1.0.0
```

### 3. 推送镜像

```bash
docker push YOUR_USERNAME/ai-travel-planner:latest
docker push YOUR_USERNAME/ai-travel-planner:v1.0.0
```

### 4. 其他人使用

```bash
docker pull YOUR_USERNAME/ai-travel-planner:latest
docker run -d -p 3000:80 --name ai-travel-planner YOUR_USERNAME/ai-travel-planner:latest
```

## 导出/导入镜像文件

### 导出镜像为 tar 文件

```bash
# 导出镜像
docker save ai-travel-planner:latest -o ai-travel-planner.tar

# 或者压缩导出（推荐）
docker save ai-travel-planner:latest | gzip > ai-travel-planner.tar.gz
```

### 导入镜像文件

```bash
# 从 tar 文件导入
docker load -i ai-travel-planner.tar

# 从压缩文件导入
gunzip -c ai-travel-planner.tar.gz | docker load
```

### 分发镜像文件

1. 导出镜像：`docker save ai-travel-planner:latest | gzip > ai-travel-planner.tar.gz`
2. 将 `ai-travel-planner.tar.gz` 文件分享给其他人
3. 其他人导入：`gunzip -c ai-travel-planner.tar.gz | docker load`
4. 运行容器：`docker run -d -p 3000:80 --name ai-travel-planner ai-travel-planner:latest`

## 使用 docker-compose

### 启动服务

```bash
docker-compose up -d
```

### 查看日志

```bash
docker-compose logs -f
```

### 停止服务

```bash
docker-compose down
```

### 重启服务

```bash
docker-compose restart
```

## 镜像大小优化

当前镜像使用了多阶段构建，已经优化了镜像大小：
- 构建阶段：包含 Node.js 和所有依赖（较大）
- 运行阶段：只包含 nginx 和构建产物（较小）

最终镜像大小约 25-30MB（基于 nginx:alpine）

