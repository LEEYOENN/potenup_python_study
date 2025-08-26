import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import torch.nn.functional as F
import numpy as np

class_names = [ str(i) for i in range(10) ]

@st.cache_resource ##모델을 캐쉬에 담아놓고 쓰겠다
def load_model():
    model = nn.Sequential( 
        nn.Linear(28*28, 64),
        nn.ReLU(), 
        nn.Linear(64, 64), 
        nn.ReLU(), 
        nn.Linear(64, 32), 
        nn.ReLU(), 
        nn.Linear(32, 10) 
        )
    state = torch.load("model/mnist_model_weight_08_22.pth",
                       map_location=torch.device('cpu'))

    model.load_state_dict(state)
    model.eval()
    return model

def transform_image(image):
    transforms_test = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((28, 28)),                   # 28x28 크기 조정
        transforms.ToTensor(), 
        #transforms.Lambda(lambda t: 1.0 - t), # 흑/백 반전
        #transforms.Normalize((0.1307,), (0.3081,))     # MNIST 평균, 표준편차
    ])
    return transforms_test(image).unsqueeze(0)

def has_strokes(pil_rgba, thr=220, min_pixels=50):
    # RGBA → L(그레이)
    g = pil_rgba.convert("RGB").convert("L")
    arr = np.array(g, dtype=np.uint8)
    # 흰 선(밝은 픽셀) 개수 세기
    return (arr > thr).sum() >= min_pixels

USE_NORMALIZE = True   # 학습 때 Normalize((0.1307,), (0.3081,)) 썼으면 True
THRESH = 40            # 이진화 임계값(30~80 사이 조정)
PADDING = 4            # 숫자 주변 여백

def preprocess_canvas_image(pil_rgba, normalize=USE_NORMALIZE):
    # RGBA → RGB → L
    img = pil_rgba.convert("RGB").convert("L")   # 0(검)~255(흰)
    arr = np.array(img, dtype=np.uint8)

    # 지금은 배경=검정, 선=흰색 → MNIST와 같으므로 반전 불필요
    # (배경 흰/선 검이면 arr = 255 - arr)

    # 이진화(얇은 선/노이즈 제거)
    bin_ = np.where(arr > THRESH, 255, 0).astype(np.uint8)

    # 바운딩박스 크롭
    ys, xs = np.where(bin_ > 0)
    if len(xs) and len(ys):
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        crop = bin_[y0:y1+1, x0:x1+1]
    else:
        # 아무것도 안 그렸을 때: 중앙 점
        crop = np.zeros((28, 28), dtype=np.uint8)
        crop[13:15, 13:15] = 255

    # 정사각 패딩
    h, w = crop.shape
    size = max(h, w) + 2*PADDING
    square = np.zeros((size, size), dtype=np.uint8)
    y = (size - h)//2
    x = (size - w)//2
    square[y:y+h, x:x+w] = crop

    # 28×28 리사이즈
    img28 = Image.fromarray(square).resize((28, 28), Image.BILINEAR)

    # 텐서(+정규화)
    t = transforms.ToTensor()(img28)  # [1, 28, 28], 값 0~1
    if normalize:
        t = transforms.Normalize((0.1307,), (0.3081,))(t)
    return t, img28
st.title("손글씨 숫자 분류기 V.1")

#upload_file = st.file_uploader("이미지를 업로드 해주세요!", type=["jpg", "png", "jpeg"])

#웹캠사용
#camimg = st.camera_input("웹캠")

canvas_img = st_canvas(
    fill_color="black",
    stroke_width=20,         # 선은 굵을수록 유리(10→20 추천)
    stroke_color="white",
    background_color="black",
    height=500, width=500,
    drawing_mode="freedraw",
    key='canvas'
)

if canvas_img is not None and canvas_img.image_data is not None:
    image = Image.fromarray(canvas_img.image_data.astype('uint8'), 'RGBA')

    if not has_strokes(image):
        st.info("그림을 조금 더 진하게/굵게 그려주세요!")
        st.stop()

    # 전처리 + 미리보기
    x28, preview = preprocess_canvas_image(image)
    st.image(preview.resize((140, 140)), caption="전처리 미리보기(28×28)")

    infer_x = x28.view(1, -1)   # [1, 784]

    model = load_model()
    with torch.no_grad():
        logits = model(infer_x)                 # [1, 10]
        pred = logits.argmax(dim=1).item()
        prob = torch.softmax(logits, dim=1)[0, pred].item() * 100

    st.success(f"예측결과: **{pred}** ({prob:.2f}% 확신)")

# canvas_img = st_canvas(
#     fill_color="black",
#     stroke_width=10,
#     stroke_color="white",
#     background_color="black",
#     height=400,
#     width=400,
#     drawing_mode="freedraw",
#     key='canvas'
# )

# if canvas_img is not None:
#     image = Image.fromarray(canvas_img.image_data.astype('uint8'), 'RGBA')
#     if np.sum(image.getchannel('A').getdata()) > 0: #캔버스의 모든 픽셀을 확인하여 하나라도 투명하지 않은(즉, 무언가 그려진) 픽셀이 있는지 검사하는 역할
#         st.image(image, caption="그려진 이미지", use_container_width=True)

#     #st.image(image, caption="업로드 이미지", use_container_width=True)

#     model = load_model() #캐쉬에서 불러온 모델
#     infer_img = transform_image(image)
#     infer_img = torch.flatten(infer_img, start_dim=1)

#     with torch.no_grad():
#         result = model(infer_img)
#         preds = torch.max(result, dim=1)[1]

#         pred_classname = class_names[preds.item()]
#         confidence = torch.softmax(result, dim=1)[0][preds.item()].item() * 100

    
#     st.success(f"예측결과: **{pred_classname}** ({confidence:.2f}% 확신)")

