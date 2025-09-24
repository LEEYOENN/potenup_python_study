# (언리얼이 FastAPI 서버에 데이터를 보낸다고 가정)
import websockets
import asyncio
import json

WEBSOCKET_URL = "ws://localhost:8080/ws/streaming"

async def send_message(question):
    async with websockets.connect(WEBSOCKET_URL) as websocket:
        # FastAPI 에게 메시지 전송
        json_data = json.dumps(
            {"question": question}, # json.dumps는 dict 형태를 str로 바꿔줌
            ensure_ascii=False) # 한글이 코드로 전달되는데 한글로 그대로 전달하기위한 코드
        
        await websocket.send(json_data)

        # FastAPI 서버에서 응답 받기
        while True:
            token = await websocket.recv()
            if token == "[END]":
                break

            yield token # return 과 기능은 같다

async def main():
    question = "너 왜그렇게살아."
    async for token in send_message(question):
        print(token, end="", flush=True)

# 실행하기
asyncio.run(main())