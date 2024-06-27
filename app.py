import streamlit as st
from st_pages import Page, Section, show_pages, add_indentation
st.set_page_config(page_title="AIアシスタントさん", page_icon=":robot_face:", layout="wide")

# st.title("AIアシスタントさん")
# st.write("左側のサイドバーから各機能を選択してください。")

show_pages(
    [
        Page("app.py", "トップ", icon=":house:"),
        Section("AIチャットさん", icon=":bulb:"),
        Page("genai-firststep/usage.py", "- 使い方"),
        Page("genai-firststep/app.py", "- プレイグラウンド"),
        Section("口コミゲットさん", icon=":writing_hand:"),
        Page("scraping-tabelog/usage.py", "- 使い方"),
        Page("scraping-tabelog/app.py", "- プレイグラウンド"),
        Section("データ分析官さん", icon=":bar_chart:"),
        Page("data-analyzer/usage.py", "- 使い方"),
        Page("data-analyzer/app.py", "- プレイグラウンド"),
        Section("物知り手助けさん", icon=":mag:"),
        Page("langchain-rag/usage.py", "- 使い方"),
        Page("langchain-rag/app.py", "- プレイグラウンド"),
    ]
)

add_indentation()

# ここにトップページの内容を追加
st.markdown("""
## 生成AIとの上手な付き合い方を学ぼう！！

このアプリケーションは、飲食業界向けに作成した生成AI技術を体験できる学習ツールです。4つの異なる機能を通じて、AIとの対話、データ収集、分析、そして高度な質問応答システムを体験できます。

### アプリケーションの内容

1. **AIチャットさん** : Amazon Bedrock を利用した対話型AIです。簡単な操作で高度な言語モデルと会話できます。

2. **口コミゲットさん** : 食べログから店舗の口コミを自動収集するツールです。インターネットに存在するデータを簡単に取得できます。

3. **データ分析官さん** : AIを活用してCSVファイルのデータ分析を行います。損益計算書や口コミデータなど、様々なデータを分析できます。

4. **物知り手助けさん** : PDFファイルをソースとするRAGシステムです。アップロードしたPDFの内容に基づいて質問に答えます。

### アプリケーションで学べること

- 生成AIとの対話を通じて、AIの応答能力と限界を理解できます。
- ウェブスクレイピングを利用したビジネスデータの収集を体験できます。
- AIを活用したデータ分析の手法と、そこから得られるインサイトを体験できます。
- RAGシステムの仕組みと、独自のナレッジベースを活用したAIの可能性を探ることができます。

各機能を順に試していくことで、生成AI技術の多様な応用と可能性を体験的に学ぶことができます。さあ、AIとの新しい付き合い方を探索しましょう！
""")