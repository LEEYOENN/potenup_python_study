from fastapi import FastAPI, UploadFile, File
import uvicorn
from ultralytics import YOLO
from pydantic import BaseModel
from PIL import Image

#모델을 한번만 불러오도록 하는게 좋다 -> refactoring 필요
model = YOLO('yolo11n.pt')

app = FastAPI()

# 객체 1개
class Data(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float
    conf: float
    clss: int
    label: str

# 감지된 객체 목록
class YoloResponse(BaseModel):
    data: list[Data]

@app.get("/")
def read_root():
    return {"message": "Hello, This is YOLO11n API main page"}

@app.post("/yolo", response_model=YoloResponse)
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file).convert('RGB')
    results = model(image)

    result = results[0]
    datas = []
    for x1, y1, x2, y2, conf, clss in result.boxes.data:
        datas.append(
            Data(x1=x1, y1=y1, x2=x2, y2=y2,
                conf=conf, clss=clss, label=result.names[int(clss)])
        )
    return YoloResponse(data=datas)

@app.get("/text")
def read_text():
    return {"message" : "안녕하세요"}

@app.post("/chat")
def read_chat(text: str):
    return {"message" : "안녕하세요"}


#이렇게 하라는건지 그냥 boxes.data를 str로 변환해서 보내는 건가
