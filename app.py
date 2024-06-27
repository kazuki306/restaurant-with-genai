# import streamlit as st
# from st_pages import Page, Section, show_pages

# st.set_page_config(page_title="AIアシスタントアプリ", page_icon=":robot_face:", layout="wide")

# show_pages(
#     [
#         Page("app.py", "トップ", icon=":house:"),
#         Page("genai-firststep/app.py", "AIチャットさん", icon=":bulb:"),
#         Page("scraping-tabelog/app.py", "口コミゲットさん", icon=":writing_hand:"),
#         Page("data-analyzer/app.py", "データ分析官さん", icon=":bar_chart:"),
#         Page("langchain-rag/app.py", "物知り手助けさん", icon=":mag:"),
#     ]
# )

# st.title("AIアシスタントアプリ")
# st.write("左側のサイドバーから各機能を選択してください。")

# # ここにトップページの内容を追加

import streamlit as st
from st_pages import Page, Section, show_pages, add_indentation
st.set_page_config(page_title="AIアシスタントアプリ", page_icon=":robot_face:", layout="wide")

st.title("AIアシスタントアプリ")
st.write("左側のサイドバーから各機能を選択してください。")

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