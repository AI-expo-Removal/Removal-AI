from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from botocore.exceptions import NoCredentialsError, ClientError
from io import BytesIO
from functions import voice_recognition, translator, detect, addsubtitle, getaudio
from remove_bad import r_b
from pydantic import BaseModel
from dotenv import load_dotenv
from urllib.parse import quote
import requests
import boto3
import os
import requests

load_dotenv()

app = FastAPI(openapi_url='/openapi.json')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 오리진을 허용하려면 "*" 사용, 필요에 따라 특정 도메인을 지정할 수 있음
    allow_credentials=False,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*" 사용
    allow_headers=["*"],  # 모든 헤더를 허용하려면 "*" 사용
)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME
)

s3 = boto3.client('s3')

class UploadRequest(BaseModel):
  s3_url: str

def upload_to_s3(file_name, bucket, object_name=None):
    # S3 클라이언트 생성
    s3_client = boto3.client('s3')
    
    # S3 객체 이름이 제공되지 않은 경우 파일 이름 사용
    if object_name is None:
        object_name = file_name.split("/")[-1]

    # 파일 업로드 시도
    try:
        # 파일 업로드
        s3_client.upload_file(file_name, bucket, object_name)
        return f"https://{bucket}.s3.{AWS_REGION_NAME}.amazonaws.com/{object_name}"
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(e)

def upload_file_to_s3(file, bucket_name):
  try:
    s3_client.upload_fileobj(
      file.file,
      bucket_name,
      file.filename
    )
  except Exception:
    raise HTTPException(status_code=500, detail="Error uploading file to S3")
  return f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"

def download_s3(s3_url, local_dir): # s3에서 동영상 다운로드
  file_name = s3_url.split('/')[-1]
  local_path = f"{local_dir}/{file_name}"

  response = requests.get(s3_url)
    
  if response.status_code == 200:
    with open(local_path, 'wb') as f:
      f.write(response.content)
    print(f'"s3 영상 다운로드에 성공했습니다!"')
    return local_path
  else:
    print(f'"s3 영상 다운로드에 실패했습니다 : {response.status_code}"')
    return None

def pro_tetrancess_text(url, lage): # mp4 영상 경로
  getaudio.getaud(url) # mp3 추출
  tup = voice_recognition.recognition(lage) # whisper 모델 전달 후, 전체 텍스트와 timeline에 대한 텍스트 반환 (전체 텍스트는 버림)

  return tup

def remo(timeline): # 입력받은 timeline에 대한 텍스트를 욕설 제거
  return r_b.removal(timeline)

def translate(text): # 번역한 타임라인 반환
  return translator.translate_to_korean(text)

def addsub(tl, mp4url): # 타임라인에 따라 영상 경로에 있는 동영상에 자막 추가
  return addsubtitle.addsub(tl, mp4url)

def giveurl(video_path):
  # try:
  #   text_path = "./location.txt"
  #   with open(text_path, "r", encoding="utf-8") as txt:
  #     file = txt.read()

  #   filename = "removal-recongnized.mp4"

  #   file_content = file.encode('utf-8')

  #   s3_client.upload_fileobj(
  #     BytesIO(file_content),
  #     S3_BUCKET_NAME,
  #     filename
  #   )

  #   file_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{file.filename}"
  #   return {"message": "s3 url이 정상적으로 반환되었습니다.", "file_url": file_url}

  # except NoCredentialsError:
  #   raise HTTPException(status_code=500, detail="AWS credentials not available.")
  # except Exception as e:
  #   raise HTTPException(status_code=500, detail="An error occurred during s3 processing.")
  try:
    # 동영상 파일 업로드
    video_name = video_path.split('/')[-1]
    s3.upload_file(video_path, S3_BUCKET_NAME, video_name)

    # 업로드된 동영상의 S3 URL 반환
    s3_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION_NAME}.amazonaws.com/{video_name}"
    return {"url": s3_url}
  except NoCredentialsError:
    raise HTTPException(status_code=500, detail="AWS 자격 증명을 찾을 수 없습니다.")
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/gets3")
async def upload_video(file: UploadFile = File(...)):
  file_url = upload_file_to_s3(file, S3_BUCKET_NAME)
  return {"url": file_url}

@app.post("/removal") # 욕설 삭제 자막 API
async def download_file(s3_url: str):
  try:
    save_video_path = "./video/uploadedvid"
    video_path = download_s3(s3_url, save_video_path)
    lage = "korean"
    timeline = pro_tetrancess_text(video_path, lage)
    timeline = remo(timeline)
    file_path = addsub(timeline, video_path)

    return giveurl(file_path)
  except Exception:
    raise HTTPException(status_code=500, detail = str(Exception))
  # try:
  #   save_path = "video/"
  #   response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
  #   file_content = response["Body"].read()

  #   local_file_path = os.path.join(save_path, file_key.split("/")[-1])
  #   with open(local_file_path, "wb") as f:
  #     f.write(file_content)
  #   video_url = local_file_path


  #   lang, timeline = pro_tetrancess_text(video_url)
  #   timeline = remo(timeline)

  #   save_result_to_file(addsub(timeline, video_url))
  #   return giveurl()
  # except Exception as e:
  #   raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload") # 그냥 자막 추가 API
async def download_file(ul: UploadRequest):
  try:
    save_video_path = "./video/uploadedvid"
    video_path = download_s3(ul.s3_url, save_video_path)
    lage = "korean"
    timeline = pro_tetrancess_text(video_path, lage)
    file_path = addsub(timeline, video_path)
    file_url = upload_to_s3(file_path, S3_BUCKET_NAME)

    return file_url
  except Exception:
    raise HTTPException(status_code=500, detail = str(Exception))
  # try:
  #   save_path = "video/"
  #   response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
  #   file_content = response["Body"].read()

  #   local_file_path = os.path.join(save_path, file_key.split("/")[-1])
  #   with open(local_file_path, "wb") as f:
  #     f.write(file_content)
  #   video_url = local_file_path

  #   lang, timeline = pro_tetrancess_text(video_url)

  #   save_result_to_file(addsub(timeline, video_url))
  #   return giveurl()
  # except Exception as e:
  #   raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate") # 영어 to 한국어 번역 자막 API
async def download_file(s3_url: str):
  try:
    save_video_path = "./video/uploadedvid"
    video_path = download_s3(s3_url, save_video_path)
    lage = "english"
    timeline = pro_tetrancess_text(video_path, lage)
    timeline = translate(timeline)
    file_path = addsub(timeline, video_path)

    return giveurl(file_path)
  except Exception:
    raise HTTPException(status_code=500, detail = str(Exception))
  # try:
  #   save_path = "video/"
  #   response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=file_key)
  #   file_content = response["Body"].read()

  #   local_file_path = os.path.join(save_path, file_key.split("/")[-1])
  #   with open(local_file_path, "wb") as f:
  #     f.write(file_content)
  #   video_url = local_file_path

  #   lang, timeline = pro_tetrancess_text(video_url)
  #   if lang == 'eng':
  #     timeline = translate(timeline)

  #   save_result_to_file(addsub(timeline, video_url))
  #   return giveurl()
  # except Exception as e:
  #   raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
  # 서버 실행
  import uvicorn
  uvicorn.run(app="main:app", host="172.16.23.66", port=5732, reload=True) # 포트 변경 가능