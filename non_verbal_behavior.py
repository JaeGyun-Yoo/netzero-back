from fastapi import File, UploadFile
import cv2
import numpy as np
        
async def detect_eye_direction(frame:np.ndarray):
    print("eye")
async def detect_head_angle(frame:np.ndarray):
    print("angle")
async def detect_emotion(frame:np.ndarray):
    print("emotion")
    
    
def detect(frame:np.ndarray):
    eye_direction = detect_eye_direction(frame)
    head_angle = detect_head_angle(frame)
    emotion = detect_emotion(frame)
    return eye_direction, head_angle,emotion

async def get_feedback_non_verbal_behavior(video_file: UploadFile = File(...)):
    video_stream = video_file.file
    video_capture = cv2.VideoCapture(video_stream)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            break
        
        eye_direction ,head_angle, emotion = detect(frame)

        # 결과를 출력하거나 다른 곳에 저장한다.
        print(eye_direction, head_angle, emotion)    
        
        