from fastapi import FastAPI, File, HTTPException
from botocore.exceptions import NoCredentialsError
from io import BytesIO
from model import voice_recognition, translator, detect, addsubtitle, getaudio
from remove_bad import r_b
import requests
import boto3
import os

app = FastAPI()

AWS_ACCESS_KEY_ID = "YOUR_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY = "YOUR_SECRET_ACCESS_KEY"
AWS_REGION_NAME = "YOUR_REGION_NAME"
S3_BUCKET_NAME = "YOUR_BUCKET_NAME"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

def save_result_to_file(result):
  file_path = "../Removal-AI/AI/location.txt"
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
    timeline = remo(timeline)
    if lang == 'eng':
      timeline = translate(timeline)

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
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
