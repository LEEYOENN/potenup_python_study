# 모델을 띄우기 -> 사용자 요청이 오면 -> 요청을 띄우기
from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
from pydantic import BaseModel
from PIL import Image
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
import json
import torch

# 사용자 데이터를 저장하는 거 중요

app = FastAPI(title="ResNet34 Inference")

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model = models.resnet34(pretrained=True)

model.fc = nn.Linear(in_features=512, out_features=3, bias=True)
model.load_state_dict(torch.load('./model/mymodel.pth'))

#이 모델은 추론용으로 쓸거니까 가중치를 건드리지 말라는뜻
model.eval()
model = model.to(device)

transforms_infer = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

class Response(BaseModel):
    name: str
    score: float
    type: int

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/predict", response_model=Response)
async def predict_image(file: UploadFile = File(...)): # **자동으로 첨부되어진 파일을 뽑아준다 file이란 key값이 꼭 들어와야된다.
    image = Image.open(file.file)

    # 들어온 이미지를 save
    image.save("./imgdata/test.jpg") #uuid, timestamp
    img_tensor = transforms_infer(image).unsqueeze(0).to(device) # [3, 224, 224] tensor

    with torch.no_grad():
        pred = model(img_tensor)
        print("예측값:", pred)
    pred_result = torch.max(pred, dim=1)[1].item() #0, 1, 2
    score = nn.Softmax()(pred)[0] # [0.03, 0.9, 0.07]
    classname = ['노홍철', '마동석', '카리나']

    name = classname[pred_result]

    return Response(name=name, score=float(score[pred_result]), type=pred_result)    

#우선 더미데이터를 반환해서 프론트 작업을 할수있게 해준다
@app.post("/trash_predict", response_model=Response)
async def trash_predict(file: UploadFile = File(...)):
    return Response(name="pet", score=0.0, type=2)



    


