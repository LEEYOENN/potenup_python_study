# uv add openai python-dotenv streamlit
# .env 파일 만들어서 OPENAI_API_KEY 추가해두기
# 서버 실행: streamlit run main.py
import streamlit as st 

pages = [
    st.Page(
        page="pages/components.py",
        title="Basic",
        icon="😊",
        default=True
    ),
    st.Page(
        page="pages/chatbot.py",
        title="Chatbot",
        icon="💬"
    )
]

nav = st.navigation(pages)
nav.run()
