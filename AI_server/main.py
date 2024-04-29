from fastapi import FastAPI, File, HTTPException
from botocore.exceptions import NoCredentialsError
from io import BytesIO
from model import voice_recognition, translator, detect, addsubtitle, getaudio
from remove_bad import r_b
from dotenv import load_dotenv
import requests
import boto3
import os

load_dotenv()

app = FastAPI()

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
S3_BUCKET_NAME = os.environ.get("S3_BuCKET_NAME")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

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
  return addsubtitle.create_subtitle_clips(tl, mp4url)

@app.post("/removal")
async def download_file(file_key: str):
  try:
    save_path = "video/"
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
    file_content = response["Body"].read()

    local_file_path = os.path.join(save_path, file_key.split("/")[-1])
    with open(local_file_path, "wb") as f:
      f.write(file_content)
    video_url = local_file_path

    lang, timeline = pro_tetrancess_text(video_url)
    timeline = remo(timeline)

    save_result_to_file(addsub(timeline, video_url))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def download_file(file_key: str):
  try:
    save_path = "video/"
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
    file_content = response["Body"].read()

    local_file_path = os.path.join(save_path, file_key.split("/")[-1])
    with open(local_file_path, "wb") as f:
      f.write(file_content)
    video_url = local_file_path

    lang, timeline = pro_tetrancess_text(video_url)
    if lang == 'eng':
      timeline = translate(timeline)

    save_result_to_file(addsub(timeline, video_url))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
  
@app.post("/upload")
async def download_file(file_key: str):
  try:
    save_path = "video/"
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
    file_content = response["Body"].read()

    local_file_path = os.path.join(save_path, file_key.split("/")[-1])
    with open(local_file_path, "wb") as f:
      f.write(file_content)
    video_url = local_file_path

    lang, timeline = pro_tetrancess_text(video_url)

    save_result_to_file(addsub(timeline, video_url))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/download")
async def upload_video():
    try:
        file = "video/outvid/"
        file_content = await file.read()

        s3_client.upload_fileobj(
            BytesIO(file_content),
            S3_BUCKET_NAME,
            file.filename
        )

        file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{file.filename}"
        return {"message": "s3 url이 정상적으로 반환되었습니다.", "file_url": file_url}

    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
  # 서버 실행
  import uvicorn
  uvicorn.run(app="main:app", host="192.168.1.51", port=5632, reload=True) # 포트 변경 가능