from fastapi import FastAPI, File, UploadFile, HTTPException, Path
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import voice_recognition, translator, detect, addsubtitle, getaudio
from remove_bad import r_b
from models import Video
import os

app = FastAPI()

def save_result_to_file(result):
  file_path = "./location.txt"
  with open(file_path, "a") as file:
    file.write(str(result) + "\n")

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

@app.post("/upload/") # 클라이언트 입장 post
async def upload_video(video: UploadFile = File(...)):
  
  output_folder = "../Removal-AI/AI_server/video/"
  os.makedirs(output_folder, exist_ok=True)
  contents = await video.read()

  output_path = os.path.join(output_folder, video.filename)
  with open(output_path, "wb") as f:
    f.write(contents)

  video_url = output_folder + video.filename

  lang, timeline = pro_tetrancess_text(video_url)
  timeline = remo(timeline)
  if lang == 'eng':
    timeline = translate(timeline)

  save_result_to_file(addsub(timeline, video_url))
  return "SUCCESS"

@app.get("/download/") # 클라이언트 입장 get
async def give_video_url():
  file_path = open('./location.txt', 'r')
  file_path = file_path.readline()
  if not Path(file_path).is_file():
    raise HTTPException(status_code=404, detail="File not found")

  return FileResponse(file_path, media_type="video/mp4")

if __name__ == "__main__":
  # 서버 실행
  import uvicorn
  uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)