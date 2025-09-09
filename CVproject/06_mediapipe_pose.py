import cv2
import mediapipe as mp
import sys

# mediapipe의 Pose Landmark를 추출하기 위한 옵션
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles

pose = mp_pose.Pose(
    static_image_mode = False,
    model_complexity = 1,
    smooth_landmarks=True,
    enable_segmentation=True,
    min_detection_confidence= 0.5,
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

    ####### Pose Landmark 그리기 #######
    #포즈 그리기 준비
    frame.flags.writeable = True

    #포즈 감지
    results = pose.process(frame)

    #자동 그리기
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing_style.get_default_pose_landmarks_style()
    )
    ##########################
    
    # 화면 띄우기
    cv2.imshow("webcam", frame)

    # 꺼지는 조건
    key = cv2.waitKey(1)
    if key == 27:
        break
vcap.release()
cv2.destroyAllWindows()