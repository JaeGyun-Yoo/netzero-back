from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from pdf_to_text import pdf_to_text
import os
import shutil
from chat_gpt import train_gpt_as_interviewer, get_question_from_gpt, reply_to_gpt,  get_feedback_from_gpt, post_to_gpt, get_question_answer_list, test_to_gpt
from audio_to_text import audio_to_text
from non_verbal_behavior import get_feedback_non_verbal_behavior
from test import post_to_gpt_test
from emotion_analysis import video_emotion_analysis


app = FastAPI()
origins = ["*"]

class Test(BaseModel):
    a:str
    b:str

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.post("/train-gpt")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 파일 저장 경로 설정
        file_path = os.path.join("uploads", file.filename)

        # 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        # 파일 저장 중에 오류 발생
        raise HTTPException(status_code=500, detail=f"파일 저장 중 오류 발생: {e}")

    try:
        # PDF 파일을 텍스트로 변환
        file_text = pdf_to_text(file.filename)
    except Exception as e:
        # PDF 파일 처리 중 오류 발생
        raise HTTPException(status_code=500, detail=f"PDF 파일 처리 중 오류 발생: {e}")

    try:
        # OpenAI GPT를 사용하여 인터뷰 질문 생성
        return train_gpt_as_interviewer(file_text)
    except Exception as e:
        # GPT 호출 중 오류 발생
        raise HTTPException(status_code=500, detail=f"GPT 호출 중 오류 발생: {e}")



@app.post("/get-question")
async def get_question():
    return get_question_from_gpt()


@app.post("/answer")
async def answer(answer_audio_file: UploadFile = File(...)):
    audio_text = await audio_to_text(answer_audio_file)
    print(audio_text)
    return reply_to_gpt(audio_text)

@app.get("/get-feedback")
async def get_feedback():
    return get_feedback_from_gpt()

@app.post("/get-feedback-non-verbal-behavior")
async def upload_video_stream_then_get_feedback(file: UploadFile = File(...)):
    return get_feedback_non_verbal_behavior(file)

@app.post("/answer-with-text")
async def answer_with_text(answer: str):
    return reply_to_gpt(answer)


@app.get("/test")
async def test():
    return post_to_gpt_test()

@app.post("/real-test")
async def real_test(test: Test):
    return post_to_gpt(test.a, test.b)

@app.get("/get-question-answer-list")
def get_list():
    return get_question_answer_list
class Result(BaseModel):
    filename: str
    content_type: str
    emotions: dict



@app.post("/video-analysis")
async def get_video_analysis(file: UploadFile = File(...)):
    emotions = video_emotion_analysis(file)
    
    result = {
        "filename": file.filename,
        "content_type": file.content_type,
        "emotions": emotions
    }

    return result


@app.post("/video-test")
async def get_video_analysis(file: UploadFile = File(...)):
    emotions = video_emotion_analysis(file)

    return test_to_gpt(emotions)