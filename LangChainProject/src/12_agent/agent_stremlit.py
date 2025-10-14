from typing import List, Union
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_experimental.tools import PythonAstREPLTool
from langchain_openai import ChatOpenAI
from langchain_teddynote.messages import AgentStreamParser, AgentCallbacks
from langchain_teddynote import logging
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# API 키 가져오기
load_dotenv()
logging.langsmith("RAG 챗봇 💬")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 상수 정의
class MessageRole:
    """
    메시지 역할을 정의하는 클래스 입니다.
    """
    USER = "user"
    ASSISTANT = "assistant"

class MessageType:
    """
    메시지 유형을 정의하는 클래스 입니다.
    """

    TEXT = "text"
    FIGURE = "figure" # 이미지
    CODE = "code"
    DATAFRAME = "dataframe"


# 메시지 관련 함수
def print_messages():
    """
    저장된 메시지를 메시지 타입에 맞게 화면에 출력하는 함수입니다.
    """
    for role, content_list in st.session_state["messages"]:
        with st.chat_message(role): # streamlit의 기능 메시지 스타일의 ui 컨테이너를 생성
            for content in content_list:
                if isinstance(content, list):
                    message_type, message_content = content

                    if message_type == MessageType.TEXT:
                        st.markdown(message_content) # 텍스트 메시지 출력
                    elif message_type == MessageType.FIGURE:
                        st.pyplot(message_content) # 그림 메시지 출력
                    elif message_type == MessageType.CODE:
                        with st.status("코드 출력", expanded=True): # 블록 내의 코드가 실행되는 동안 진행중을 나타냄 상태상자 내용 보이기
                            st.code(
                                message_content,language="python"
                                ) # 코드 메시지 출력
                    elif message_type == MessageType.DATAFRAME:
                        st.dataframe(message_content) # 데이터프레임 메시지 출력
                
                else:
                    raise ValueError(f"알 수 없는 콘텐츠 유형입니다. {content}")
                

def add_message(role: MessageRole, content: List[Union[MessageType, str]]): # 메시지 내용하나하나가 둘중에 한 타입이어야함을 의미
    """
    새로운 메시지를 저장하는 함수입니다.

    Args:
        role (MessageRole): 메시지 역할 (USER, ASSISTANT)
        content (List[Union[MessageType, str]]): 메시지 내용
    """

    messages = st.session_state["messages"]
    if messages and messages[-1][0] == role:
        messages[-1][1].extend([content]) # 같은 역할의 연속된 메시지는 하나로 합칩니다.
    else:
        messages.append([role, [content]]) # 새로운 역할의 메시지는 새로 추가합니다.
    
# 사이드바 설정
with st.sidebar:
    clear_btn = st.button("대화 초기화")
    uploaded_csv_file = st.file_uploader(
        "CSV 파일을 업로드 해주세요.", type=["csv"], accept_multiple_files=False) # csv파일 업로드 기능
    uploaded_pdf_file = st.file_uploader(
        "PDF 파일을 업로드 해주세요.", type=["pdf"], accept_multiple_files=False) # pdf파일 업로드 기능
    selected_model = st.selectbox(
        "OpenAI 모델을 선택해주세요.", ["gpt-4.1-mini", "gpt-4.1-nano"], index=0
    )
    apply_btn = st.button("파일 활용 시작") # 파일 활용 시작 버튼
     