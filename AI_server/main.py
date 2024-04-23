from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from typing import List
from video2audio import ffmpeg
from model import voice_recognition, translator, detect
from remove_bad import r_b
import shutil
import os

app = FastAPI()

async def pro_tetrancess_text(url):
  ffmpeg.video_to_audio(url)
  text, timeline = voice_recognition.recognition()
  lang = detect.detect_language(text)
  return lang, timeline

async def remo(timeline):
  return r_b.removal(timeline)

async def translate(text):
  return translator.translate_to_korean(text)

@app.post("")

@app.get("/video/{video_name}")
async def get_processed_video(video_name: str):
  video_path = os.path.join("processed_videos", video_name)
  if os.path.exists(video_path):
    return FileResponse(video_path, media_type="video/mp4")
  else:
    return {"error": "Video not found"}

if __name__ == "__main__":
  # 서버 실행
  import uvicorn
  uvicorn.run(app, host="127.0.0.0", port=8000)




# 1. 한국어일 경우          영상을 소리로 변환 -> 소리에서 텍스트 추출 -> 비속어 검열 -> 영상에 자막으로 삽입
# 2. 영어일 경우            영상을 소리로 변환 -> 소리에서 텍스트 추출 -> 비속어 검열 -> 한국어로 번역 -> 영상에 자막으로 삽입