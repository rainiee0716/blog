---
title: 'OpenClaw 部署指南：从零开始搭建你的本地 AI 助理'
description: '手把手教你本地部署 OpenClaw（原 Clawdbot）：环境准备、Docker 部署、模型配置、插件安装、常见排查。即使没有深厚技术背景也能跟下来。'
pubDate: '2026-04-03'
heroImage: '../../../assets/hero-clawdbot.jpg'
category: '技术教程'
---

上一篇我们聊了 OpenClaw（原 Clawdbot）的架构和功能。这一篇进入实战环节，从零部署一个本地 AI 助理。

## 前置要求

### 硬件

- **CPU**：4 核以上（推荐 8 核）
- **内存**：16GB 以上（推荐 32GB）
- **存储**：至少 50GB 可用空间（放模型和向量数据库）
- **GPU**（可选但强烈推荐）：
  - NVIDIA：CUDA 11.0+（RTX 3060 及以上）
  - Apple Silicon：M1/M2/M3/M4，统一内存 16GB+

### 软件

- 操作系统：Linux / macOS / Windows (WSL2)
- Docker：20.10+
- Docker Compose：2.0+
- Git

## 第一步：环境准备

### 装 Docker

**macOS：**

```bash
brew install --cask docker
```

或者去 docker.com 下载官方包。

**Ubuntu/Debian：**

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
# 加 Docker 官方 GPG 密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# 加仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

**Windows：** 装 Docker Desktop，启用 WSL2 后端。

装完之后，把当前用户加入 docker 组（避免每次 sudo）：

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### 验证安装

```bash
docker --version
docker compose version
```

## 第二步：克隆 OpenClaw

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
```

## 第三步：配置环境变量

复制示例配置：

```bash
cp .env.example .env
```

编辑 `.env`，关键变量：

```bash
# Ollama 地址（默认即可）
OLLAMA_BASE_URL=http://ollama:11434

# 管理员密码（务必修改！）
ADMIN_PASSWORD=your_strong_password_here

# 数据存储路径
DATA_PATH=./data

# 日志级别
LOG_LEVEL=info
```

## 第四步：启动服务

```bash
docker compose up -d
```

这个命令会启动三个服务：

- `openclaw`：主应用
- `ollama`：模型推理后端
- `qdrant`：向量数据库

查看启动状态：

```bash
docker compose ps
```

等所有服务都变成 `healthy` 状态。

## 第五步：下载模型

进 Ollama 容器：

```bash
docker exec -it openclaw-ollama-1 bash
```

下载模型（按显存/内存选）：

```bash
# 7B：8GB 显存/内存
ollama pull llama3:8b

# 13B：16GB
ollama pull llama3:13b

# 70B：64GB（需要高性能机器）
ollama pull llama3:70b
```

退出容器：

```bash
exit
```

## 第六步：访问控制台

打开浏览器：

```
http://localhost:3000
```

首次访问用 `.env` 里设置的 `ADMIN_PASSWORD` 登录。

进入 `Settings` → `Model Provider`：

1. 选择 `Ollama`
2. Model Name 填刚才下载的（比如 `llama3:8b`）
3. 点 `Test Connection`，返回 Success 说明 OK

## 第七步：装插件

进 `Integrations` 页面，按需启用：

- **Slack**：填 Bot Token 和 App Token
- **Discord**：填 Bot Token
- **Telegram**：填 Bot Token
- **Calendar**：OAuth 授权 Google Calendar

每启用一个插件，记得重启容器：

```bash
docker compose restart openclaw
```

## 第八步：建个人知识库

把本地文档喂给 OpenClaw：

```bash
# 把文件丢到 data/knowledge/ 目录下
cp -r ~/Documents/notes data/knowledge/
```

进控制台 `Knowledge Base` → `Create New`：

- 名称：比如 "我的笔记"
- 数据源：`data/knowledge`
- Embedding 模型：`nomic-embed-text`（默认）

点 `Build Index`，等待完成（取决于文档量）。

之后你就可以问："我上周写的关于 OKR 的笔记里讲了什么？"——AI 会从本地索引里找答案。

## 常见问题排查

### 容器起不来

```bash
docker compose logs openclaw
```

常见原因：

- 端口冲突：改 `.env` 里的 `PORT`
- 权限问题：`sudo chown -R $USER:$USER data/`
- 内存不足：把 Ollama 模型换成更小的

### 模型响应慢

- 检查 GPU 是否被识别：`docker exec openclaw-ollama-1 nvidia-smi`
- 模型太大：换 8B 或量化版本
- 上下文过长：精简 prompt

### 知识库检索不准

- 文档质量：噪音太多会影响 embedding
- 切片大小：默认 500 tokens，可以试试 300 或 800
- Embedding 模型：`nomic-embed-text` 对中文一般，可以换 `bge-large-zh`

### 内存爆掉

```bash
docker stats
```

看哪个容器吃得多。如果 Ollama 吃满，说明模型对硬件要求太高，建议换小模型或升级硬件。

## 性能优化建议

**模型量化**

默认 Q4_K_M 量化已经够用。Q8 质量更好但吃双倍内存，Q4 更快但质量略降。

**上下文管理**

长对话容易爆上下文。开启"自动总结早期消息"功能，定期压缩历史。

**并发限制**

如果同时跑多个 Agent，记得在 `.env` 里设 `MAX_CONCURRENT_REQUESTS`，避免 OOM。

## 写在最后

到这里，你拥有了一个完全本地、可定制、隐私安全的 AI 助理。后续可以慢慢探索：

- 接更多 IM（飞书、微信）
- 写自定义 Python Action
- 调提示词让 AI 更懂你
- 加更多模型做"模型路由"

整个过程从 0 到能用大概 1–2 小时。最大的成本其实不是部署，是选择合适的模型和打磨提示词——这部分没有捷径，需要时间慢慢调。

但一旦跑起来，"自己的 AI 助理"这种感觉，是云端工具给不了的。