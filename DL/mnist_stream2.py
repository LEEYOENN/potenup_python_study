import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from torchvision.datasets.mnist import MNIST
import numpy as np

class_names = [str(i) for i in range(10)]

#모델 불러오기
@st.cache_resource
def load_model():
    model = nn.Sequential(
        nn.Linear(784, 64),
        nn.ReLU(),
        nn.Linear(64, 64),
        nn.ReLU(),
        nn.Linear(64, 32),
        nn.ReLU(),
        nn.Linear(32, 10)

    )
    model.load_state_dict(torch.load('model/mnist_model_weight_08_22.pth', map_location=torch.device('cpu')))
    model.eval()
    return model

#이미지 전처리 함수
def transform_image(image):
    transforms_test = transforms.Compose(
        [
            transforms.Grayscale(num_output_channels=1),
            transforms.Resize((28, 28)),
            transforms.ToTensor()
        ]
    )
    return transforms_test(image).unsqueeze(0)


st.title("손글씨 분류기 V.1")

canvas_img = st_canvas(
    fill_color='black', # MNIST와 동일하게 검은색 배경으로 변경
    stroke_width=5, # 펜 굵기
    stroke_color='white', # MNIST와 동일하게 흰색 펜으로 변경
    background_color='black',
    height=400,
    width=400,
    drawing_mode="freedraw",
    key = "canvas"
)


if canvas_img.image_data is not None: # 업로드 된 파일이 있으면
    image = Image.fromarray(canvas_img.image_data.astype('uint8'), 'RGBA') 
    if np.sum(image.getchannel('A').getdata()) > 0: #캔버스의 모든 픽셀을 확인하여 하나라도 투명하지 않은(즉, 무언가 그려진) 픽셀이 있는지 검사하는 역할
        st.image(image, caption="그려진 이미지", use_container_width=True)

        # 모델 로드
        model = load_model()

#모델을 위한 이미지 전처리
        infer_img = transform_image(image)

#이미지를 784 크기의 1차원 텐서로 변환
        infer_img = infer_img.view(-1, 784)

#추론 수행
        with torch.no_grad():
            result = model(infer_img)
            preds = torch.max(result, dim=1)[1]
            pred_classname = class_names[preds.item()]

            # 수정된 부분: result 텐서에 softmax를 적용하여 신뢰도 계산
            confidence = torch.softmax(result, dim=1)[0][preds.item()].item() * 100

            st.success(f'예측 결과: {pred_classname} ({confidence:.2f}% 확신)')