#!/bin/bash

# Form AI 本番環境セットアップスクリプト

set -e

echo "🚀 Form AI 本番環境セットアップを開始します..."
echo ""

# Step 1: Homebrewの確認
echo "📦 Step 1: Homebrewの確認..."
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrewが見つかりません"
    echo ""
    echo "以下のコマンドを実行してHomebrewをインストールしてください："
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    echo ""
    echo "インストール完了後、画面の指示に従ってPATHを設定してから、このスクリプトを再実行してください。"
    exit 1
fi
echo "✅ Homebrew がインストールされています"
echo ""

# Step 2: Python 3.11のインストール
echo "🐍 Step 2: Python 3.11をインストール中..."
if ! command -v python3.11 &> /dev/null; then
    echo "Python 3.11をインストール中..."
    brew install python@3.11
    echo "✅ Python 3.11 のインストール完了"
else
    echo "✅ Python 3.11 は既にインストールされています"
fi
python3.11 --version
echo ""

# Step 3: 仮想環境の作成
echo "🔧 Step 3: 仮想環境を作成中..."
if [ -d "venv" ]; then
    echo "既存の仮想環境を削除中..."
    rm -rf venv
fi
python3.11 -m venv venv
echo "✅ 仮想環境の作成完了"
echo ""

# Step 4: 依存関係のインストール
echo "📚 Step 4: 依存関係をインストール中..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ 依存関係のインストール完了"
echo ""

# Step 5: Playwrightのインストール
echo "🌐 Step 5: Playwright ブラウザをインストール中..."
playwright install chromium
echo "✅ Playwright のインストール完了"
echo ""

# Step 6: 環境変数の確認
echo "⚙️  Step 6: 環境変数の確認..."
if [ -f ".env" ]; then
    if grep -q "ANTHROPIC_API_KEY=sk-ant" .env; then
        echo "✅ .env ファイルが存在します"
    else
        echo "⚠️  .env ファイルにANTHROPIC_API_KEYが設定されていません"
        echo "   .envファイルを編集して、ANTHROPIC_API_KEYを設定してください"
    fi
else
    echo "⚠️  .env ファイルが見つかりません"
    echo "   .env.example をコピーして .env を作成し、APIキーを設定してください"
fi
echo ""

# 完了メッセージ
echo "🎉 セットアップ完了！"
echo ""
echo "サーバーを起動するには："
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "ブラウザで以下にアクセス："
echo "  http://localhost:8000/docs"
echo ""
