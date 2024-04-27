from fastapi import FastAPI, File, UploadFile, HTTPException, Path, Form
from fastapi.responses import FileResponse
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import voice_recognition, translator, detect, addsubtitle
from model import getaudio, delete
from model.tomp4 import convert_to_mp4
from remove_bad import r_b
from models import Video
import os

app = FastAPI()

def tomp4(output_path):
  convert_to_mp4(output_path)

def save_result_to_file(result):
  file_path = "../Removal-AI/AI_server/location.txt"
  with open(file_path, "w") as file:
    file.write(str(result))

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

@app.post("/removal")
async def removebad(video3: UploadFile = File(...)):
  with open("../Removal-AI/AI_server/location.txt", "w") as file:
    file.write("")
  delete.delete_all_files('../Removal-AI/AI_server/video/output')
  delete.delete_all_files('../Removal-AI/AI_server/video/outvid')
  delete.delete_all_mp4_files('../Removal-AI/AI_server/video')
  output_folder = "../Removal-AI/AI_server/video/"
  video3.filename = video3.filename[:-4] + ".mp4"
  output_path = os.path.join(output_folder, video3.filename)
  tomp4(output_folder[:-1])
  os.makedirs(output_folder, exist_ok=True)
  contents = await video3.read()

  output_path = os.path.join(output_folder, video3.filename)
  with open(output_path, "wb") as f:
    f.write(contents)

  video_url = output_folder + video3.filename

  lang, timeline = pro_tetrancess_text(video_url)
  timeline = remo(timeline)
  # if lang == 'eng':
  #   timeline = translate(timeline)

  save_result_to_file(addsub(timeline, video_url))
  return "removing bad word SUCCESS"

@app.post("/translate")
async def upload_video(video2: UploadFile = File(...)):
  with open("../Removal-AI/AI_server/location.txt", "w") as file:
    file.write("")
  delete.delete_all_files('../Removal-AI/AI_server/video/output')
  delete.delete_all_files('../Removal-AI/AI_server/video/outvid')
  delete.delete_all_mp4_files('../Removal-AI/AI_server/video')
  output_folder = "../Removal-AI/AI_server/video/"
  video2.filename = video2.filename[:-4] + ".mp4"
  output_path = os.path.join(output_folder, video2.filename)
  tomp4(output_folder[:-1])
  os.makedirs(output_folder, exist_ok=True)
  contents = await video2.read()
  output_path = os.path.join(output_folder, video2.filename)
  with open(output_path, "wb") as f:
    f.write(contents)

  video_url = output_folder + video2.filename

  lang, timeline = pro_tetrancess_text(video_url)
  # timeline = remo(timeline)
  if lang == 'eng':
    timeline = translate(timeline)

  save_result_to_file(addsub(timeline, video_url))
  return "Translated SUCCESS"

@app.post("/upload") # 클라이언트 입장 post
async def upload_video(video1: UploadFile = File(...)):
  with open("../Removal-AI/AI_server/location.txt", "w") as file:
    file.write("")
  delete.delete_all_files('../Removal-AI/AI_server/video/output')
  delete.delete_all_files('../Removal-AI/AI_server/video/outvid')
  delete.delete_all_mp4_files('../Removal-AI/AI_server/video')
  output_folder = "../Removal-AI/AI_server/video/"
  video1.filename = video1.filename[:-4] + ".mp4"
  output_path = os.path.join(output_folder, video1.filename)
  tomp4(output_folder[:-1])
  os.makedirs(output_folder, exist_ok=True)
  contents = await video1.read()

  with open(output_path, "wb") as f:
    f.write(contents)

  video_url = output_folder + video1.filename

  lang, timeline = pro_tetrancess_text(video_url)
  # timeline = remo(timeline)
  # if lang == 'eng':
  #   timeline = translate(timeline)

  save_result_to_file(addsub(timeline, video_url))
  return "SUCCESS"

@app.get("/download") # 클라이언트 입장 get
async def get_video():
  try:
    with open("../Removal-AI/AI_server/location.txt", "r") as file:
      video_path = file.read().strip()
    return FileResponse(video_path)
  except Exception:
    raise HTTPException(status_code=500, detail="SERVER ERROR")

if __name__ == "__main__":
  # 서버 실행
  import uvicorn
  uvicorn.run(app="main:app", host="YOUR_IP", port=5632, reload=True) # 포트 변경 가능