from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from utils.chat_util import friendly_chat_model

# --- 서버 세팅 --- #
app = FastAPI()

@app.get("/chat")
async def chat(question: str, session_id: str, conversation_id: str):
    result = await friendly_chat_model(question=question, session_id=session_id, conversation_id=conversation_id)
    return result
    
# 소켓 통신
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    # STEP1. 클라이언트의 연결을 수락합니다.
    await websocket.accept()
    print("WebSocket 연결됨.")

    try:
        # STEP2. 연결을 유지하며 계속해서 메시지를 받습니다.
        while True:
            # STEP 2-1: 클라이언트로부터 JSON 데이터를 받습니다.
            json_data = await websocket.receive_json()
            question = json_data["question"]
            session_id = json_data["session_id"]
            conversation_id = json_data["conversation_id"]

            # STEP 2-2: 받은 질문으로 비즈니스 로직(모델 호출 등)을 수행합니다.
            response = await friendly_chat_model(
                question=question, session_id=session_id, conversation_id=conversation_id
                )
            
             # STEP 2-3: 결과를 스트리밍하여 클라이언트로 전송합니다.
            for token in response:
                await websocket.send_json({"token": token})
            # (선택사항) 스트리밍이 끝났음을 알리는 메시지를 보낼 수도 있습니다.
            await websocket.send_json({"token": "[DONE]"})
    
    except WebSocketDisconnect:
        # STEP 3-1: 클라이언트가 연결을 끊었을 때 처리합니다.
        print("클라이언트에 의해 WebSocket 연결이 종료되었습니다.")

    except Exception as e:
        print(f"WebSocket 에러 발생: {e}")
    
    finally:
        # STEP 4: 모든 처리가 끝나면 WebSocket 연결을 안전하게 닫습니다.
        # (위 코드에서는 try 블록이 끝나면 자동으로 close가 호출되지는 않지만,
        # WebSocketDisconnect 예외 발생 시 finally가 실행되어 close가 호출됩니다.)
        await websocket.close() # FastAPI가 연결 종료를 자동으로 처리해주는 경우가 많습니다.
        print("WebSocket 리소스 정리 및 연결 종료")