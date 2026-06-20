---
title: 'Clawdbot 部署指南：手把手搭一个 Docker 化的私人 AI 指挥中心'
description: '这篇是 Clawdbot (OpenClaw) 的实战教程，从硬件准备、Ollama 安装、Docker 部署，到 Slack 集成、自定义 Python Action，每一步都附带具体操作。'
pubDate: '2026-01-27'
heroImage: '../../../assets/hero-clawdbot.jpg'
---

上一篇我们聊了 Clawdbot 的架构和定位，这篇把袖子撸起来，实际把它部署到你的机器上。

**前置**：基本的命令行操作，电脑上已安装 Docker Desktop。

## 第一阶段：环境准备

### 硬件要求

Clawdbot 本身很轻，但要流畅跑本地大模型（比如 Llama 3 8B），建议：

- **内存**：至少 16GB，跑更大模型建议 24GB 以上
- **显卡**：NVIDIA RTX 3060 以上，或者 Mac M1/M2/M3 系列（统一内存架构对 LLM 友好）
- **存储**：至少 50GB 空闲 SSD（放模型文件）

### 装 Ollama（大模型后端）

Ollama 才是神经元，Clawdbot 是皮层。Mac/Linux 直接装：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

如果用 Docker 跑 Clawdbot，容器内的它要访问宿主机的 Ollama。Ollama 默认只监听 localhost，需要改成监听所有接口：

- **Mac**：菜单栏点 Ollama 图标 → Quit，然后 `OLLAMA_HOST=0.0.0.0 ollama serve`
- **Windows**：设置环境变量 `OLLAMA_HOST=0.0.0.0`，重启 Ollama

### 启动 Clawdbot 容器

写一个 `docker-compose.yml`：

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
      - ./clawdbot_data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
      - CLAW_API_KEY=your_secret_key_change_this
```

跑起来：

```bash
docker-compose up -d
```

访问 `http://localhost:3000`，应该能看到控制台。

## 第二阶段：接入大脑（模型配置）

进控制台 `Settings` → `Model Provider`：

1. **Provider Selection**：选 `Ollama`
2. **Model Pulling**：回到终端下载模型
   ```bash
   ollama pull llama3
   ollama run llama3
   ```
3. **Configuration**：界面里填 Model Name `llama3`
4. **System Prompt**（人设）很关键，输入：
   > 你叫 Clawdbot，是一个运行在本地的高效 AI 助手。你的特点是话少、精准、执行力强。回答使用中文。

点 `Test Connection`，返回 Success 说明大脑连接成功。

## 第三阶段：连接世界（IM 集成）

我用 Slack 做示例，因为它对 Bot 最友好。

### 创建 Slack App

1. 访问 `api.slack.com/apps`，点 `Create New App` → `From scratch`
2. `Socket Mode` 页面开启 Socket Mode（这样你不需要公网 IP）
3. `OAuth & Permissions` 加这几个 Scope：
   - `app_mentions:read`（让它看到 @）
   - `chat:write`（让它说话）
   - `files:write`（让它发文件）
4. 装到工作区，拿到 `Bot User OAuth Token`（xoxb- 开头）和 `App-Level Token`（xapp- 开头）

### 配置 Clawdbot

`Integrations` → `Slack`：

- Enabled: True
- App Token: xapp-...
- Bot Token: xoxb-...

保存后重启容器。在 Slack 任意频道 @Clawdbot 看会不会回复。

## 第四阶段：自定义 Python Action

这是 Clawdbot 的杀手锏——我们写一个"查询今日 GitHub Trending 推送到 Slack"的 Action。

在 `./clawdbot_data/actions/` 下新建 `github_trending.py`：

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
        for i, col in enumerate(cols[:5]):
            repo_name = col.select_one('h1 a').text.strip().replace('\n', '').replace(' ', '')
            desc = col.select_one('p.col-9').text.strip() if col.select_one('p.col-9') else "无描述"
            result_text += f"{i+1}. *{repo_name}*: {desc}\n"

        return result_text
```

重启 Clawdbot。现在你可以对它说："看看今天 GitHub 上有什么热门项目？" 它会调用这个脚本、抓数据、格式化结果返回给你。

## 常见问题排查

**连接不上 Ollama**：99% 是网络问题。重点检查 `host.docker.internal` 在你的系统上是否可用（Linux 用户可能要用 `172.17.0.1`）。

**响应极慢**：检查 CPU/GPU 占用。模型过大（70B）而显存不足时会切到纯 CPU 模式，速度跌到 0.5 token/s。建议换回 Llama 3 8B 或 Phi-3。

**Python 依赖缺失**：脚本用到 `requests` 或 `bs4` 时，进容器手动装：

```bash
docker exec -it my-clawdbot pip install requests beautifulsoup4
```

## 收尾

到这里，你拥有了一个完全本地、可编程、可扩展的 AI 中枢。这不只是一个工具的安装过程，更是从"AI 消费者"变成"AI 创造者"的第一步。

接下来去探索吧，多写几个 Action，让 Clawdbot 真正成为你数字生活的指挥官。