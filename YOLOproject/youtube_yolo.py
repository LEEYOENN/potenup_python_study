# 모델 불러오기
from ultralytics import YOLO
import cv2

model = YOLO('yolo11n.pt')

# 유튜브 url 가져오기
youtube_url = "https://youtu.be/S5nsDT5oU90"

# 예측하기
results = model(youtube_url, stream=True)

    # 스트리밍 결과를 반복해서 소비해야 화면이 뜸
for r in model(source=youtube_url, stream=True, conf=0.25, imgsz=640, show=False):
    # r.plot() -> 감지 박스가 그려진 numpy 이미지(BGR)
    im0 = r.plot()
    cv2.imshow("YOLO-YouTube", im0)

    # ESC(27) 누르면 종료
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()