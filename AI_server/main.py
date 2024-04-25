from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import voice_recognition, translator, detect, addsubtitle, getaudio
from remove_bad import r_b
from models import Video
import shutil
import os

app = FastAPI()

def pro_tetrancess_text(url): # mp4 video url
  getaudio.getaud(url)
  text, timeline = voice_recognition.recognition()
  lang = detect.detect_language(text)
  return lang, timeline

def remo(timeline):
  return r_b.removal(timeline)

def translate(text):
  return translator.translate_to_korean(text)

def addsub(tl, mp4url):
  return addsubtitle.addsub(tl, mp4url)

@router.post("/upload")
async def upload(file: UploadFile, directory: str):
    if directory not in directories:
        raise HTTPException(status_code=400, detail="유효하지 않는 디렉토리에요")

    filename = f"{str(uuid.uuid4())}.jpg"
    s3_key = f"{directory}/{filename}"

    try:
        s3.upload_fileobj(file.file, BUCKET_NAME, s3_key)
    except (BotoCoreError, ClientError) as e:
        raise HTTPException(status_code=500, detail=f"S3 upload fails: {str(e)}")

    url = "https://s3-ap-northeast-2.amazonaws.com/%s/%s" % (
        BUCKET_NAME,
        urllib.parse.quote(s3_key, safe="~()*!.'"),
    )
    return JSONResponse(content={"url": url})

# @app.get("/videos/{video_id}")
# async def get_video_url(video_id: int):
#     db = SessionLocal()
#     video = db.query(Video).filter(Video.id == video_id).first()
#     if video is None:
#         return {"error": "Video not found"}
#     return {"url": video.url}

# if __name__ == "__main__":
#   # 서버 실행
#   import uvicorn
#   uvicorn.run(app, host="127.0.0.1", port=8000)



# 1. 한국어일 경우          영상을 소리로 변환 -> 소리에서 텍스트 추출 -> 비속어 검열 -> 영상에 자막으로 삽입
# 2. 영어일 경우            영상을 소리로 변환 -> 소리에서 텍스트 추출 -> 비속어 검열 -> 한국어로 번역 -> 영상에 자막으로 삽입