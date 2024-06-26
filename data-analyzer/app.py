from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
import streamlit as st
import pandas as pd
import io

# chainの定義
def make_chain(analyze_model, analyze_system_prompt, analyze_temperature, analyze_max_tokens):
    prompt = ChatPromptTemplate.from_messages([
            ("system",analyze_system_prompt),
            MessagesPlaceholder(variable_name="analyze_messages"),
            MessagesPlaceholder(variable_name="human_message")])
    LLM = ChatBedrock(model_id=analyze_model, model_kwargs={"max_tokens": analyze_max_tokens, "temperature": analyze_temperature})
    chain = prompt | LLM
    return chain

st.title("データ分析官さん")

# CSVファイルの読み込み
profit_loss_df = None
review_df = None

# サイドバーの設定
with st.sidebar:
    st.title("設定")
    analyze_model = st.selectbox("モデルを選択", ["anthropic.claude-3-sonnet-20240229-v1:0", "anthropic.claude-3-haiku-20240307-v1:0"])
    analyze_system_prompt = st.text_area("システムプロンプト", placeholder="あなたは優秀なデータ分析官です")
    analyze_temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    analyze_max_tokens = st.slider("最大トークン数", 100, 4096, 1000)
    if st.button("会話履歴のリセット"):
        st.session_state.analyze_messages = []

    # CSVファイルのアップロード
    st.title("CSVファイルのアップロード")
    profit_loss_csv = st.file_uploader("損益計算書CSV", type="csv")
    review_csv = st.file_uploader("口コミCSV", type="csv")

    if profit_loss_csv is not None:
        profit_loss_df = pd.read_csv(profit_loss_csv)
        st.write("損益計算書CSVが読み込まれました !!")

    if review_csv is not None:
        review_df = pd.read_csv(review_csv)
        st.write("口コミCSVが読み込まれました !!")

# 初回はsession領域を作成
if "analyze_messages" not in st.session_state:
    st.session_state["analyze_messages"] = []

# 2回目以降はsessionを元に全量再描画を行う        
for message in st.session_state.analyze_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 入力された場合
if user_prompt := st.chat_input("損益計算書や口コミを基に生成AIに分析をお願いしてみましょう"):
    if profit_loss_df is None and review_df is None:
        st.error("分析するためのCSVを入力してください")
    else:
        chain = make_chain(analyze_model, analyze_system_prompt, analyze_temperature, analyze_max_tokens)
        # 入力内容の描画
        with st.chat_message("user"):
            st.write(user_prompt)
        # chainをstreamで実行し生成内容をstreamで出力
        with st.chat_message("assistant"):
            # CSVデータをプロンプトに追加
            csv_data = ""
            if profit_loss_df is not None:
                csv_data += "損益計算書データ:\n" + profit_loss_df.to_string() + "\n\n"
            if review_df is not None:
                csv_data += "口コミデータ:\n" + review_df.to_string() + "\n\n"
            
            full_prompt = user_prompt + csv_data
            response = st.write_stream(chain.stream({"analyze_messages": st.session_state.analyze_messages, "human_message": [HumanMessage(content=full_prompt)]}))

        # 入力内容と生成内容をsession領域に格納
        st.session_state.analyze_messages.append({"role": "user", "content": user_prompt})
        st.session_state.analyze_messages.append({"role": "assistant", "content": response})