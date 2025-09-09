import sys
import cv2

vcap = cv2.VideoCapture(0)

while True:
    ret, frame = vcap.read()
    if not ret:
        print("카메라가 작동하지 않습니다.")
        sys.exit()

    # 좌우반전
    flipped_frame = cv2.flip(frame, 1)

    # 화면 띄우기
    cv2.imshow("webcam", flipped_frame)

    # 꺼지는 조건
    key = cv2.waitKey(1)
    if key == 27:
        break
vcap.release()
cv2.destroyAllWindows()