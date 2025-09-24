from openai import OpenAI
import json

# STEP1. 환경변수 불러오기
from dotenv import load_dotenv
load_dotenv()

# STEP2. OpenAI 객체 생성
client = OpenAI()

# STEP3. 시스템 프롬프트 만들기
system_prompt = """
    당신은 친절하고 도움이 되는 챗봇 어시스턴트입니다.
    질문이 들어오면 논리적이고 이해되기 쉽게 설명해줍니다.
    꼭 존댓말을 사용하세요.
    상대방이 쓰는 언어에 맞춰서 대답해주세요.
    질문자가 의미없는 말을 하면 '헛소리 하지마세요.' 라고 대답하세요.

    [대화 히스토리]는 사용자와 당신이 나눈 대화입니다. 
    이 대화를 참고해서 사용자의 질문에 답변해주세요.

    [대화 히스토리]
"""

# STEP4. 채팅하는 함수 만들기
def mychat(input_text):
    # 현재 st.session_state["messages"]는 딕셔너리가 포하뫼어 있는 리스트
    # 문자열로 바꿔서 넣어주어야 한다.

    #history_str = json.dumps(history, ensure_ascii=False)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input_text}
    ]

    # print("=" * 50)
    # print(system_prompt)
    # #print(history_str)
    # print("=" * 50)
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages,
        stream=True
    )

    return response