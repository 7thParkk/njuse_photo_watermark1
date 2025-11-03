# Docker 安装和使用指南

## Docker 未安装时的解决方案

### Windows 系统

#### 1. 安装 Docker Desktop

1. **下载 Docker Desktop**
   - 访问：https://www.docker.com/products/docker-desktop/
   - 点击 "Download for Windows"
   - 下载 `Docker Desktop Installer.exe`

2. **安装步骤**
   - 运行安装程序
   - 按照向导完成安装
   - 安装完成后重启电脑（如提示）

3. **启动 Docker Desktop**
   - 从开始菜单启动 "Docker Desktop"
   - 等待 Docker 完全启动（系统托盘图标不再闪烁）
   - 首次启动可能需要几分钟时间

4. **验证安装**
   ```powershell
   docker --version
   docker ps
   ```

#### 2. 如果 Docker 已安装但无法识别

**问题：** 命令提示符显示 `'docker' 不是内部或外部命令`

**解决方案：**

1. **检查 Docker Desktop 是否运行**
   - 查看系统托盘是否有 Docker 图标
   - 如果没有，手动启动 Docker Desktop

2. **重启 PowerShell/CMD**
   - 关闭当前命令行窗口
   - 重新打开 PowerShell 或 CMD
   - 再次运行脚本

3. **检查 PATH 环境变量**
   ```powershell
   # 查看 PATH 中是否包含 Docker
   $env:PATH -split ';' | Select-String docker
   
   # 如果 Docker Desktop 已安装，通常路径在：
   # C:\Program Files\Docker\Docker\resources\bin
   ```

4. **手动添加 PATH（如需要）**
   - 右键 "此电脑" → "属性"
   - "高级系统设置" → "环境变量"
   - 在 "系统变量" 中找到 "Path"
   - 添加 Docker 的安装路径（通常在 `C:\Program Files\Docker\Docker\resources\bin`）
   - 重启命令行窗口

### Linux/Mac 系统

#### Ubuntu/Debian

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
```

#### macOS

```bash
# 使用 Homebrew 安装
brew install --cask docker

# 或下载 Docker Desktop for Mac
# https://www.docker.com/products/docker-desktop/
```

## 验证 Docker 是否正常工作

运行以下命令验证：

```bash
# 查看 Docker 版本
docker --version

# 查看 Docker 信息
docker info

# 运行测试容器
docker run hello-world
```

如果以上命令都能正常执行，说明 Docker 已正确安装。

## 常见问题

### 1. Docker Desktop 启动失败

**解决方案：**
- 确保已启用虚拟化（BIOS/UEFI 设置）
- 确保 Windows 功能中启用了 "Hyper-V" 或 "WSL 2"
- 以管理员身份运行 Docker Desktop

### 2. Docker 命令权限不足（Linux）

**解决方案：**
```bash
# 将当前用户添加到 docker 组
sudo usermod -aG docker $USER

# 重新登录或运行
newgrp docker
```

### 3. 网络连接问题

**解决方案：**
- 检查网络连接
- 如果在公司网络，可能需要配置代理
- Docker Desktop → Settings → Resources → Proxies

## 构建镜像的替代方案

如果无法安装 Docker，可以考虑：

1. **使用云服务构建**
   - GitHub Actions
   - GitLab CI/CD
   - Docker Hub 自动构建

2. **使用已构建的镜像**
   - 如果已发布到 Docker Hub，可以直接拉取
   - `docker pull your-username/ai-travel-planner:latest`

3. **手动构建**
   - 使用 npm 构建：`npm run build`
   - 使用任何静态文件服务器（如 nginx）部署 `dist` 目录

