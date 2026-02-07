---
title: 'Clawdbot Practical Guide: Building Your Dockerized Personal AI Command Center from Scratch'
description: 'This tutorial will walk you through Clawdbot Docker deployment, Ollama model configuration, Slack integration, and custom Python Action development.'
pubDate: '2026-01-27'
heroImage: '../../../assets/hero-clawdbot.jpg'
---

In the previous deep dive, we learned about the power of Clawdbot (OpenClaw). Today, we'll shed the theoretical coat and deploy this powerful AI assistant to your computer through real code and configuration.

**Prerequisites**: This tutorial requires basic command-line knowledge and Docker Desktop installed on your computer.

## Phase 1: Environment Preparation and Basic Deployment

Clawdbot recommends Docker deployment to isolate environment dependencies from your host machine, keeping your system clean.

### 1.1 Hardware Requirements Check
While Clawdbot itself uses minimal resources, for smooth local large model operation (like Llama 3 8B), we recommend:
*   **Memory (RAM)**: At least 16GB (24GB+ recommended for larger parameter models).
*   **GPU**: NVIDIA RTX 3060 or higher, or Mac M1/M2/M3 series chips (unified memory architecture is very LLM-friendly).
*   **Storage**: At least 50GB free SSD space (for model files).

### 1.2 Install Ollama (Large Model Backend)
Clawdbot is just the brain's cortex; Ollama is the neurons. If your host is Mac or Linux, install Ollama directly:

```bash
# Mac / Linux
curl -fsSL https://ollama.com/install.sh | sh
```

If running Clawdbot in Docker, to allow the container to access the host's Ollama, ensure Ollama listens on all interfaces, not just localhost.
*   **Mac**: Click Ollama icon in menu bar -> Quit. Then run in terminal: `OLLAMA_HOST=0.0.0.0 ollama serve`
*   **Windows**: Set environment variable `OLLAMA_HOST` to `0.0.0.0`, then restart Ollama.

### 1.3 Start Clawdbot Container
Create a `docker-compose.yml` file for better configuration management:

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
      - ./clawdbot_data:/app/data  # Persistent data
      - /var/run/docker.sock:/var/run/docker.sock # Optional: manage other Docker
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434 # Point to host Ollama
      - CLAW_API_KEY=your_secret_key_change_this
```

Run in terminal:
```bash
docker-compose up -d
```
Visit `http://localhost:3000`, you should see Clawdbot's console interface.

## Phase 2: Give It Intelligence (Model Configuration)

Enter console's `Settings` -> `Model Provider`.

1.  **Provider Selection**: Choose `Ollama`.
2.  **Model Pulling**: Back to terminal, download the model first.
    ```bash
    ollama pull llama3
    ollama run llama3
    ```
3.  **Configuration**: In Clawdbot interface, fill Model Name as `llama3`.
4.  **System Prompt (Persona)**: This is key. Enter:
    > "You are Clawdbot, an efficient AI assistant running locally. Your characteristics are concise, precise, and highly executable. Please respond in English."

Click `Test Connection`, if it returns "Success", the brain connection is successful.

## Phase 3: Connect to the World (IM Integration)

Using Slack as an example, as it's most bot-friendly.

### 3.1 Create Slack App
1.  Visit `api.slack.com/apps`, click `Create New App` -> `From scratch`.
2.  On `Socket Mode` page, enable Socket Mode (no public IP needed).
3.  On `OAuth & Permissions` page, add these Scopes:
    *   `app_mentions:read` (allow it to see @)
    *   `chat:write` (allow it to speak)
    *   `files:write` (allow it to send files)
4.  Install App to workspace, get `Bot User OAuth Token` (starts with xoxb-) and `App-Level Token` (starts with xapp-).

### 3.2 Configure Clawdbot
In Clawdbot's `Integrations` -> `Slack` page:
*   **Enabled**: True
*   **App Token**: Fill in xapp-...
*   **Bot Token**: Fill in xoxb-...

Save and restart container. Now @Clawdbot in any Slack channel to see if it responds.

## Phase 4: Advanced Play — Custom Python Actions

This is Clawdbot's killer feature. Let's write an Action: **Query today's GitHub Trending and push to Slack**.

Create `github_trending.py` in `./clawdbot_data/actions` directory:

```python
import requests
from bs4 import BeautifulSoup
from claw_sdk import Action, Context

class GithubTrendingAction(Action):
    name = "get_github_trending"
    description = "Get today's GitHub trending repositories"
    
    def run(self, context: Context):
        url = "https://github.com/trending"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cols = soup.select('article.Box-row')
        
        result_text = "*Today's GitHub Trending Projects*:\\n"
        for i, col in enumerate(cols[:5]): # Only top 5
            repo_name = col.select_one('h1 a').text.strip().replace('\\n', '').replace(' ', '')
            desc = col.select_one('p.col-9').text.strip() if col.select_one('p.col-9') else "No description"
            result_text += f"{i+1}. *{repo_name}*: {desc}\\n"
            
        return result_text
```

Restart Clawdbot. Now you can say: "What's trending on GitHub today?", it will call this Python script, scrape data, and send you formatted results.

## Troubleshooting

1.  **Can't connect to Ollama**: 99% network issue. Check if `host.docker.internal` works on your system (Linux users might need `172.17.0.1`).
2.  **Extremely slow response**: Check CPU/GPU usage. If model is too large (like 70B) with insufficient VRAM, it switches to pure CPU mode, dropping to 0.5 token/s. Recommend switching back to Llama 3 8B or Phi-3.
3.  **Missing Python dependencies**: If your script uses `requests` or `bs4`, enter container to install:
    ```bash
    docker exec -it my-clawdbot pip install requests beautifulsoup4
    ```

## Conclusion

Congratulations! You now have a fully local, programmable, extensible AI hub. This isn't just a tool installation process, but your first step from AI consumer to AI creator. Go explore, write more Actions, and make Clawdbot truly the commander of your digital life.
