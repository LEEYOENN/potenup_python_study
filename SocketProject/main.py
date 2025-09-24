# 서버 실행 : uvicorn main:app --port 8000 --reload
# (주의) 서버 실행 시, 경로가 socket_project여야 합니다.
# uv ad "fastapi[all]"
from fastapi import FastAPI, WebSocket
from models.chatgpt import mychat

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "World"}

# 웹소켓
## 1. (언리얼) 텍스트 <---> (AI) 텍스트 생성 | ChatGPT
## 2. (언리얼) 이미지 <---> (AI) JSON 준다 | mediaPipe
## 3. (언리얼) .wav 파일 <---> (AI) 텍스트 생성 | stt

# 사전에 어떤걸 key로 줄지 정해야한다.

@app.websocket('/ws/streaming')
async def websocket_text(websocket: WebSocket):
    await websocket.accept()

    try:
        # 데이터 받기
        data = await websocket.receive_json()
        print(data, type(data), data["question"])
        # AI 활동
        #response = ["안녕", "반가워", "[END]"]

        response = mychat(data["question"])
        for chunk in response:
            chunk_text = chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")

            if chunk_text is None:
                break
            await websocket.send_text(chunk_text)
        await websocket.send_text("[END]")
    
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
        print("WebSocket Connection Closed")