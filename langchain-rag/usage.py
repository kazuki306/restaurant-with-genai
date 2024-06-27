import streamlit as st

st.title("物知り手助けさんの使い方 by Claude 3.5")

st.markdown("""
### アプリケーションの説明

物知り手助けさんは、PDFをデータソースとするRetrieval Augmented Generation (RAG)システムです。基盤モデルとして[Anthropic Claude](https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-claude.html)と[Amazon Titan Text Embeddings v2](https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/titan-embedding-models.html)を利用し、ベクトルDBに[Chroma DB](https://www.trychroma.com/)を使用しています。アップロードされたPDFの内容に基づいて質問に答えることができます。

### RAG の仕組みとユースケース

RAGは、大規模言語モデル（LLM）の知識を外部データで補強する技術です。従来のLLMは学習データの制限により最新の情報や特定のドメイン知識を持っていないことがありました。RAGはこの課題を解決するため、質問に関連する情報を外部データソースから取得し、LLMの回答生成に活用します。

RAGの主な仕組み : 
1. 外部データをベクトル化して保存
2. 質問をベクトル化し、関連する情報を検索
3. 検索結果とオリジナルの質問を組み合わせてLLMに入力
4. LLMが補強された情報を基に回答を生成

### アプリの使い方

1. モデルやシステムプロンプトなどを設定します。

2. RAGのデータソースに利用したいPDFをアップロードします。
   - 利用できそうなPDFがない場合は、[生成 AI 体験ワークショップ](https://catalog.workshops.aws/generative-ai-use-cases-jp/ja-JP)のRAGのユースケースで使用されている[勤怠管理システム入力方法マニュアル](https://ws-assets-prod-iad-r-nrt-2cb4b4649d0e0f94.s3.ap-northeast-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/rag-data/kintai.pdf)と[情報システム部門の Wiki](https://ws-assets-prod-iad-r-nrt-2cb4b4649d0e0f94.s3.ap-northeast-1.amazonaws.com/9748a536-3a71-4f0e-a6cd-ece16c0e3487/rag-data/information-system-dept.pdf)を利用できます。

3. 「ベクトルDBを作成」のボタンを押し、ベクトルDBが構築されるのを待ちます。

4. ベクトルDBが作成されたら、アップロードしたPDFにまつわる質問をします。

## サンプルドキュメントを利用した場合のプロンプト例

- 社内Wifiの使用方法を教えて
- USBメモリを使用するにはどうしたらいいですか？
- 勤怠システムのURLは？
""")