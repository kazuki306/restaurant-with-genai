import os
import tempfile
# import shutil
# from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import streamlit as st
from langchain_aws import ChatBedrock
# import chromadb
# from chromadb.config import Settings

def make_chain(rag_model, rag_temperature, rag_max_tokens):
    chat = ChatBedrock(model_id=rag_model, model_kwargs={"max_tokens": rag_max_tokens, "temperature": rag_temperature})
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=st.session_state.retriever,
        memory=st.session_state.memory,
        )
    return chain

def create_vectordb(uploaded_file, select_chunk_size):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    loader = PyMuPDFLoader(file_path=tmp_file_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=select_chunk_size,
        chunk_overlap=100,
        length_function=len,
    )

    data = text_splitter.split_documents(documents)
    embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

    if "database" not in st.session_state:
        database = Chroma(
            collection_name="sample_collection",
            embedding_function=embeddings,
        )
    else:
        database = st.session_state.database

    database.add_documents(data)
    retriever = database.as_retriever()

    st.session_state.database = database
    st.session_state.retriever = retriever
    st.success("ベクトルDBが作成されました。")

def delete_vectordb():
    if st.session_state.get("database"):
        del st.session_state.database
    if st.session_state.get("retriever"):
        del st.session_state.retriever
    st.success("ベクトルDBが削除されました。")

st.title("物知り手助けさん")

with st.sidebar:
    st.title("設定")
    rag_model = st.selectbox("モデルを選択", ["anthropic.claude-3-sonnet-20240229-v1:0", "anthropic.claude-3-haiku-20240307-v1:0"])
    rag_temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    rag_max_tokens = st.slider("最大トークン数", 100, 4096, 1000)
    select_chunk_size = st.slider("Chunk", min_value=0.0, max_value=1000.0, value=300.0, step=10.0)
    if st.button("会話履歴のリセット"):
        st.session_state.rag_messages = []
        st.session_state.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

    uploaded_file = st.file_uploader("PDFをアップロード", type="pdf")

    if st.button("ベクトルDBを作成"):
        if uploaded_file:
            with st.spinner("ベクトルDBを作成中..."):
                create_vectordb(uploaded_file, select_chunk_size)
        else:
            st.error("PDFをアップロードしてください。")

    if st.button("ベクトルDBを削除"):
        if st.session_state.get("database"):
            with st.spinner("ベクトルDBを削除中..."):
                delete_vectordb()
        else:
            st.error("ベクトルDBが存在しません。")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

if "rag_messages" not in st.session_state:
    st.session_state["rag_messages"] = []

for message in st.session_state.rag_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# prompt = st.chat_input("PDFの内容について聞いてみましょう")

if rag_prompt := st.chat_input("アップロードしたPDFにまつわる質問をしてみましょう"):
    if uploaded_file is None:
        st.error("PDFをアップロードし、「ベクトルDBを作成」ボタンを押してベクトルDBを作成してください。")
    else:
        if not st.session_state.get("retriever"):
            st.error("PDFをアップロードし、「ベクトルDBを作成」ボタンを押してベクトルDBを作成してください。")
        else:
            chain = make_chain(rag_model, rag_temperature, rag_max_tokens)
            with st.chat_message("user"):
                st.markdown(rag_prompt)
            with st.chat_message("assistant"):
                with st.spinner("ドキュメントを取得し、回答を生成しています..."):
                    # chat = ChatBedrock(model_id=rag_model, model_kwargs={"max_tokens": rag_max_tokens, "temperature": rag_temperature})
                    # chain = ConversationalRetrievalChain.from_llm(
                    #     llm=chat,
                    #     retriever=st.session_state.retriever,
                    #     memory=st.session_state.memory,
                    # )
                    response = chain({"question": rag_prompt})
                    st.markdown(response["answer"])
                # response = st.write_stream(chain.astream({"question": rag_prompt}))
                

            st.session_state.rag_messages.append({"role": "user", "content": rag_prompt})
            # st.session_state.rag_messages.append({"role": "assistant", "content": response[0]["answer"]})
            st.session_state.rag_messages.append({"role": "assistant", "content": response["answer"]})

# print(st.session_state.memory)