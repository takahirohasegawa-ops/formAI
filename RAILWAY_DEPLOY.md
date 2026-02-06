# 🚀 Railway デプロイ完全ガイド

## ✅ Step 1: Git準備完了

```
✅ Gitリポジトリ初期化完了
✅ 不要なファイル削除完了
✅ コミット完了
```

---

## 📝 Step 2: GitHubリポジトリ作成

### 2-1. GitHubにアクセス

1. https://github.com にアクセス
2. ログイン（アカウントがない場合は作成）

### 2-2. 新しいリポジトリを作成

1. 右上の「+」→「New repository」をクリック
2. 以下を入力：
   - **Repository name**: `formAI`
   - **Description**: `Automated form submission with Gemini AI`
   - **Visibility**: **Private** を選択（推奨）
   - ❌ **Initialize this repository** はチェックしない
3. 「Create repository」をクリック

### 2-3. ローカルからプッシュ

GitHubに表示される指示のうち、**「push an existing repository」**の部分を使用：

```bash
cd /Users/user/claudetest/formAI

# GitHubリポジトリをリモートに追加
git remote add origin https://github.com/YOUR_USERNAME/formAI.git

# ブランチ名をmainに変更（必要な場合）
git branch -M main

# プッシュ
git push -u origin main
```

**YOUR_USERNAME** を自分のGitHubユーザー名に置き換えてください。

### トラブルシューティング

**認証エラーが出る場合:**

1. Personal Access Token (PAT) を作成：
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 「Generate new token (classic)」をクリック
   - Note: `formAI deploy`
   - Expiration: 90 days
   - Scopes: **repo** にチェック
   - 「Generate token」をクリック
   - **トークンをコピー**（このページを離れると二度と表示されません！）

2. プッシュ時、パスワードの代わりにトークンを使用：
```bash
git push -u origin main
# Username: YOUR_USERNAME
# Password: (トークンを貼り付け)
```

---

## 🚂 Step 3: Railwayでデプロイ

### 3-1. Railwayアカウント作成

1. https://railway.app にアクセス
2. 「Start a New Project」をクリック
3. **GitHub** でサインイン

### 3-2. プロジェクト作成

1. 「New Project」をクリック
2. 「Deploy from GitHub repo」を選択
3. **Configure GitHub App** をクリック
4. リポジトリへのアクセスを許可:
   - 「Only select repositories」を選択
   - `formAI` を選択
   - 「Save」をクリック
5. 戻って `formAI` リポジトリを選択
6. 「Deploy Now」をクリック

### 3-3. 自動デプロイ開始

Railwayが自動的に以下を実行します：
- Dockerfileを検出
- イメージをビルド
- デプロイ

**待機時間:** 5〜10分

---

## ⚙️ Step 4: 環境変数を設定

デプロイ中に設定できます：

### 4-1. Variablesタブを開く

1. Railwayダッシュボードで `formAI` プロジェクトをクリック
2. 「Variables」タブをクリック

### 4-2. 環境変数を追加

以下を1つずつ追加：

```bash
GOOGLE_API_KEY=YOUR_API_KEY_HERE
DEFAULT_MODEL=gemini-1.5-flash
COMPANY_NAME=RECHANCE株式会社
CONTACT_PERSON=桑原麻由
EMAIL=info@rechance.jp
PHONE=090-1234-7891
```

**重要:**
- 各変数を「Add Variable」で1つずつ追加
- すべて追加したら自動的に再デプロイされます

---

## 🌐 Step 5: URLを取得

### 5-1. ドメイン生成

1. 「Settings」タブをクリック
2. 「Networking」セクションを見つける
3. 「Generate Domain」をクリック

Railway が自動的にドメインを生成します：
```
https://formai-production-xxxx.up.railway.app
```

### 5-2. URLをコピー

このURLが本番環境のAPIエンドポイントになります！

---

## ✅ Step 6: デプロイ確認

### 6-1. ヘルスチェック

ブラウザで以下にアクセス：
```
https://formai-production-xxxx.up.railway.app/
```

期待される応答：
```json
{
  "service": "Form AI",
  "version": "0.1.0",
  "status": "running",
  "docs": "/docs"
}
```

### 6-2. Swagger UIを確認

```
https://formai-production-xxxx.up.railway.app/docs
```

Swagger UIが表示されればOK！

### 6-3. ログを確認

Railway ダッシュボード → 「Deployments」タブ → ログを確認

エラーがなければ成功です！

---

## 📊 Step 7: Google Spreadsheetと連携

### 7-1. GASのURL更新

1. Googleスプレッドシートを開く
2. 拡張機能 → Apps Script
3. `Code.gs` の以下の行を編集：

```javascript
const API_ENDPOINT = 'https://formai-production-xxxx.up.railway.app/api/submit';
```

**xxxx** を実際のRailway URLに置き換え

4. 保存（💾アイコン）

### 7-2. テスト送信

1. スプレッドシートに戻る
2. A列にURL、B列にメッセージを入力
3. メニューから「Form AI > 選択行を送信」
4. 結果を確認！

---

## 🎉 完了！

**デプロイされたURL:**
```
https://formai-production-xxxx.up.railway.app
```

**Swagger UI:**
```
https://formai-production-xxxx.up.railway.app/docs
```

---

## 💡 次のステップ

### コスト管理

Railway 無料プラン：
- 月 $5 分の無料クレジット
- 超過分は従量課金

**節約のコツ:**
- 使わないときはプロジェクトを停止
- Gemini Flash モデルを使用（超低コスト）

### カスタマイズ

- `app/config.py` で設定変更
- 送信者情報のカスタマイズ
- モデルの切り替え

### 更新方法

コードを更新したら：
```bash
git add .
git commit -m "Update: description"
git push
```

Railwayが自動的に再デプロイします！

---

## 🆘 トラブルシューティング

### デプロイが失敗する

1. Railway ログを確認
2. 環境変数が正しく設定されているか確認
3. Dockerfile の記述を確認

### APIが動かない

1. `GOOGLE_API_KEY` が正しいか確認
2. Railway のログでエラーを確認
3. https://aistudio.google.com/app/apikey でAPIキーを再生成

### スプレッドシートから送信できない

1. GAS の `API_ENDPOINT` が正しいか確認
2. Railway の URL にアクセスできるか確認
3. Railway のログを確認

---

**お疲れ様でした！🎉**
