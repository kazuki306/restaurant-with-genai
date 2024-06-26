from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_core.messages import HumanMessage
import streamlit as st

# chainの定義
def make_chain(model, system_prompt, temperature, max_tokens):
    prompt = ChatPromptTemplate.from_messages([
            ("system",system_prompt),
            # SystemMessagePromptTemplate.from_template(system_prompt),
            # SystemMessagePromptTemplate.from_template("{system_message}"),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="human_message")])
    LLM = ChatBedrock(model_id=model, model_kwargs={"max_tokens": max_tokens, "temperature": temperature})
    # print(prompt)
    chain = prompt | LLM
    return chain

st.title("AIチャットさん")

# サイドバーの設定
with st.sidebar:
    st.title("設定")
    model = st.selectbox("モデルを選択", ["anthropic.claude-3-sonnet-20240229-v1:0", "anthropic.claude-3-haiku-20240307-v1:0"])
    system_prompt = st.text_area("システムプロンプト", placeholder="あなたは親切なチャットボットです")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("最大トークン数", 100, 4096, 1000)
    if st.button("会話履歴のリセット"):
        st.session_state.messages = []


# 初回はsession領域を作成
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 2回目以降はsessionを元に全量再描画を行う        
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 入力された場合
if user_prompt := st.chat_input("何か話しかけてみましょう"):
    # 入力内容の描画
    with st.chat_message("user"):
        st.write(user_prompt)
    # chainをstreamで実行し生成内容をstreamで出力
    with st.chat_message("assistant"):
        # chain = make_chain(st.session_state.model, st.session_state.system_prompt,st.session_state.temperature,st.session_state.max_tokens)
        chain = make_chain(model, system_prompt,temperature,max_tokens)
        # chain = make_chain(st.session_state.system_prompt, st.session_state.temperature, st.session_state.max_tokens)
        # response = st.write_stream(chain.stream({"system_message": st.session_state.system_prompt,"messages": st.session_state.messages, "human_message": [HumanMessage(content=user_prompt)]}))
        response = st.write_stream(chain.stream({"system_message": system_prompt,"messages": st.session_state.messages, "human_message": [HumanMessage(content=user_prompt)]}))

    # 入力内容と生成内容をsession領域に格納
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
