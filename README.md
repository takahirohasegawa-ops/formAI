# 📧 Form AI - フォーム自動送信システム

スプレッドシートからURLと本文を読み込み、お問い合わせフォームに自動送信するシステム

## 🎯 概要

- **Python + Browser Use + Gemini API** でフォーム送信を自動化
- **FastAPI** でAPI化
- **Railway** にデプロイ
- **Google Apps Script** からスプレッドシート操作

## 🏗️ システム構成

```
formAI/
├── app/
│   ├── main.py          # FastAPI アプリケーション
│   ├── form_agent.py    # フォーム送信エンジン (Browser Use)
│   ├── config.py        # 設定管理
│   └── models.py        # データモデル
├── gas/
│   └── Code.gs          # Google Apps Script
├── requirements.txt     # Python依存関係
├── Dockerfile          # Dockerイメージ定義
├── railway.json        # Railway設定
└── .env.example        # 環境変数テンプレート
```

## 🚀 セットアップ

### 1. ローカル開発環境

```bash
# リポジトリをクローン
cd formAI

# 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# Playwrightブラウザをインストール
playwright install chromium

# 環境変数を設定
cp .env.example .env
# .envファイルを編集してANTHROPIC_API_KEYを設定
```

### 2. 環境変数設定

`.env` ファイルに以下を設定：

```bash
# Google Gemini API Key (必須)
# https://aistudio.google.com/app/apikey で取得
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXX

# モデル設定
DEFAULT_MODEL=gemini-2.5-flash-latest    # コスト重視（高速・安価）
# DEFAULT_MODEL=gemini-2.5-flash-latest    # 精度重視（高精度）

# 送信者情報
COMPANY_NAME=RECHANCE株式会社
CONTACT_PERSON=桑原麻由
EMAIL=info@rechance.jp
PHONE=050-1783-6959
```

### 3. ローカルでテスト実行

```bash
# APIサーバーを起動
uvicorn app.main:app --reload

# ブラウザで http://localhost:8000/docs を開く
# Swagger UIでAPIをテスト
```

### 4. APIテスト（cURLで送信テスト）

```bash
curl -X POST "http://localhost:8000/api/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/contact",
    "message": "お問い合わせテストです。",
    "use_complex_model": false
  }'
```

## ☁️ Railwayへのデプロイ

### 1. Railwayアカウント作成

1. [Railway](https://railway.app/) にアクセス
2. GitHubアカウントでサインアップ

### 2. プロジェクトをデプロイ

```bash
# Gitリポジトリを初期化（まだの場合）
git init
git add .
git commit -m "Initial commit"

# GitHubにプッシュ
git remote add origin https://github.com/YOUR_USERNAME/formAI.git
git push -u origin main
```

### 3. RailwayでGitHubリポジトリを接続

1. Railway ダッシュボードで **New Project** をクリック
2. **Deploy from GitHub repo** を選択
3. リポジトリを選択
4. 自動的にデプロイが開始されます

### 4. 環境変数を設定

Railway プロジェクトの **Variables** タブで以下を設定：

```
GOOGLE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXX
DEFAULT_MODEL=gemini-1.5-flash
COMPANY_NAME=RECHANCE株式会社
CONTACT_PERSON=桑原麻由
EMAIL=info@rechance.jp
PHONE=090-1234-7891
```

### 5. デプロイURLを確認

- Railway が自動的に URL を発行します
- 例: `https://formAI-production-xxxx.up.railway.app`

## 📊 Google Spreadsheetのセットアップ

### 1. スプレッドシート作成

1. 新しいGoogleスプレッドシートを作成
2. 以下の列を作成：

| A列 (URL) | B列 (メッセージ) | C列 (ステータス) | D列 (詳細) | E列 (コスト) |
|-----------|-----------------|----------------|-----------|------------|

### 2. Apps Scriptを追加

1. スプレッドシートで **拡張機能 > Apps Script** を開く
2. `gas/Code.gs` の内容をコピー＆ペースト
3. **API_ENDPOINT** を Railway の URL に変更：

```javascript
const API_ENDPOINT = 'https://your-app.railway.app/api/submit';
```

4. 保存して、スプレッドシートに戻る

### 3. 初期設定を実行

1. Apps Script エディタで **setupSheet** 関数を実行
2. 権限を許可
3. スプレッドシートが自動設定されます

### 4. メニューから送信

スプレッドシートのメニューに **📧 Form AI** が追加されます：

- **🚀 選択行を送信**: 選択した行のフォームを送信
- **📊 全件送信**: ステータスが空白の全行を送信
- **🔄 ステータスクリア**: ステータスをクリア
- **⚙️ 設定**: 現在の設定を表示

## 💰 コスト最適化

### モデル選択

- **Gemini 1.5 Flash** (デフォルト): 超低コスト、高速、シンプルなフォーム向け
  - 入力: $0.075 / 1M tokens
  - 出力: $0.30 / 1M tokens
  - **Claude Haikuの約1/3のコスト！**

- **Gemini 1.5 Pro**: 高精度、複雑なフォーム向け
  - 入力: $1.25 / 1M tokens
  - 出力: $5.00 / 1M tokens

### CAPTCHA自動検知

CAPTCHAを検知すると早期終了し、無駄なトークン消費を防ぎます。

### コストメリット

- Gemini Flashは Claude Haikuの **約1/3のコスト**
- 1,000件送信で約 **$0.30〜$1.00** の節約

## 📝 使用例

### スプレッドシート入力例

| URL | メッセージ | ステータス | 詳細 | コスト |
|-----|-----------|-----------|------|--------|
| https://example.com/contact | 貴社のサービスに興味があります。 | ✅ 成功 | フォーム送信が完了しました | $0.001234 |
| https://example2.com/inquiry | お問い合わせです。 | 🔒 CAPTCHA | CAPTCHAが検出されました | - |

### API直接呼び出し

```python
import requests

response = requests.post(
    "https://your-app.railway.app/api/submit",
    json={
        "url": "https://example.com/contact",
        "message": "お問い合わせ内容",
        "use_complex_model": False
    }
)

print(response.json())
```

## 🔧 トラブルシューティング

### Playwrightが起動しない

```bash
# ブラウザを再インストール
playwright install chromium
playwright install-deps chromium
```

### Railway でタイムアウトする

- Railway の無料プランは一定時間でスリープします
- 初回リクエストは起動に時間がかかる場合があります

### GASでAPIエラーが出る

1. Railway の URL が正しいか確認
2. Railway の環境変数が設定されているか確認
3. Railway のログを確認: `railway logs`

## 📚 API ドキュメント

デプロイ後、以下のURLでSwagger UIにアクセス：

```
https://your-app.railway.app/docs
```

### エンドポイント

- `GET /` - ヘルスチェック
- `GET /health` - ヘルスチェック
- `POST /api/submit` - フォーム送信（単体）
- `POST /api/batch-submit` - フォーム送信（バッチ）
- `GET /api/config` - 現在の設定を取得

## 🛡️ セキュリティ

- API キーは環境変数で管理
- `.env` ファイルは `.gitignore` に含める
- Railway の環境変数は暗号化されて保存されます

## 📄 ライセンス

MIT License

## 🤝 サポート

問題が発生した場合は、GitHubのIssuesで報告してください。

---

**開発:** RECHANCE株式会社
**お問い合わせ:** info@rechance.jp
# Railway deployment 2026年 2月 7日 土曜日 23時45分53秒 JST
