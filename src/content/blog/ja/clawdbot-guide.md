---
title: 'Clawdbot実践ガイド：ゼロからDockerized個人AIコマンドセンターを構築'
description: 'このチュートリアルでは、ClawdbotのDocker展開、Ollamaモデル設定、Slack統合、カスタムPython Actionの作成を手順を追って説明します。'
pubDate: '2026-01-27'
heroImage: '../../../assets/hero-clawdbot.jpg'
---

前回の詳細分析で、Clawdbot（OpenClaw）の強力さを理解しました。今日は、理論の外套を脱ぎ、実際のコードと設定を通じて、この強力なAIアシスタントをあなたのコンピューターに展開します。

**前提知識**：このチュートリアルでは、基本的なコマンドライン操作の知識が必要で、コンピューターにDocker Desktopがインストールされている必要があります。

## フェーズ1：環境準備と基本展開

Clawdbotは、環境依存関係をホストマシンから分離してシステムをクリーンに保つため、Docker展開を推奨しています。

### 1.1 ハードウェア要件チェック
Clawdbot自体は最小限のリソースしか使用しませんが、ローカル大規模モデル（Llama 3 8Bなど）をスムーズに実行するには、以下を推奨します：
*   **メモリ（RAM）**：最低16GB（より大きなパラメータモデルには24GB以上を推奨）。
*   **GPU**：NVIDIA RTX 3060以上、またはMac M1/M2/M3シリーズチップ（統合メモリアーキテクチャはLLMに非常に適しています）。
*   **ストレージ**：最低50GBの空きSSDスペース（モデルファイル用）。

### 1.2 Ollamaのインストール（大規模モデルバックエンド）
Clawdbotは脳の皮質に過ぎず、Ollamaがニューロンです。ホストがMacまたはLinuxの場合、Ollamaを直接インストールします：

```bash
# Mac / Linux
curl -fsSL https://ollama.com/install.sh | sh
```

DockerでClawdbotを実行している場合、コンテナ内のClawdbotがホストのOllamaにアクセスできるようにするには、Ollamaがlocalhostだけでなくすべてのインターフェースでリッスンするようにします。
*   **Mac**：メニューバーのOllamaアイコンをクリック -> 終了。次にターミナルで実行：`OLLAMA_HOST=0.0.0.0 ollama serve`
*   **Windows**：環境変数`OLLAMA_HOST`を`0.0.0.0`に設定し、Ollamaを再起動。

### 1.3 Clawdbotコンテナの起動
より良い設定管理のために`docker-compose.yml`ファイルを作成します：

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
      - ./clawdbot_data:/app/data  # 永続データ
      - /var/run/docker.sock:/var/run/docker.sock # オプション：他のDockerを管理
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434 # ホストOllamaを指す
      - CLAW_API_KEY=your_secret_key_change_this
```

ターミナルで実行：
```bash
docker-compose up -d
```
`http://localhost:3000`にアクセスすると、Clawdbotのコンソールインターフェースが表示されるはずです。

## フェーズ2：知性を与える（モデル設定）

コンソールの`Settings` -> `Model Provider`に入ります。

1.  **Provider Selection**：`Ollama`を選択。
2.  **Model Pulling**：ターミナルに戻り、まずモデルをダウンロードします。
    ```bash
    ollama pull llama3
    ollama run llama3
    ```
3.  **Configuration**：ClawdbotインターフェースでModel Nameを`llama3`と入力。
4.  **System Prompt（ペルソナ）**：これが鍵です。入力：
    > "あなたはClawdbotで、ローカルで実行される効率的なAIアシスタントです。あなたの特徴は簡潔、正確、実行力が高いことです。日本語で応答してください。"

`Test Connection`をクリックし、"Success"が返されれば、脳の接続が成功です。

## フェーズ3：世界とつながる（IM統合）

ここではSlackを例にします。最もボットフレンドリーだからです。

### 3.1 Slack Appの作成
1.  `api.slack.com/apps`にアクセスし、`Create New App` -> `From scratch`をクリック。
2.  `Socket Mode`ページで、Socket Modeを有効化（パブリックIPは不要）。
3.  `OAuth & Permissions`ページで、以下のScopeを追加：
    *   `app_mentions:read`（@を見ることを許可）
    *   `chat:write`（話すことを許可）
    *   `files:write`（ファイルを送ることを許可）
4.  Appをワークスペースにインストールし、`Bot User OAuth Token`（xoxb-で始まる）と`App-Level Token`（xapp-で始まる）を取得。

### 3.2 Clawdbotの設定
Clawdbotの`Integrations` -> `Slack`ページで：
*   **Enabled**：True
*   **App Token**：xapp-...を入力
*   **Bot Token**：xoxb-...を入力

保存してコンテナを再起動。Slackの任意のチャンネルで@Clawdbotして、応答するか確認。

## フェーズ4：高度な使い方 — カスタムPython Actions

これがClawdbotの切り札です。Actionを書きましょう：**今日のGitHub Trendingを照会してSlackにプッシュ**。

`./clawdbot_data/actions`ディレクトリに`github_trending.py`を作成：

```python
import requests
from bs4 import BeautifulSoup
from claw_sdk import Action, Context

class GithubTrendingAction(Action):
    name = "get_github_trending"
    description = "今日のGitHub人気リポジトリを取得"
    
    def run(self, context: Context):
        url = "https://github.com/trending"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cols = soup.select('article.Box-row')
        
        result_text = "*今日のGitHub人気プロジェクト*:\\n"
        for i, col in enumerate(cols[:5]): # トップ5のみ
            repo_name = col.select_one('h1 a').text.strip().replace('\\n', '').replace(' ', '')
            desc = col.select_one('p.col-9').text.strip() if col.select_one('p.col-9') else "説明なし"
            result_text += f"{i+1}. *{repo_name}*: {desc}\\n"
            
        return result_text
```

Clawdbotを再起動。「今日GitHubで何が人気？」と言えば、このPythonスクリプトを呼び出し、データをスクレイピングし、フォーマットされた結果を送信します。

## トラブルシューティング

1.  **Ollamaに接続できない**：99%ネットワークの問題。`host.docker.internal`がシステムで機能するか確認（Linuxユーザーは`172.17.0.1`が必要かも）。
2.  **非常に遅い応答**：CPU/GPU使用率を確認。モデルが大きすぎる（70Bなど）でVRAMが不足している場合、純粋なCPUモードに切り替わり、0.5 token/sに低下。Llama 3 8BまたはPhi-3への切り替えを推奨。
3.  **Python依存関係の欠落**：スクリプトが`requests`や`bs4`を使用する場合、コンテナに入ってインストール：
    ```bash
    docker exec -it my-clawdbot pip install requests beautifulsoup4
    ```

## 結論

おめでとうございます！完全にローカルで、プログラム可能で、拡張可能なAIハブを手に入れました。これは単なるツールのインストールプロセスではなく、AI消費者からAIクリエイターへの転換の第一歩です。探索し、より多くのActionを書き、Clawdbotを本当にあなたのデジタルライフの司令官にしましょう。
