import cv2
import concurrent.futures
from deepface import DeepFace
from fastapi import FastAPI, UploadFile, File
from typing import List
import tempfile
import shutil

app = FastAPI()

def process_frame(frame):
    try:
        if frame is None or frame.size == 0:
            print("Empty frame received")
            return None

        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=True, detector_backend='mtcnn')
        return result
    except Exception as e:
        print(f"Error processing frame: {e}")
        return None

def video_emotion_analysis(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name

    video = cv2.VideoCapture(temp_file_path)

    if not video.isOpened():
        print("Could not open video")
        return

    # 비디오의 프레임 속도를 얻습니다.
    fps = video.get(cv2.CAP_PROP_FPS)

    frames_to_analyze = []
    frame_index = 0
    while True:
        ret, frame = video.read()
        
        if not ret:
            break

        # 5초 간격으로 프레임을 선택합니다.
        if frame_index % (5 * fps) == 0:
            frames_to_analyze.append(frame)

        frame_index += 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_frame, frames_to_analyze))

    for result in results:
        if result:
            print(f"Results for {file.filename}: {result}")

    return results