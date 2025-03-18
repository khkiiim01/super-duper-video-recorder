import cv2 as cv
import os
import numpy as np

cap = cv.VideoCapture(0)

fourcc = cv.VideoWriter_fourcc(*'XVID')  # 코덱 설정 (XVID)
out = None  
is_recording = False
recording_count = 0  # 녹화 파일 번호
contrast_factor = 1.0  # 대비 계수 (1.0 = 원본)

def adjust_contrast(frame, factor):
    """대비를 조절하는 함수 (감마 보정 방식)"""
    if factor == 1.0:
        return frame  # 원본 유지
    gamma = max(0.1, min(3.0, factor))
    invGamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** invGamma * 255 for i in range(256)]).astype("uint8")
    return cv.LUT(frame, table)

while True:
    ret, frame = cap.read() 
    if not ret:
        break 
    
    # contrast 조절
    frame = adjust_contrast(frame, contrast_factor)

    if is_recording:
        if out is None:
            filename = f'output{recording_count}.avi'
            while os.path.exists(filename):  # 기존 파일이 있으면 숫자 증가
                recording_count += 1
                filename = f'output{recording_count}.avi'

            out = cv.VideoWriter(filename, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
        
        out.write(frame)  # 프레임 저장
        cv.circle(frame, (50, 50), 10, (0, 0, 255), -1)  # 녹화 중일 때 빨간 원 표시
    
    cv.imshow('Video Recorder', frame)

    key = cv.waitKey(1)  # 키 입력력
    
    if key == 27:  # ESC 키 → 종료
        break
    elif key == 32:  # Space 키 → 녹화 시작/중지
        is_recording = not is_recording
        if is_recording:
            recording_count += 1  # 새로운 파일 번호 증가
        else:
            if out is not None:
                out.release()  # 녹화 중지 시 파일 저장 완료
                out = None
    elif key == ord('1'):  # '1' 키 → 대비 증가
        contrast_factor = min(contrast_factor + 0.1, 2.5)  # 최대 2.5까지 제한
        print(f"Contrast Increased: {contrast_factor:.1f}")
    elif key == ord('2'):  # '2' 키 → 대비 감소
        contrast_factor = max(contrast_factor - 0.1, 0.5)  # 최소 0.5까지 제한
        print(f"Contrast Decreased: {contrast_factor:.1f}")

cap.release()
if out is not None:
    out.release()
cv.destroyAllWindows()
