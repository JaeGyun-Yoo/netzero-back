import speech_recognition as sr
from fastapi import File, UploadFile, HTTPException
import io

r = sr.Recognizer()


async def audio_to_text(answer_audio_file): #wav 파일 처리 가능함
    try:
        audio_data = await answer_audio_file.read()
        with io.BytesIO(audio_data) as audio_data_io, sr.AudioFile(audio_data_io) as source:
            audio = r.record(source)
        text = r.recognize_google(audio_data=audio, language='ko-KR')
        return {"text": text}
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Speech Recognition request failed: {e}")
    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Could not understand the audio")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

