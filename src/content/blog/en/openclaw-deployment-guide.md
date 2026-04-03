---
title: 'Complete OpenClaw Deployment Guide: Building Your Local AI Assistant from Scratch'
description: 'A step-by-step tutorial on deploying OpenClaw (formerly Clawdbot) locally, including environment setup, Docker deployment, model configuration, plugin installation, and troubleshooting. Even without deep technical background, you can easily own your own AI assistant.'
pubDate: 2026-04-03
heroImage: '../../../assets/hero-clawdbot.jpg'
category: 'Tutorial'
---

In our previous article, we introduced the technical architecture and core features of OpenClaw (formerly Clawdbot). Today, we'll dive into the practical implementation, guiding you step-by-step to deploy this powerful local AI assistant from scratch.

## Prerequisites

Before we begin, ensure your system meets the following basic requirements:

### Hardware Requirements
- **CPU**: 4 cores or above (8 cores recommended)
- **RAM**: 16GB or above (32GB recommended)
- **Storage**: At least 50GB free space (for models and vector database)
- **GPU** (optional but highly recommended):
  - NVIDIA GPU: CUDA 11.0+ support (RTX 3060 or above)
  - Apple Silicon: M1/M2/M3/M4 chips (Unified Memory 16GB+)

### Software Requirements
- **Operating System**: Linux / macOS / Windows (WSL2)
- **Docker**: 20.10.0 or above
- **Docker Compose**: 2.0.0 or above
- **Git**: For cloning the project repository

## Step 1: Environment Preparation

### 1.1 Install Docker

#### macOS
```bash
# Install using Homebrew
brew install --cask docker

# Or download the official installer
# Visit https://www.docker.com/products/docker-desktop
```

#### Ubuntu/Debian Linux
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
sudo docker run hello-world
```

#### Windows (WSL2)
1. Enable WSL2: Run PowerShell as administrator
```powershell
wsl --install
```
2. Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
3. Restart your computer

### 1.2 Install Ollama (Local LLM Runtime)

OpenClaw relies on Ollama to run local large language models.

#### macOS / Linux
```bash
# Use official installation script
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

#### Windows
```powershell
# Download official installer
# Visit https://ollama.com/download
```

## Step 2: Clone OpenClaw Project

```bash
# Clone repository
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# View project structure
ls -la
```

Project structure:
```
openclaw/
├── docker-compose.yml      # Docker orchestration config
├── config/                 # Configuration directory
│   ├── config.yaml        # Main configuration file
│   ├── prompts/           # System prompts
│   └── actions/           # Custom action scripts
├── integrations/          # Integration plugins
├── data/                  # Data directory (vector DB, etc.)
└── README.md
```

## Step 3: Configure OpenClaw

### 3.1 Edit Main Configuration File

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Open with your favorite editor
vim config/config.yaml
```

Key configuration parameters explained:

```yaml
# LLM Configuration
llm:
  provider: ollama          # Use Ollama as provider
  model: llama3:8b         # Default model (adjust based on hardware)
  base_url: http://ollama:11434  # Ollama service address
  temperature: 0.7         # Generation temperature
  max_tokens: 2048         # Max generation length

# Vector Database Configuration
vector_db:
  provider: qdrant         # Use Qdrant
  url: http://qdrant:6333  # Qdrant service address
  collection_name: openclaw_kb

# Integration Configuration
integrations:
  slack:
    enabled: true
    bot_token: "xoxb-your-slack-bot-token"  # Your Slack Bot Token
    app_token: "xapp-your-slack-app-token"
  telegram:
    enabled: false
    bot_token: ""          # Fill in if enabling

# Action Configuration
actions:
  enabled: true
  allowed_paths:           # Restrict accessible paths (security)
    - /home/user/documents
    - /home/user/downloads
  shell_enabled: true      # Allow shell command execution
```

### 3.2 Get Slack Bot Token (using Slack as example)

1. Visit [Slack API](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Fill in App name and select workspace
4. In "OAuth & Permissions" page:
   - Add Bot Token Scopes: `chat:write`, `channels:history`, `im:history`, `app_mentions:read`
5. Install App to workspace, get `Bot User OAuth Token`
6. Enable Socket Mode and get `App-Level Token`

## Step 4: Launch OpenClaw

### 4.1 Pull Docker Images and Start Services

```bash
# Execute from project root
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f openclaw
```

First launch will automatically download required Docker images (about 5-10 minutes, depending on network speed).

### 4.2 Download and Run LLM Models

```bash
# Enter Ollama container
docker exec -it openclaw-ollama bash

# Download model (using Llama 3 8B as example)
ollama pull llama3:8b

# Test model
ollama run llama3:8b "Hello, OpenClaw!"

# Exit container
exit
```

Model size reference:
- `llama3:8b`: ~4.7GB (suitable for 16GB RAM devices)
- `llama3:70b`: ~40GB (requires 32GB+ RAM)

## Step 5: Verify Deployment

### 5.1 Check All Services Status

```bash
# Check container status
docker-compose ps

# You should see these containers running:
# openclaw-core       # Main service
# openclaw-ollama     # LLM runtime
# openclaw-qdrant     # Vector database
# openclab-redis      # Cache (optional)
```

### 5.2 Test Slack Integration

1. Find your App in Slack
2. Send message: "Hello, OpenClaw!"
3. If configured correctly, you should receive a reply like:

> "Hello! I'm OpenClaw, your local AI assistant. I can help you process messages, manage knowledge bases, and execute automation tasks. How can I help you?"

### 5.3 Test Knowledge Base Feature

```bash
# Send command to OpenClaw:
"/kb-add https://example.com/article.html"

# Wait for processing, then ask:
"What was that article about?"
```

## Step 6: Configure Advanced Features

### 6.1 Enable Personal Knowledge Base (RAG)

```bash
# Prepare your documents
mkdir -p data/documents
cp ~/Documents/*.pdf data/documents/

# Send in Slack:
"/kb-index /data/documents"
```

OpenClaw will automatically vectorize documents and store them in Qdrant.

### 6.2 Create Custom Action

Create a simple weather query action:

```bash
# Edit action script
vim config/actions/get_weather.py
```

```python
#!/usr/bin/env python3
import requests
import sys

def get_weather(city):
    """Get weather information for specified city"""
    # Using free weather API
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current = data['current_condition'][0]
        return f"{city} current weather: {current['weatherDesc'][0]['value']}, temp {current['temp_C']}°C"
    return f"Unable to get weather for {city}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        print(get_weather(city))
    else:
        print("Please provide city name")
```

```bash
# Add execute permission
chmod +x config/actions/get_weather.py

# Restart OpenClaw service
docker-compose restart openclaw

# Test in Slack:
"/action get_weather Beijing"
```

### 6.3 Configure Automation Tasks

Edit `config/automations.yaml`:

```yaml
automations:
  - name: "Daily Morning Briefing"
    trigger:
      type: schedule
      cron: "0 9 * * 1-5"  # 9 AM, weekdays
    actions:
      - type: message
        target: slack
        channel: "#general"
        template: "morning_briefing"

  - name: "Cross-Platform Message Summary"
    trigger:
      type: schedule
      cron: "0 18 * * *"  # 6 PM daily
    actions:
      - type: summary
        sources: [slack, telegram]
        target: slack
        channel: "#daily-summary"
```

## Step 7: Troubleshooting Common Issues

### Issue 1: Ollama Model Download Fails

**Symptoms**: Error when executing `ollama pull`

**Solution**:
```bash
# Use mirror acceleration
export OLLAMA_MIRROR=https://ollama.registry.example.com
ollama pull llama3:8b
```

### Issue 2: Slack Bot Not Responding

**Checklist**:
1. Bot Token correctly configured
2. Socket Mode enabled
3. Required scopes added
4. Check logs: `docker-compose logs openclaw | grep slack`

### Issue 3: Insufficient Memory

**Symptoms**: System slows down, containers killed

**Solution**:
1. Use smaller model: `llama3:8b` → `mistral:7b` → `gemma:2b`
2. Limit Docker memory usage:
```yaml
# In docker-compose.yml
services:
  openclaw:
    deploy:
      resources:
        limits:
          memory: 8G
```

### Issue 4: Vector Database Query Slow

**Solution**:
```bash
# Restart Qdrant with optimization
docker-compose restart qdrant

# Consider using smaller embedding model
# Edit config.yaml
embeddings:
  model: "nomic-embed-text"  # Smaller, faster embedding model
```

## Step 8: Performance Optimization Tips

### 8.1 GPU Acceleration (if NVIDIA GPU available)

```bash
# Install NVIDIA Container Toolkit
sudo apt-get install -y nvidia-container-toolkit

# Configure Docker to use NVIDIA runtime
sudo nvidia-ctk runtime configure --runtime=docker

# Restart Docker
sudo systemctl restart docker

# Modify docker-compose.yml
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

### 8.2 Adjust Model Parameters

In `config/config.yaml`:
```yaml
llm:
  max_tokens: 1024        # Reduce max generation length (faster but may truncate)
  temperature: 0.5        # Lower temperature (more deterministic output)
  context_window: 4096    # Adjust context window as needed
```

### 8.3 Enable Caching

```yaml
# In config.yaml
cache:
  enabled: true
  provider: redis         # Use Redis as cache
  ttl: 3600              # Cache for 1 hour
```

## Advanced: Multi-Model Deployment

If you have sufficient hardware resources, you can run multiple models for different scenarios:

```yaml
# config.yaml
llm:
  models:
    default: llama3:8b
    fast: mistral:7b           # For quick responses
    creative: llama3:70b       # For complex tasks
    code: :33b   # For code generation

  routing_rules:
    - if: context.includes("code")
      use: code
    - if: context.length > 1000
      use: creative
    - else: fast
```

## Security Recommendations

1. **Network Isolation**: If possible, deploy OpenClaw in an isolated network
2. **Regular Updates**: Regularly pull latest images and code
```bash
git pull
docker-compose pull
docker-compose up -d --build
```
3. **Backup Configuration**: Regularly backup `config/` and `data/` directories
4. **Monitor Logs**: Set up log monitoring to detect anomalies early

## Summary

Through these steps, you've successfully deployed your own OpenClaw local AI assistant. You can now:

- ✅ Interact with AI in Slack/Telegram
- ✅ Build and query personal knowledge bases
- ✅ Execute local automation tasks
- ✅ Create custom Actions
- ✅ Configure automated workflows

The power of OpenClaw lies in its extensibility. As your needs grow, you can continuously add new integrations, create more complex Actions, and optimize model configurations.

**Next Steps**:
- Try integrating other communication platforms (Discord, WhatsApp)
- Explore more plugins from the [OpenClaw community](https://github.com/openclaw/openclaw)
- Share your custom Actions with the community

If you encounter any issues during deployment, feel free to ask in GitHub Issues, or check our [complete documentation](https://docs.openclaw.dev).

Happy Hacking! 🚀
