---
title: 'OpenClaw導入完全ガイド：ゼロから構築するローカルAIアシスタント'
description: 'OpenClaw（旧Clawdbot）のローカル展開方法をステップバイステップで解説。環境準備、Docker導入、モデル設定、プラグインインストール、トラブルシューティングまでカバー。深い技術背景がなくても、簡単に自分だけのAIアシスタントを持てます。'
pubDate: 2026-04-03
heroImage: '../../../assets/hero-clawdbot.jpg'
category: '技術チュートリアル'
---

前回の記事では、OpenClaw（旧Clawdbot）の技術アーキテクチャとコア機能について紹介しました。今回は実践編として、この強力なローカルAIアシスタントをゼロから導入する方法をステップバイステップで解説します。

## 前提条件

始める前に、お使いのシステムが以下の基本要件を満たしていることを確認してください。

### ハードウェア要件
- **CPU**: 4コア以上（8コア推奨）
- **メモリ**: 16GB以上（32GB推奨）
- **ストレージ**: 50GB以上の空き容量（モデルとベクトルデータベース用）
- **GPU**（オプションだが強く推奨）:
  - NVIDIA GPU: CUDA 11.0+対応（RTX 3060以上）
  - Apple Silicon: M1/M2/M3/M4チップ（ユニファイドメモリ16GB+）

### ソフトウェア要件
- **OS**: Linux / macOS / Windows (WSL2)
- **Docker**: 20.10.0以上
- **Docker Compose**: 2.0.0以上
- **Git**: プロジェクトリポジトリのクローン用

## ステップ1：環境準備

### 1.1 Dockerのインストール

#### macOS
```bash
# Homebrewでインストール
brew install --cask docker

# または公式インストーラーをダウンロード
# https://www.docker.com/products/docker-desktop
```

#### Ubuntu/Debian Linux
```bash
# パッケージインデックスを更新
sudo apt-get update

# 依存関係をインストール
sudo apt-get install ca-certificates curl gnupg

# Dockerの公式GPGキーを追加
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# リポジトリを設定
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Docker Engineをインストール
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# インストールを確認
sudo docker run hello-world
```

#### Windows (WSL2)
1. WSL2を有効化：管理者権限でPowerShellを実行
```powershell
wsl --install
```
2. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)をダウンロードしてインストール
3. コンピューターを再起動

### 1.2 Ollamaのインストール（ローカルLLMランタイム）

OpenClawは、ローカル大規模言語モデルの実行にOllamaを使用します。

#### macOS / Linux
```bash
# 公式インストールスクリプトを使用
curl -fsSL https://ollama.com/install.sh | sh

# インストールを確認
ollama --version
```

#### Windows
```powershell
# 公式インストーラーをダウンロード
# https://ollama.com/download
```

## ステップ2：OpenClawプロジェクトのクローン

```bash
# リポジトリをクローン
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# プロジェクト構造を確認
ls -la
```

プロジェクト構造：
```
openclaw/
├── docker-compose.yml      # Dockerオーケストレーション設定
├── config/                 # 設定ファイルディレクトリ
│   ├── config.yaml        # メイン設定ファイル
│   ├── prompts/           # システムプロンプト
│   └── actions/           # カスタムアクションスクリプト
├── integrations/          # 統合プラグイン
├── data/                  # データディレクトリ（ベクトルDB等）
└── README.md
```

## ステップ3：OpenClawの設定

### 3.1 メイン設定ファイルの編集

```bash
# サンプル設定をコピー
cp config/config.example.yaml config/config.yaml

# お好みのエディタで開く
vim config/config.yaml
```

主な設定パラメータの説明：

```yaml
# LLM設定
llm:
  provider: ollama          # Ollamaをプロバイダーとして使用
  model: llama3:8b         # デフォルトモデル（ハードウェアに応じて調整）
  base_url: http://ollama:11434  # Ollamaサービスアドレス
  temperature: 0.7         # 生成温度
  max_tokens: 2048         # 最大生成長

# ベクトルデータベース設定
vector_db:
  provider: qdrant         # Qdrantを使用
  url: http://qdrant:6333  # Qdrantサービスアドレス
  collection_name: openclaw_kb

# 統合設定
integrations:
  slack:
    enabled: true
    bot_token: "xoxb-your-slack-bot-token"  # あなたのSlack Bot Token
    app_token: "xapp-your-slack-app-token"
  telegram:
    enabled: false
    bot_token: ""          # 有効にする場合に入力

# アクション設定
actions:
  enabled: true
  allowed_paths:           # アクセス可能なパスを制限（セキュリティ）
    - /home/user/documents
    - /home/user/downloads
  shell_enabled: true      # シェルコマンド実行を許可
```

### 3.2 Slack Bot Tokenの取得（Slack統合の場合）

1. [Slack API](https://api.slack.com/apps)にアクセス
2. 「Create New App」→「From scratch」をクリック
3. アプリ名とワークスペースを入力
4. 「OAuth & Permissions」ページで：
   - Bot Token Scopesを追加：`chat:write`, `channels:history`, `im:history`, `app_mentions:read`
5. アプリをワークスペースにインストールし、`Bot User OAuth Token`を取得
6. Socket Modeを有効にし、`App-Level Token`を取得

## ステップ4：OpenClawの起動

### 4.1 Dockerイメージのプルとサービス起動

```bash
# プロジェクトルートから実行
docker-compose up -d

# サービス状態を確認
docker-compose ps

# ログを確認
docker-compose logs -f openclaw
```

初回起動時に必要なDockerイメージが自動的にダウンロードされます（約5〜10分、ネットワーク速度によります）。

### 4.2 LLMモデルのダウンロードと実行

```bash
# Ollamaコンテナに入る
docker exec -it openclaw-ollama bash

# モデルをダウンロード（Llama 3 8Bを例に）
ollama pull llama3:8b

# モデルをテスト
ollama run llama3:8b "こんにちは、OpenClaw！"

# コンテナを終了
exit
```

モデルサイズの参考：
- `llama3:8b`: 約4.7GB（16GBメモリのデバイスに適している）
- `llama3:70b`: 約40GB（32GB以上のメモリが必要）

## ステップ5：導入の確認

### 5.1 すべてのサービスの状態を確認

```bash
# コンテナ状態を確認
docker-compose ps

# 以下のコンテナが実行されているはず：
# openclaw-core       # メインサービス
# openclaw-ollama     # LLMランタイム
# openclaw-qdrant     # ベクトルデータベース
# openclab-redis      # キャッシュ（オプション）
```

### 5.2 Slack統合のテスト

1. Slackでアプリを見つける
2. メッセージを送信：「こんにちは、OpenClaw！」
3. 設定が正しければ、以下のような返信が届きます：

> 「こんにちは！私はOpenClaw、あなたのローカルAIアシスタントです。メッセージ処理、ナレッジベース管理、自動化タスクの実行を手伝えます。何かお手伝いできることはありますか？」

### 5.3 ナレッジベース機能のテスト

```bash
# OpenClawにコマンドを送信：
"/kb-add https://example.com/article.html"

# 処理完了後、質問：
"あの記事は何についてでしたか？"
```

## ステップ6：高度な機能の設定

### 6.1 パーソナルナレッジベース（RAG）の有効化

```bash
# ドキュメントを準備
mkdir -p data/documents
cp ~/Documents/*.pdf data/documents/

# Slackで送信：
"/kb-index /data/documents"
```

OpenClawは自動的にドキュメントをベクトル化し、Qdrantに保存します。

### 6.2 カスタムアクションの作成

天気検索アクションを作成してみましょう：

```bash
# アクションスクリプトを編集
vim config/actions/get_weather.py
```

```python
#!/usr/bin/env python3
import requests
import sys

def get_weather(city):
    """指定された都市の天気情報を取得"""
    # 無料の天気APIを使用
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        current = data['current_condition'][0]
        return f"{city}の現在の天気：{current['weatherDesc'][0]['value']}、気温{current['temp_C']}°C"
    return f"{city}の天気を取得できませんでした"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        print(get_weather(city))
    else:
        print("都市名を入力してください")
```

```bash
# 実行権限を追加
chmod +x config/actions/get_weather.py

# OpenClawサービスを再起動
docker-compose restart openclaw

# Slackでテスト：
"/action get_weather Tokyo"
```

### 6.3 自動化タスクの設定

`config/automations.yaml`を編集：

```yaml
automations:
  - name: "毎朝のブリーフィング"
    trigger:
      type: schedule
      cron: "0 9 * * 1-5"  # 平日の9時
    actions:
      - type: message
        target: slack
        channel: "#general"
        template: "morning_briefing"

  - name: "クロスプラットフォームメッセージ要約"
    trigger:
      type: schedule
      cron: "0 18 * * *"  # 毎日18時
    actions:
      - type: summary
        sources: [slack, telegram]
        target: slack
        channel: "#daily-summary"
```

## ステップ7：一般的な問題のトラブルシューティング

### 問題1：Ollamaモデルのダウンロードに失敗する

**症状**: `ollama pull`実行時にエラーが発生

**解決策**:
```bash
# ミラーを使用
export OLLAMA_MIRROR=https://ollama.registry.example.com
ollama pull llama3:8b
```

### 問題2：Slack Botが応答しない

**チェックリスト**:
1. Bot Tokenが正しく設定されている
2. Socket Modeが有効になっている
3. 必要なスコープが追加されている
4. ログを確認：`docker-compose logs openclaw | grep slack`

### 問題3：メモリ不足

**症状**: システムが遅くなる、コンテナが終了する

**解決策**:
1. より小さいモデルを使用：`llama3:8b` → `mistral:7b` → `gemma:2b`
2. Dockerのメモリ使用を制限：
```yaml
# docker-compose.ymlで
services:
  openclaw:
    deploy:
      resources:
        limits:
          memory: 8G
```

### 問題4：ベクトルデータベースのクエリが遅い

**解決策**:
```bash
# Qdrantを再起動して最適化
docker-compose restart qdrant

# より小さい埋め込みモデルの使用を検討
# config.yamlを編集
embeddings:
  model: "nomic-embed-text"  # より小さく高速な埋め込みモデル
```

## ステップ8：パフォーマンス最適化のヒント

### 8.1 GPUアクセラレーション（NVIDIA GPUがある場合）

```bash
# NVIDIA Container Toolkitをインストール
sudo apt-get install -y nvidia-container-toolkit

# DockerがNVIDIAランタイムを使用するように設定
sudo nvidia-ctk runtime configure --runtime=docker

# Dockerを再起動
sudo systemctl restart docker

# docker-compose.ymlを変更
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

### 8.2 モデルパラメータの調整

`config/config.yaml`で：
```yaml
llm:
  max_tokens: 1024        # 最大生成長を減らす（高速だが切り捨てられる可能性）
  temperature: 0.5        # 温度を下げる（より決定論的な出力）
  context_window: 4096    # 必要に応じてコンテキストウィンドウを調整
```

### 8.3 キャッシュの有効化

```yaml
# config.yamlで
cache:
  enabled: true
  provider: redis         # Redisをキャッシュとして使用
  ttl: 3600              # 1時間キャッシュ
```

## 応用：マルチモデル展開

十分なハードウェアリソースがある場合、異なるシナリオで複数のモデルを同時に実行できます：

```yaml
# config.yaml
llm:
  models:
    default: llama3:8b
    fast: mistral:7b           # 高速応答用
    creative: llama3:70b       # 複雑なタスク用
    code: :33b   # コード生成用

  routing_rules:
    - if: context.includes("code")
      use: code
    - if: context.length > 1000
      use: creative
    - else: fast
```

## セキュリティ推奨事項

1. **ネットワーク分離**: 可能であれば、OpenClawを分離されたネットワークに展開
2. **定期的な更新**: 定期的に最新のイメージとコードをプル
```bash
git pull
docker-compose pull
docker-compose up -d --build
```
3. **設定のバックアップ**: 定期的に`config/`と`data/`ディレクトリをバックアップ
4. **ログの監視**: ログ監視を設定し、異常を早期に検出

## まとめ

以上のステップで、独自のOpenClawローカルAIアシスタントの導入に成功しました。これで以下のことができます：

- ✅ Slack/TelegramでAIと対話
- ✅ パーソナルナレッジベースの構築と検索
- ✅ ローカル自動化タスクの実行
- ✅ カスタムアクションの作成
- ✅ 自動化ワークフローの設定

OpenClawの強みはその拡張性にあります。ニーズの成長に伴い、新しい統合を追加し、より複雑なアクションを作成し、モデル設定を最適化し続けることができます。

**次のステップ**:
- 他のコミュニケーションプラットフォーム（Discord、WhatsApp）との統合を試す
- [OpenClawコミュニティ](https://github.com/openclaw/openclaw)のその他のプラグインを探索
- カスタムアクションをコミュニティと共有

導入中に問題が発生した場合は、GitHub Issuesで質問するか、[完全なドキュメント](https://docs.openclaw.dev)を参照してください。

Happy Hacking! 🚀
