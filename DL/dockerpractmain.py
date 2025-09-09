from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
from pydantic import BaseModel
from PIL import Image
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
import json
import torch
import uuid

# 사용자 데이터를 저장하는거 중요함
app = FastAPI(title="ResNet34 Inference Test")

device = 'cuda' if torch.cuda.is_available() else 'cpu'

weights = models.ResNet34_Weights.DEFAULT
model = models.resnet34(weights=weights)

model.fc = nn.Linear(in_features=512, out_features=3, bias=True)
model.load_state_dict(torch.load('./model/mymodel.pth'))

#이 모델은 추론에만 써서 가중치는 건드리지 말라는 뜻
model.eval()
model = model.to(device)

transforms_infer = transforms.Compose([
    transforms.Resize((224,224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

class Response(BaseModel):
    name: str
    score: float
    type: int

@app.get("/")
def root():
    return {"message": "This is a test api"}

@app.post("/predict", response_model=Response)
#이렇게 하면 자동으로 첨부되어진 파일을 뽑아줌(file 이란 key값과 함께 전달해야만 함)
async def predict_image(file: UploadFile = File(...)):
    image = Image.open(file.file)

    # 들어온 이미지를 저장해줘야함
    file_uuid = str(uuid.uuid4())
    file_extension = file.filename.split(".")[1]
    filename = f"{file_uuid}.{file_extension}"

    image.save(f"./imgdata/{filename}")

    # 전처리 적용 후
    img_tensor = transforms_infer(image).unsqueeze(0)

    with torch.no_grad():
        pred = model(img_tensor)
        #print("예측값: ", pred)
    pred_result = torch.max(pred, dim=1)[1].item()
    score = torch.softmax(pred, dim=1)[0][pred_result].item()
    classname = ['노홍철', '마동석', '카리나']

    name = classname[pred_result]

    return Response(name=name, score=float(score[pred_result]), type=pred_result)
