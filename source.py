import cv2 as cv

# 웹캠을 캡처하는 객체 생성 (0번 카메라 사용)
cap = cv.VideoCapture(0)

# 동영상 저장을 위한 설정
fourcc = cv.VideoWriter_fourcc(*'XVID')  # 코덱 설정 (XVID, MP4V 등)
out = None  # VideoWriter 객체 초기화
is_recording = False  # 녹화 상태 변수

while True:
    ret, frame = cap.read()  # 프레임 읽기
    if not ret:
        break  # 프레임을 제대로 읽지 못하면 종료
    
    if is_recording:
        if out is None:
            out = cv.VideoWriter('output.avi', fourcc, 20.0, (frame.shape[1], frame.shape[0]))  # 비디오 파일 생성
        out.write(frame)  # 프레임 저장
        cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)  # 화면에 빨간색 원 표시 (녹화 중 표시)
        
    cv.imshow('Video Recorder', frame)  # 화면에 프레임 표시

    key = cv.waitKey(1) & 0xFF
    if key == 27:  # ESC 키를 누르면 종료
        break
    elif key == 32:  # Space 키를 누르면 녹화 모드 변경
        is_recording = not is_recording
        if not is_recording and out is not None:
            out.release()  # 녹화 중지 시 파일 저장 완료
            out = None

# 리소스 해제
cap.release()
if out is not None:
    out.release()
cv.destroyAllWindows()
