import sys
import cv2
import mediapipe as mp
import os
import joblib
import numpy as np

#mediapipe hand landmark 옵션
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
# 모델 불러오기, 라벨 정의
model = joblib.load("rock_scissors_paper.pkl")
label = {"Rock": 0, "Scissors":1, "Paper":2}
labels = ["Rock", "Scissors", "Paper"]
# 웹캠
#    # 카메라 감지
vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()
    # 좌우 반전
    frame = cv2.flip(frame, 1)
    # 손 그리기 준비
    frame.flags.writeable = True
    # 손 감지
    results = hands.process(frame)
    # Hand Landmark 추출
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            height, width, _ = frame.shape 
           # 손 하나의 Hand Landmark 추출
            data = []
            for landmark in hand_landmarks.landmark:
                #좌표 데이터
                data.extend([landmark.x, landmark.y, landmark.z])

                # 저장 데이터 만들기, 포인트 그리기
                point_x = int(landmark.x * width) # landmark.x 는 이미지에서의 비율적 위치(소수점)을 리턴하기 때문에 화면 넓이를 곱해줘야한다.
                point_y = int(landmark.y * height)

                cv2.circle(frame, (point_x, point_y), 5, (0, 255, 0), 2)
                # 예측
            pred = model.predict(np.array([data]))
            cv2.putText(frame, f"Your choice is {labels[pred[0]]}", (10, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    # 화면 띄우기
    cv2.imshow("webcam", frame)
    # ECS 누르면 종료
    key = cv2.waitKey(1)
    if key == 27: #ESC
        break
    
# 마무리
vcap.release()
cv2.destroyAllWindows