# 🛠️ 完全セットアップガイド

## ⚠️ 重要: APIキーのセキュリティ

チャットでAPIキーを共有されました。このキーは公開される可能性があります。

**すぐに以下を実行してください:**

1. https://aistudio.google.com/app/apikey にアクセス
2. 既存のAPIキー `AIzaSyCBT0TvNvR5Y8mkrPGLn6KR5hvIjn-jGa8` を**削除**
3. 新しいAPIキーを**作成**
4. 新しいキーをメモ（後で使用）

---

## Step 1: Python 3.11 をインストール

### Option A: Homebrew経由（推奨）

```bash
# ターミナルで以下を実行

# 1. Homebrewをインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. インストール後、表示される指示に従って環境変数を設定
# (画面に表示されるコマンドを実行)

# 3. Python 3.11 をインストール
brew install python@3.11

# 4. バージョン確認
python3.11 --version
```

### Option B: 公式インストーラー（Homebrewを使いたくない場合）

1. https://www.python.org/downloads/ にアクセス
2. 「Download Python 3.11.x」をクリック
3. ダウンロードした `.pkg` ファイルを実行
4. インストーラーの指示に従う
5. ターミナルで確認:
   ```bash
   python3.11 --version
   ```

---

## Step 2: プロジェクトのセットアップ

```bash
# 1. formAIディレクトリに移動
cd /Users/user/claudetest/formAI

# 2. 古い仮想環境を削除（既にある場合）
rm -rf venv

# 3. Python 3.11で新しい仮想環境を作成
python3.11 -m venv venv

# 4. 仮想環境を有効化
source venv/bin/activate

# 5. pipをアップグレード
pip install --upgrade pip

# 6. 依存関係をインストール
pip install -r requirements.txt

# 7. Playwrightブラウザをインストール
playwright install chromium
```

---

## Step 3: 新しいAPIキーを設定

```bash
# .envファイルを編集
nano .env

# または
open -e .env
```

**新しいAPIキー**を入力:

```
GOOGLE_API_KEY=ここに新しいAPIキーを貼り付け
```

保存して閉じる（nanoの場合: Ctrl+X → Y → Enter）

---

## Step 4: サーバーを起動

```bash
# 仮想環境が有効化されていることを確認（プロンプトに (venv) が表示される）
source venv/bin/activate

# サーバー起動
uvicorn app.main:app --reload
```

成功すると以下のような表示が出ます:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Step 5: APIをテスト

ブラウザで開く:
```
http://localhost:8000/docs
```

Swagger UIが表示されます。

### テスト送信:

1. `/api/submit` のセクションを開く
2. 「Try it out」をクリック
3. 以下のJSONを入力:

```json
{
  "url": "https://example.com/contact",
  "message": "これはテストメッセージです。",
  "use_complex_model": false
}
```

4. 「Execute」をクリック
5. 結果を確認

---

## 📊 Google Spreadsheet セットアップ

### 1. スプレッドシート作成

1. Google Spreadsheetを新規作成
2. 以下の見出しを設定:

| A列 | B列 | C列 | D列 | E列 |
|-----|-----|-----|-----|-----|
| URL | メッセージ | ステータス | 詳細 | コスト |

### 2. Apps Script設定

1. スプレッドシートで: **拡張機能 > Apps Script**
2. `formAI/gas/Code.gs` の内容を全てコピー
3. Apps Scriptエディタに貼り付け
4. **重要**: 以下の行を編集:

```javascript
const API_ENDPOINT = 'http://localhost:8000/api/submit';
// ローカルテスト用
// Railwayデプロイ後は Railway の URL に変更
```

5. 保存（💾アイコンをクリック）

### 3. 初期設定実行

1. Apps Scriptエディタで関数一覧から `setupSheet` を選択
2. 実行ボタン（▶️）をクリック
3. 権限を求められたら:
   - 「権限を確認」をクリック
   - Googleアカウントを選択
   - 「詳細」→「（プロジェクト名）に移動」
   - 「許可」をクリック

### 4. 使用方法

スプレッドシートに戻ると:
- メニューに「📧 Form AI」が追加されます
- A列にURL、B列にメッセージを入力
- メニューから「Form AI > 選択行を送信」

---

## ☁️ Railway デプロイ（本番環境）

### 1. Gitリポジトリ作成

```bash
cd /Users/user/claudetest/formAI

# Git初期化
git init

# .gitignoreを確認（.envが除外されているか）
cat .gitignore

# コミット
git add .
git commit -m "Initial commit: Form AI with Gemini"
```

### 2. GitHubにプッシュ

1. https://github.com にアクセス
2. 「New repository」をクリック
3. リポジトリ名: `formAI`
4. Privateを選択（推奨）
5. 「Create repository」

ターミナルで:
```bash
git remote add origin https://github.com/YOUR_USERNAME/formAI.git
git branch -M main
git push -u origin main
```

### 3. Railwayでデプロイ

1. https://railway.app にアクセス
2. GitHubアカウントでサインイン
3. 「New Project」をクリック
4. 「Deploy from GitHub repo」を選択
5. `formAI` リポジトリを選択
6. 自動的にデプロイが開始されます

### 4. 環境変数を設定

1. Railway ダッシュボードでプロジェクトを開く
2. 「Variables」タブをクリック
3. 以下を追加:

```
GOOGLE_API_KEY=新しく作成したAPIキー
DEFAULT_MODEL=gemini-1.5-flash
COMPANY_NAME=RECHANCE株式会社
CONTACT_PERSON=桑原麻由
EMAIL=info@rechance.jp
PHONE=090-1234-7891
```

4. 「Add」をクリック

### 5. デプロイURLを取得

1. 「Settings」タブ
2. 「Networking」セクション
3. 「Generate Domain」をクリック
4. URLをコピー（例: `https://formai-production-xxxx.up.railway.app`）

### 6. Google Apps ScriptのURL更新

1. Apps Scriptエディタに戻る
2. `API_ENDPOINT` を更新:

```javascript
const API_ENDPOINT = 'https://formai-production-xxxx.up.railway.app/api/submit';
```

3. 保存

---

## ✅ 完了！

これで以下が動作します:

- ✅ ローカルでAPI実行
- ✅ Railwayで本番環境
- ✅ スプレッドシートから自動送信

---

## 🆘 トラブルシューティング

### Python 3.11が見つからない

```bash
# インストール確認
which python3.11

# パスを確認
ls /usr/local/bin/python* /opt/homebrew/bin/python*

# 見つかったパスで仮想環境作成
/フルパス/python3.11 -m venv venv
```

### playwright installでエラー

```bash
# 依存関係をインストール
playwright install-deps chromium
playwright install chromium
```

### uvicornが見つからない

```bash
# 仮想環境が有効化されているか確認
which python
# /Users/user/claudetest/formAI/venv/bin/python と表示されるはず

# 有効化されていない場合
source venv/bin/activate
```

### Railwayでタイムアウト

- 無料プランは一定時間でスリープします
- 初回アクセスは1〜2分かかる場合があります
- 2回目以降は高速です

---

## 📞 サポート

問題が発生した場合は、エラーメッセージを共有してください。
