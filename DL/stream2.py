import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from streamlit_drawable_canvas import st_canvas

class_names = ["노홍철", "마동석", "카리나"]

#모델 불러오기

@st.cache_resource ##모델을 캐쉬에 담아놓고 쓰겠다
def load_model():
    model = models.resnet34(pretrained=False)
    model.fc = nn.Linear(512, 3)
    model.load_state_dict(torch.load("./model/mymodel.pth", map_location=torch.device('cpu'))) #모델을 cpu로 불러오기 비용문제
    model.eval()
    return model

def transform_image(image):
    transforms_test = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    return transforms_test(image).unsqueeze(0) #3,224,224


st.title("연예인 분류기 V.1")

upload_file = st.file_uploader("이미지를 업로드 해주세요!", type=["jpg", "png", "jpeg"])

#웹캠사용
#camimg = st.camera_input("웹캠")

canvas_img = st_canvas(
    fill_color="white",
    stroke_width=3,
    stroke_color="black",
    background_color="white",
    height=400,
    width=400,
    drawing_mode="freedraw",
    key='canvas'
)

if canvas_img is not None:
    image = Image.fromarray(canvas_img.image_data).convert('RGB')
    st.image(image, caption="업로드 이미지", use_container_width=True)

    model = load_model() #캐쉬에서 불러온 모델
    infer_img = transform_image(image)

    with torch.no_grad():
        result = model(infer_img)
        preds = torch.max(result, dim=1)[1]

        pred_classname = class_names[preds.item()]
        confidence = torch.softmax(result, dim=1)[0][preds.item()].item() * 100

    
    st.success(f"예측결과: **{pred_classname}** ({confidence:.2f}% 확신)")


