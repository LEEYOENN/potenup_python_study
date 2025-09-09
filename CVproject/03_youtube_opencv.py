# uv add yt_dlp
import yt_dlp
import cv2
from ultralytics import YOLO

# YOLO 모델 로드
model = YOLO('yolo11n.pt')

video_url = "https://youtu.be/S5nsDT5oU90"

# yt_dlp 옵션 설정
ydl_opts = {
    "format": "bes[ext=mp4][protocol=https]/best",
    "quite": True,
    'no_warnings': True
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(video_url, download=False)
    stream_url = info_dict['url']

vcap = cv2.VideoCapture(stream_url)

while True:
    if not vcap.isOpened():
        print('비디오를 열 수 없습니다.')
        break

    #카메라 동작여부, 프레임 읽기
    ret, frame = vcap.read()
    print(ret)

    if not ret:
        print("비디오 프레임을 읽어올 수 없습니다.")
        break
    
    # YOLO 모델 사용한 객체탐지 진행
    results = model(frame, conf=0.75)
    result = results[0]
    boxes = result.boxes
    print(boxes.data)

    # 바운딩박스 그리기
    cnt = 0
    for x1, y1, x2, y2, conf, idx in boxes.data:
        # 사람만 박스 그리기위한 조건
        if idx != 0:
            continue

        #사람수 카운팅
        cnt += 1
        #박스좌표를 정수 변환
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        # rectangle 인자 순서 (frame, (x1, y1), (x2, y2), 색상, 두께, 기타옵션)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    
    # 텍스트작성
    cnt_text = f"Person Count: {cnt}"
    # putText 인자 순서(frame, 텍스트, 위치, 폰트, 크기, 색상, 두께)
    cv2.putText(frame, cnt_text, (5,30), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 255, 0), 2)
    cv2.imshow("Youtube Video", frame)

    #종료 조건
    key = cv2.waitKey(1)
    if key == 27:
        break

vcap.release()
cv2.destroyAllWindows()
