# 飲食店向けAI分析アプリケーション

## 概要

このプロジェクトは、Amazon Bedrockを利用したStreamlitベースの飲食向けWebアプリケーションです。Dockerコンテナを使用して簡単に起動できます。

## 主な機能

1. シンプルな生成AIチャット
2. 食べログの口コミスクレイピング
3. 損益計算書と口コミに基づく店舗状況のAI分析
4. PDFを利用したRAGアプリケーション

## インストールと起動方法

1. リポジトリをクローンします:

```
git clone https://github.com/kazuki306/restaurant-with-genai.git
```

2. クローンしたリポジトリに移動します:

```
cd restaurant-with-genai 
```

3. Dockerイメージをビルドします:

```
docker build -t streamlit-genai-app .
```

4. コンテナを起動します:

```
docker run -p 8080:8501 streamlit-genai-app
```

5. ブラウザで `http://localhost:8080` にアクセスしてアプリケーションを利用できます。

## 注意事項

- Amazon Bedrockの認証情報が必要です。
- 詳細な設定や使用方法については、プロジェクト内のドキュメントを参照してください。
