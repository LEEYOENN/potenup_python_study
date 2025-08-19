from fastapi import FastAPI

app = FastAPI()


@app.get("/image")
def make_image():
    return {
        "result": "카리나"
        }

@app.get("/chatbot")
def chat():
    return {
            "result": '안녕하세요 저는 ChatGPT입니다.'
        }

@app.get("/video")
def ohaoh():
    return {
        "result": "동영상 생성이 완료되었습니다."
        }


