import sys
import cv2
import mediapipe as mp

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
vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()

    # 좌우반전
    frame = cv2.flip(frame, 1)

    ######## Hands Landmark 추출 ##########

    # 손 그리기 설정
    frame.flags.writeable = True

    # 손 감지하기
    results = hands.process(frame)

    #추출 및 그리기
    if results.multi_hand_landmarks:
        #print(len(results.multi_hand_landmarks)) # 손이 몇개 탐지 되는가?
        for hand_landmarks in results.multi_hand_landmarks:
            #print(len(hand_landmarks.landmark)) # 한개의 손마다 좌표가 몇개 나오나?

            # # 자동 그리기
            # mp_drawing.draw_landmarks(
            #     frame,
            #     hand_landmarks,
            #     mp_hands.HAND_CONNECTIONS,
            #     mp_drawing_styles.get_default_hand_landmarks_style(),
            #     mp_drawing_styles.get_default_hand_connections_style()
            # )

            # 좌표 데이터 리스트로 만들기
            landmark_list = []
            # 직접 그리기
            height, width, _ = frame.shape 

            for landmark in hand_landmarks.landmark:

                #좌표 데이터 리스트로 만들기
                landmark_list.extend([landmark.x, landmark.y, landmark.z])
                print(len(landmark_list))
                point_x = int(landmark.x * width) # landmark.x 는 이미지에서의 비율적 위치(소수점)을 리턴하기 때문에 화면 넓이를 곱해줘야한다.
                point_y = int(landmark.y * height)

                cv2.circle(frame, (point_x, point_y), 5, (0, 255, 0), 2)
    ######################################

    #화면 띄우기
    cv2.imshow("webcam", frame)

    # 꺼지는 조건
    key = cv2.waitKey(1)
    if key == ord("1"):
        print("1-key를 눌렀습니다.", {ord("1")})
    elif key == ord("2"):
        print("2-key를 눌렀습니다.")
    elif key == ord("3"):
        print("3-key를 눌렀습니다.")

    if key == 27: #ESC
        break

vcap.release()
cv2.destroyAllWindows()