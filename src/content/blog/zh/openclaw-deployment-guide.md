---
title: 'OpenClaw 部署完全指南：从零开始搭建你的本地 AI 助理'
description: '手把手教你如何在本地部署 OpenClaw（原 Clawdbot），包括环境准备、Docker 部署、模型配置、插件安装和常见问题排查。即使没有深厚的技术背景，也能轻松拥有属于自己的 AI 助理。'
pubDate: 2026-04-03
heroImage: '../../../assets/hero-clawdbot.jpg'
category: '技术教程'
---

在上一篇文章中，我们介绍了 OpenClaw（原 Clawdbot）的技术架构和核心功能。今天，我们将进入实战环节，手把手教你从零开始部署这个强大的本地 AI 助理。

## 前置要求

在开始之前，请确保你的系统满足以下基本要求：

### 硬件要求
- **CPU**：4 核心及以上（推荐 8 核心）
- **内存**：16GB 及以上（推荐 32GB）
- **存储**：至少 50GB 可用空间（用于存储模型和向量数据库）
- **GPU**（可选但强烈推荐）：
  - NVIDIA GPU：支持 CUDA 11.0+（如 RTX 3060 及以上）
  - Apple Silicon：M1/M2/M3/M4 芯片（统一内存 16GB+）

### 软件要求
- **操作系统**：Linux / macOS / Windows (WSL2)
- **Docker**：20.10.0 及以上版本
- **Docker Compose**：2.0.0 及以上版本
- **Git**：用于克隆项目仓库

## 第一步：环境准备

### 1.1 安装 Docker

#### macOS
```bash
# 使用 Homebrew 安装
brew install --cask docker

# 或者下载官方安装包
# 访问 https://www.docker.com/products/docker-desktop
```

#### Ubuntu/Debian Linux
```bash
# 更新包索引
sudo apt-get update

# 安装依赖
sudo apt-get install ca-certificates curl gnupg

# 添加 Docker 官方 GPG 密钥
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 设置仓库
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装 Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 验证安装
sudo docker run hello-world
```

#### Windows (WSL2)
1. 启用 WSL2：以管理员身份运行 PowerShell
```powershell
wsl --install
```
2. 下载并安装 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
3. 重启计算机

### 1.2 安装 Ollama（本地 LLM 运行时）

OpenClaw 依赖 Ollama 来运行本地大模型。

#### macOS / Linux
```bash
# 使用官方安装脚本
curl -fsSL https://ollama.com/install.sh | sh

# 验证安装
ollama --version
```

#### Windows
```powershell
# 下载官方安装包
# 访问 https://ollama.com/download
```

## 第二步：克隆 OpenClaw 项目

```bash
# 克隆仓库
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# 查看项目结构
ls -la
```

项目结构如下：
```
openclaw/
├── docker-compose.yml      # Docker 编排配置
├── config/                 # 配置文件目录
│   ├── config.yaml        # 主配置文件
│   ├── prompts/           # 系统提示词
│   └── actions/           # 自定义动作脚本
├── integrations/          # 集成插件
├── data/                  # 数据目录（向量数据库等）
└── README.md
```

## 第三步：配置 OpenClaw

### 3.1 编辑主配置文件

```bash
# 复制示例配置
cp config/config.example.yaml config/config.yaml

# 使用你喜欢的编辑器打开
vim config/config.yaml
```

配置文件关键参数说明：

```yaml
# LLM 配置
llm:
  provider: ollama          # 使用 Ollama 作为提供者
  model: llama3:8b         # 默认模型（可根据硬件调整）
  base_url: http://ollama:11434  # Ollama 服务地址
  temperature: 0.7         # 生成温度
  max_tokens: 2048         # 最大生成长度

# 向量数据库配置
vector_db:
  provider: qdrant         # 使用 Qdrant
  url: http://qdrant:6333  # Qdrant 服务地址
  collection_name: openclaw_kb

# 集成配置
integrations:
  slack:
    enabled: true
    bot_token: "xoxb-your-slack-bot-token"  # 你的 Slack Bot Token
    app_token: "xapp-your-slack-app-token"
  telegram:
    enabled: false
    bot_token: ""          # 如果需要启用，填入你的 Telegram Bot Token

# 动作配置
actions:
  enabled: true
  allowed_paths:           # 限制可访问的路径（安全考虑）
    - /home/user/documents
    - /home/user/downloads
  shell_enabled: true      # 允许执行 Shell 命令
```

### 3.2 获取 Slack Bot Token（以 Slack 集成为例）

1. 访问 [Slack API](https://api.slack.com/apps)
2. 点击 "Create New App" → "From scratch"
3. 填写 App 名称和选择工作区
4. 在 "OAuth & Permissions" 页面：
   - 添加 Bot Token Scopes：`chat:write`, `channels:history`, `im:history`, `app_mentions:read`
5. 安装 App 到工作区，获取 `Bot User OAuth Token`
6. 启用 Socket Mode 并获取 `App-Level Token`

## 第四步：启动 OpenClaw

### 4.1 拉取 Docker 镜像并启动服务

```bash
# 在项目根目录执行
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f openclaw
```

首次启动会自动下载所需的 Docker 镜像（约 5-10 分钟，取决于网络速度）。

### 4.2 下载并运行 LLM 模型

```bash
# 进入 Ollama 容器
docker exec -it openclaw-ollama bash

# 下载模型（以 Llama 3 8B 为例）
ollama pull llama3:8b

# 测试模型运行
ollama run llama3:8b "Hello, OpenClaw!"

# 退出容器
exit
```

模型大小参考：
- `llama3:8b`：约 4.7GB（适合 16GB 内存设备）
- `llama3:70b`：约 40GB（需要 32GB+ 内存）

## 第五步：验证部署

### 5.1 检查所有服务状态

```bash
# 检查容器状态
docker-compose ps

# 应该看到以下容器都在运行：
# openclaw-core       # 主服务
# openclaw-ollama     # LLM 运行时
# openclaw-qdrant     # 向量数据库
# openclab-redis      # 缓存（可选）
```

### 5.2 测试 Slack 集成

1. 在 Slack 中找到你的 App
2. 向 App 发送消息："Hello, OpenClaw!"
3. 如果配置正确，你应该收到类似以下的回复：

> "你好！我是 OpenClaw，你的本地 AI 助理。我可以帮你处理消息、管理知识库和执行自动化任务。有什么可以帮你的吗？"

### 5.3 测试知识库功能

```bash
# 向 OpenClaw 发送指令：
"/kb-add https://example.com/article.html"

# 等待处理完成后，提问：
"那篇文章讲了什么？"
```

## 第六步：配置高级功能

### 6.1 启用个人知识库（RAG）

```bash
# 准备你的文档
mkdir -p data/documents
cp ~/Documents/*.pdf data/documents/

# 在 Slack 中发送：
"/kb-index /data/documents"
```

OpenClaw 会自动将文档向量化并存储到 Qdrant 中。

### 6.2 创建自定义 Action

创建一个简单的天气查询 Action：

```bash
# 编辑 action 脚本
vim config/actions/get_weather.py
```

```python
#!/usr/bin/env python3
import requests
import sys

def get_weather(city):
    """获取指定城市的天气信息"""
    # 这里使用免费的天气 API
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current = data['current_condition'][0]
        return f"{city} 当前天气：{current['weatherDesc'][0]['value']}，温度 {current['temp_C']}°C"
    return f"无法获取 {city} 的天气信息"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        print(get_weather(city))
    else:
        print("请提供城市名称")
```

```bash
# 给脚本添加执行权限
chmod +x config/actions/get_weather.py

# 重启 OpenClaw 服务
docker-compose restart openclaw

# 在 Slack 中测试：
"/action get_weather Beijing"
```

### 6.3 配置自动化任务

编辑 `config/automations.yaml`：

```yaml
automations:
  - name: "每日晨报"
    trigger:
      type: schedule
      cron: "0 9 * * 1-5"  # 工作日早上 9 点
    actions:
      - type: message
        target: slack
        channel: "#general"
        template: "morning_briefing"

  - name: "跨平台消息摘要"
    trigger:
      type: schedule
      cron: "0 18 * * *"  # 每天 18:00
    actions:
      - type: summary
        sources: [slack, telegram]
        target: slack
        channel: "#daily-summary"
```

## 第七步：常见问题排查

### 问题 1：Ollama 模型下载失败

**症状**：执行 `ollama pull` 时报错

**解决方案**：
```bash
# 使用镜像加速
export OLLAMA_MIRROR=https://ollama.registry.example.com
ollama pull llama3:8b
```

### 问题 2：Slack Bot 无响应

**检查清单**：
1. Bot Token 是否正确配置
2. Socket Mode 是否已启用
3. 必要的 Scopes 是否已添加
4. 查看日志：`docker-compose logs openclaw | grep slack`

### 问题 3：内存不足

**症状**：系统变慢，容器被杀

**解决方案**：
1. 使用更小的模型：`llama3:8b` → `mistral:7b` → `gemma:2b`
2. 限制 Docker 内存使用：
```yaml
# 在 docker-compose.yml 中添加
services:
  openclaw:
    deploy:
      resources:
        limits:
          memory: 8G
```

### 问题 4：向量数据库查询慢

**解决方案**：
```bash
# 重启 Qdrant 并优化配置
docker-compose restart qdrant

# 考虑使用更小的嵌入模型
# 在 config.yaml 中修改
embeddings:
  model: "nomic-embed-text"  # 更小更快的嵌入模型
```

## 第八步：性能优化建议

### 8.1 GPU 加速（如果有 NVIDIA GPU）

```bash
# 安装 NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit

# 配置 Docker 使用 NVIDIA 运行时
sudo nvidia-ctk runtime configure --runtime=docker

# 重启 Docker
sudo systemctl restart docker

# 修改 docker-compose.yml
services:
  ollama:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 8.2 调整模型参数

在 `config/config.yaml` 中：
```yaml
llm:
  max_tokens: 1024        # 减少最大生成长度（更快但可能截断）
  temperature: 0.5        # 降低温度（更确定的输出）
  context_window: 4096    # 根据需求调整上下文窗口
```

### 8.3 启用缓存

```yaml
# 在 config.yaml 中
cache:
  enabled: true
  provider: redis         # 使用 Redis 作为缓存
  ttl: 3600              # 缓存 1 小时
```

## 进阶：多模型部署

如果你有足够的硬件资源，可以同时运行多个模型以应对不同场景：

```yaml
# config.yaml
llm:
  models:
    default: llama3:8b
    fast: mistral:7b           # 用于快速响应
    creative: llama3:70b       # 用于复杂任务
    code: :33b   # 用于代码生成

  routing_rules:
    - if: context.includes("code")
      use: code
    - if: context.length > 1000
      use: creative
    - else: fast
```

## 安全建议

1. **网络隔离**：如果可能，将 OpenClaw 部署在独立的网络中
2. **定期更新**：定期拉取最新镜像和代码
```bash
git pull
docker-compose pull
docker-compose up -d --build
```
3. **备份配置**：定期备份 `config/` 和 `data/` 目录
4. **监控日志**：设置日志监控，及时发现异常

## 总结

通过以上步骤，你已经成功部署了属于自己的 OpenClaw 本地 AI 助理。现在你可以：

- ✅ 在 Slack/Telegram 中与 AI 互动
- ✅ 构建和查询个人知识库
- ✅ 执行本地自动化任务
- ✅ 创建自定义 Actions
- ✅ 配置自动化工作流

OpenClaw 的强大之处在于其可扩展性。随着你的需求增长，你可以持续添加新的集成、创建更复杂的 Actions，并优化模型配置。

**下一步**：
- 尝试接入其他通讯平台（Discord、WhatsApp）
- 探索 [OpenClaw 社区](https://github.com/openclaw/openclaw)的更多插件
- 分享你的自定义 Actions 给社区

如果你在部署过程中遇到任何问题，欢迎在 GitHub Issues 中提问，或者查阅我们的[完整文档](https://docs.openclaw.dev)。

Happy Hacking! 🚀
