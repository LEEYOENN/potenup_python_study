import sys
import cv2
import mediapipe as mp

# mediapipe의 Hand Landmark 를 추출을 위한 옵션
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode = False, #고정이미지 아님
    max_num_hands = 2,
    min_detection_confidence = 0.3, #감지 확률 0.5 이상만
    min_tracking_confidence = 0.3 # 트래킹 확률 0.5 이상만
)

vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    if not ret:
        print("웹캠이 작동하지 않습니다.")
        sys.exit()

    ###### Hands Landmark 설정하기 ########


    # 손 감지하기
    results = hands.process(frame)

    #print(results)

    # 그리기
    if results.multi_hand_landmarks:
        #print(len(results.multi_hand_landmarks)) # 손이 몇개 탐지 되는가?
        for hand_landmarks in results.multi_hand_landmarks:
            #print(len(hnad_landmarks.landmark)) # 한개의 손마다 좌표가 몇개 나오나?21개
            #print(hand_landmarks.landmark)
            height, width, _ = frame.shape # (h, w, c)

            for idx, landmark in enumerate(hand_landmarks.landmark):
                #print(landmark.x, landmark.y)
                if idx in [5, 6, 7, 8, 9, 10, 11, 12]:
                    print(f"{idx}번째 좌표: x:{landmark.x}, y:{landmark.y}, z:{landmark.z}")
                    point_x = int(landmark.x * width) # 소수점인 x좌표를 우리 화면 해상도에 맞는 좌표 정수로 변환
                    point_y = int(landmark.y * height)
                    cv2.circle(frame, (point_x, point_y), 5, (0, 255, 0), 1)
                #cv2.circle(frame, (point_x, point_y), 5, (0, 255, 0), 1)
           
            # 자동 그리기    
            # mp_drawing.draw_landmarks(
            #     frame,
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style()
            # )

    # 좌우 반전
    flipped_frame = cv2.flip(frame, 1)
    #contrast_frame = 255 - flipped_frame

    rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
        # 손 그리기 설정
    frame.flags.writeable = False
    # 화면 띄우기
    cv2.imshow("webcam", flipped_frame)

    # 꺼지는 조건
    key = cv2.waitKey(1)
    if key == 27:
        break

vcap.release()
cv2.destroyAllWindows()