---
title: 'Clawdbot 实战指南：从零打造你的 Docker 化私人 AI 指挥中心'
description: '本教程将手把手带你完成 Clawdbot 的 Docker 部署、Ollama 模型配置、Slack 集成以及自定义 Python Action 的编写。'
pubDate: '2026-01-27'
heroImage: '../../assets/hero-clawdbot.jpg'
---

在上一篇深度解析中，我们了解了 Clawdbot (OpenClaw) 的强大之处。今天，我们将脱去理论的外衣，通过实实在在的代码和配置，把这个强大的 AI 助手部署到你的电脑上。

**前置知识**：本教程需要你了解基本的命令行操作，并且电脑上已安装 Docker Desktop。

## 第一阶段：环境准备与基础部署

Clawdbot 推荐使用 Docker 部署，这样可以将环境依赖与你的宿主机隔离开，保持系统清洁。

### 1.1 硬件要求检查
虽然 Clawdbot 本身占用资源极小，但为了流畅运行本地大模型（如 Llama 3 8B），我们建议：
*   **内存 (RAM)**：至少 16GB（推荐 24GB 以上，以便运行更大参数的模型）。
*   **显卡 (GPU)**：NVIDIA RTX 3060 以上，或 Mac M1/M2/M3 系列芯片（统一内存架构对 LLM 非常友好）。
*   **存储**：至少 50GB 空闲 SSD 空间（用于存放模型文件）。

### 1.2 安装 Ollama（大模型后端）
Clawdbot 只是大脑的皮层，Ollama 才是神经元。如果你的宿主机是 Mac 或 Linux，直接安装 Ollama：

```bash
# Mac / Linux
curl -fsSL https://ollama.com/install.sh | sh
```

如果你是在 Docker 中运行 Clawdbot，为了让容器内的 Clawdbot 能访问宿主机的 Ollama，你需要确保 Ollama 监听所有接口，而不仅仅是 localhost。
*   **Mac**: 在顶部菜单栏点击 Ollama 图标 -> Quit。然后在终端运行：`OLLAMA_HOST=0.0.0.0 ollama serve`
*   **Windows**: 设置环境变量 `OLLAMA_HOST` 为 `0.0.0.0`，然后重启 Ollama。

### 1.3 启动 Clawdbot 容器
创建一个 `docker-compose.yml` 文件，以便更好地管理配置：

```yaml
version: '3.8'
services:
  clawdbot:
    image: openclaw/core:latest
    container_name: my-clawdbot
    restart: always
    ports:
      - "3000:3000"
    volumes:
      - ./clawdbot_data:/app/data  # 持久化数据
      - /var/run/docker.sock:/var/run/docker.sock # 可选：让它能管理其他 Docker
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434 # 指向宿主机 Ollama
      - CLAW_API_KEY=your_secret_key_change_this
```

在终端运行：
```bash
docker-compose up -d
```
访问 `http://localhost:3000`，你应该能看到 Clawdbot 的控制台界面。

## 第二阶段：赋予它智慧 (模型配置)

进入控制台的 `Settings` -> `Model Provider`。

1.  **Provider Selection**: 选择 `Ollama`。
2.  **Model Pulling**: 回到终端，我们需要先下载模型。
    ```bash
    ollama pull llama3
    ollama run llama3
    ```
3.  **Configuration**: 在 Clawdbot 界面填写 Model Name 为 `llama3`。
4.  **System Prompt (人设)**：这是关键。输入：
    > "你叫 Clawdbot，是一个运行在本地的高效 AI 助手。你的特点是话少、精准、执行力强。回答请使用中文。"

点击 `Test Connection`，如果返回 "Success"，说明大脑连接成功。

## 第三阶段：连接世界 (IM 集成)

这里以 Slack 为例，因为它对 Bot 最友好。

### 3.1 创建 Slack App
1.  访问 `api.slack.com/apps`，点击 `Create New App` -> `From scratch`。
2.  在 `Socket Mode` 页面，开启 Socket Mode（这样你不需要公网 IP）。
3.  在 `OAuth & Permissions` 页面，添加以下 Scope：
    *   `app_mentions:read` (允许它看到@)
    *   `chat:write` (允许它说话)
    *   `files:write` (允许它发文件)
4.  安装 App 到工作区，获取 `Bot User OAuth Token` (以 xoxb- 开头) 和 `App-Level Token` (以 xapp- 开头)。

### 3.2 配置 Clawdbot
在 Clawdbot 的 `Integrations` -> `Slack` 页面：
*   **Enabled**: True
*   **App Token**: 填入 xapp-...
*   **Bot Token**: 填入 xoxb-...

保存后重启容器。现在，在 Slack 的任意频道 @Clawdbot，看它是否会回复你。

## 第四阶段：高阶玩法 —— 自定义 Python Actions

这是 Clawdbot 的杀手锏。我们来写一个 Action：**查询今日 GitHub Trending 并推送到 Slack**。

在 `./clawdbot_data/actions` 目录下新建 `github_trending.py`：

```python
import requests
from bs4 import BeautifulSoup
from claw_sdk import Action, Context

class GithubTrendingAction(Action):
    name = "get_github_trending"
    description = "获取 GitHub 今日热门仓库"
    
    def run(self, context: Context):
        url = "https://github.com/trending"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cols = soup.select('article.Box-row')
        
        result_text = "*今日 GitHub 热门项目*:\n"
        for i, col in enumerate(cols[:5]): # 只取前5个
            repo_name = col.select_one('h1 a').text.strip().replace('\n', '').replace(' ', '')
            desc = col.select_one('p.col-9').text.strip() if col.select_one('p.col-9') else "无描述"
            result_text += f"{i+1}. *{repo_name}*: {desc}\n"
            
        return result_text
```

重启 Clawdbot。现在你可以对它说：“看看今天 GitHub 上有什么热门项目？”，它会调用这个 Python 脚本，抓取数据，并把格式化好的结果发给你。

## 常见问题排查 (Troubleshooting)

1.  **连接不上 Ollama**: 99% 是因为网络问题。请重点检查 `host.docker.internal` 在你的系统上是否可用（Linux 用户可能需要用 `172.17.0.1`）。
2.  **响应极其缓慢**: 检查你的 CPU/GPU 占用率。如果模型过大（如 70B）而显存不足，会切到纯 CPU 模式，速度会跌至 0.5 token/s。建议换回 Llama 3 8B 或 Phi-3。
3.  **Python 依赖缺失**: 如果你的脚本用到 `requests` 或 `bs4`，你需要进入容器安装它们：
    ```bash
    docker exec -it my-clawdbot pip install requests beautifulsoup4
    ```

## 结语

恭喜！你现在拥有了一个完全运行在本地、可编程、可扩展的 AI 中枢。这不仅仅是一个工具的安装过程，更是你从 AI 消费者向 AI 创造者转变的第一步。去探索吧，编写更多的 Action，让 Clawdbot 真正成为你数字生活的指挥官。
