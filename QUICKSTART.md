# 🚀 クイックスタートガイド

## 1️⃣ Claude API キーを取得

1. https://console.anthropic.com/settings/keys にアクセス
2. 「Create Key」をクリック
3. APIキーをコピー

## 2️⃣ ローカルセットアップ（5分）

```bash
# 環境変数設定
cp .env.example .env

# .envファイルを編集
# ANTHROPIC_API_KEY=あなたのAPIキー に変更

# 依存関係インストール
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Playwrightブラウザインストール
playwright install chromium

# サーバー起動
uvicorn app.main:app --reload
```

## 3️⃣ テスト送信

ブラウザで http://localhost:8000/docs を開く

Swagger UIで以下をテスト:

```json
{
  "url": "https://example.com/contact",
  "message": "テストメッセージです。",
  "use_complex_model": false
}
```

## 4️⃣ Railway デプロイ（10分）

```bash
# Gitリポジトリ作成
git init
git add .
git commit -m "Initial commit"

# GitHubにプッシュ
git remote add origin https://github.com/YOUR_USERNAME/formAI.git
git push -u origin main
```

Railway で:
1. New Project → Deploy from GitHub repo
2. リポジトリを選択
3. Variables タブで `ANTHROPIC_API_KEY` を設定
4. デプロイ完了！

## 5️⃣ Google Spreadsheet セットアップ（5分）

1. 新規スプレッドシート作成
2. 拡張機能 > Apps Script
3. `gas/Code.gs` の内容をコピー＆ペースト
4. `API_ENDPOINT` を Railway URL に変更
5. `setupSheet()` を実行
6. メニューから「Form AI」で送信！

---

## 💡 使い方

| 列 | 内容 |
|---|------|
| A | フォームのURL |
| B | 送信するメッセージ |
| C | ステータス（自動更新） |
| D | 詳細（自動更新） |
| E | コスト（自動更新） |

データを入力して、メニューから「Form AI > 選択行を送信」をクリック！

## 💰 コスト目安

- 1件送信: 約 $0.0001〜$0.0005（0.01円〜0.05円）
- 1,000件送信: 約 $0.10〜$0.50（10円〜50円）

Claude Haikuは高速かつ低コスト！

## 🆘 トラブルシューティング

### APIエラーが出る
- Claude API キーが正しいか確認
- https://console.anthropic.com/settings/keys で有効か確認

### ブラウザが起動しない
```bash
playwright install chromium
playwright install-deps chromium
```

### Railway でタイムアウト
- 初回リクエストは起動に時間がかかります（1〜2分）
- 2回目以降は高速です

---

詳細は [README.md](README.md) を参照
