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

async def pro_tetrancess_text(url): # mp4 video url
  getaudio.getaud(url)
  text, timeline = voice_recognition.recognition()
  lang = detect.detect_language(text)
  return lang, timeline

async def remo(timeline):
  return r_b.removal(timeline)

async def translate(text):
  return translator.translate_to_korean(text)

async def addsub(tl, mp4url):
  return addsubtitle.addsub(tl, mp4url)

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://3.36.127.22:3306/removal"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/videos/{video_id}")
async def get_video_url(video_id: int):
    db = SessionLocal()
    video = db.query(Video).filter(Video.id == video_id).first()
    if video is None:
        return {"error": "Video not found"}
    return {"url": video.url}

if __name__ == "__main__":
  # 서버 실행
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)



# 1. 한국어일 경우          영상을 소리로 변환 -> 소리에서 텍스트 추출 -> 비속어 검열 -> 영상에 자막으로 삽입
# 2. 영어일 경우            영상을 소리로 변환 -> 소리에서 텍스트 추출 -> 비속어 검열 -> 한국어로 번역 -> 영상에 자막으로 삽입