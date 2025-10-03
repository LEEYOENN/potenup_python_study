from typing import Dict, List # 타이핑 형식 검증 용
from langchain_core.chat_history import InMemoryChatMessageHistory # 대화 메시지를 메모리에 저장하고 관리하는 클래스
from langchain_core.runnables import RunnableWithMessageHistory # 실행할 때마다 이전 대화 기록을 참고할 수 있게 해줌, 체인이나 파이프라인 실행시, 대화 히스토리를 함께 관리할 수 있게해주는 래퍼클래스
from langchain_core.prompts import MessagesPlaceholder # langchain 프롬프트에서 대화 히스토리(이전메시지)를 삽입할 위치를 지정하는 클래스
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory # DB에 저장되어있는 메시지 히스토리
from langchain_core.runnables.utils import ConfigurableFieldSpec
# LangSmith 추적 설정 부분
from dotenv import load_dotenv
import os
import sys
# 모델
from langchain_openai import ChatOpenAI

# --- 환경변수 가져오기 --- #
load_dotenv()

project_name = "wanted_2nd_prompt_basic"
os.environ["LANGSMITH_PROJECT"] = project_name

#--- 모델 설정 ---#
model = ChatOpenAI(
    temperature=0.1,
    model="gpt-4.1-mini",
    verbose=True
)
# --- DB 세팅 --- #
DB_URL = "sqlite:///chat_history_test.db"


# --- Help 함수 --- #
def get_chat_history(session_id: str, conversation_id: str) -> dict:
    return SQLChatMessageHistory(
        table_name = session_id,
        session_id = conversation_id,
        connection = DB_URL
    )

async def friendly_chat_model(question: str, session_id: str, conversation_id: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 사용자의 아주 편한 친구야. 사용자의 물음에 간결하게 대답해. 항상 반말체로 대답해."),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{question}")
    ])
    chain = prompt | model | StrOutputParser()

    # history 연결
    with_history = RunnableWithMessageHistory(
        chain,
        get_chat_history,
        input_messages_key="question",
        history_messages_key="history",
        history_factory_config=[
                        ConfigurableFieldSpec(
                            id="session_id",
                            annotation=str,
                            name="User ID",
                            description="Unique identifier for the user.",
                            default="",
                            is_shared=True,
                        ),
                        ConfigurableFieldSpec(
                            id="conversation_id",
                            annotation=str,
                            name="Conversation ID",
                            description="Unique identifier for the conversation.",
                            default="",
                            is_shared=True,
                        ),
                    ],
    )
    config = {"configurable": {"session_id": session_id, "conversation_id": conversation_id}}
    response_stream = with_history.astream({"question": question}, config=config)

    # 2. 'async for'를 사용해 비동기 스트림을 순회합니다.
    #    여기서 스트림을 소비(print, full_response +=)하는 대신,
    #    그대로 바깥으로 전달(yield)합니다.
    async for chunk in response_stream:
        # 3. LangChain 스트림의 chunk는 일반적으로 .content 속성에 실제 텍스트를 담고 있습니다.
        #    따라서 chunk 객체 전체가 아닌, chunk.content를 yield 해줍니다.
        yield chunk.content
# if __name__ == '__main__':
#     print(friendly_chat_model("안녕", "user1", "conv1"))