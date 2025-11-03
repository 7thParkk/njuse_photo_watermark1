#!/bin/bash

# Docker 镜像构建和导出脚本

set -e

IMAGE_NAME="ai-travel-planner"
IMAGE_TAG="latest"
OUTPUT_FILE="ai-travel-planner.tar.gz"

echo "🚀 开始构建 Docker 镜像..."

# 构建镜像
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

echo "✅ 镜像构建完成！"
echo "📦 镜像信息："
docker images | grep ${IMAGE_NAME}

echo ""
echo "💾 导出镜像文件..."

# 导出并压缩镜像
docker save ${IMAGE_NAME}:${IMAGE_TAG} | gzip > ${OUTPUT_FILE}

echo "✅ 镜像导出完成！"
echo "📁 文件位置: $(pwd)/${OUTPUT_FILE}"
echo "📊 文件大小: $(du -h ${OUTPUT_FILE} | cut -f1)"

echo ""
echo "📝 使用说明："
echo "1. 将 ${OUTPUT_FILE} 文件分享给其他人"
echo "2. 其他人可以运行以下命令导入："
echo "   gunzip -c ${OUTPUT_FILE} | docker load"
echo "3. 然后运行容器："
echo "   docker run -d -p 3000:80 --name ${IMAGE_NAME} ${IMAGE_NAME}:${IMAGE_TAG}"

