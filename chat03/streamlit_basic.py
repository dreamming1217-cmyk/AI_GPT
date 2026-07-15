import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# 상단의 메뉴 없애기
# streamlit_basic.py
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Streamlit 페이지 설정: 반드시 가장 위쪽 Streamlit 명령이어야 함
st.set_page_config(
    page_title="Chatbot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Streamlit 상단 메뉴/툴바/사이드바/푸터 숨기기
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

[data-testid="stToolbar"] {display: none;}
[data-testid="stDecoration"] {display: none;}
[data-testid="stStatusWidget"] {display: none;}
[data-testid="collapsedControl"] {display: none;}

section[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebarCollapsedControl"] {display: none !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

load_dotenv()

load_dotenv()

# (0) 사이드바에서 api_key 입력하는 부분 
with st.sidebar:
    openai_api_key = os.getenv('OPENAI_API_KEY') 
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
st.title("💬 Chatbot")

# (1) st.session_state에 "messages"가 없으면 초기값을 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "뭐가 문제야"}]

# (2) 대화 기록을 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# (3) 사용자 입력을 받아 대화 기록에 추가하고 AI 응답을 생성
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt}) 
    st.chat_message("user").write(prompt) 
    response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages) 
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg}) 
    st.chat_message("assistant").write(msg)