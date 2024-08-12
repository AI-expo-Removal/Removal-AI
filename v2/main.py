from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from model import getaudio, voice_recognition, writesrt, addsubtitle, translate
import os
import shutil

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_script(video_title, video_path, language):
  try:
    # 동영상을 입력받아, 오디오를 추출한 후, 대본을 만들어 srt 파일로 저장
    if not os.path.exists("./v2/audio"):
      os.mkdir("./v2/audio")
    getaudio.getaud(video_title, video_path)
    # recognition_wav2vec2.recognition(video_title, language)
    text, text_with_timestamp = voice_recognition.recognition(video_title, language)

    # 동영상 언어가 영어일 경우 script를 한글로 번역
    if language == 'englsih':
      text_with_timestamp = translate.translate_to_korean(text_with_timestamp)

    if not os.path.exists("./v2/srt_script"):
      os.mkdir("./v2/srt_script")
    writesrt.create_srt_from_list(text_with_timestamp)

    print("srt 파일 생성 완료.")
    return "srt processing Success!!"
  except Exception as e:
    print(f"Error: {str(e)}")
    return "Error occurred"

@app.get("/basic-subtitle") # 업로드 받은 동영상에 자막을 추가 후 다운로드 요청을 기다림.
async def basic(video_path: str): # 동영상 -> srt파일 대본 -> 영상에 자막으로 삽입
  try:
    language = "korean"
    video_title = os.path.splitext(os.path.basename(video_path))[0]
    # 파일 형식 없는 이름 / video.title은 파일 형식 있는 이름
    get_script(video_title, video_path, language) # 자막 추가 함수

    # 저장된 동영상에 자막 추가
    addsubtitle.addsub(video_title, video_path)

    processed_path = "./v2/processed/" + video_title + ".mp4"

    if os.path.exists(processed_path):
      return FileResponse(str(video_path))
    else:
      raise HTTPException(status_code=404, detail="video file not found.")
  except Exception as e:
    print(str(e))
    raise HTTPException(status_code=500, detail=str(e))

@app.get("/translate")
async def basic(video_path: str): # 동영상 -> srt파일 대본 -> 번역 -> 영상에 자막으로 삽입
  try:
    language = "english"
    video_title = os.path.splitext(os.path.basename(video_path))[0]
    # 파일 형식 없는 이름 / video.title은 파일 형식 있는 이름
    get_script(video_title, video_path, language)

    # 저장된 동영상에 자막추가
    addsubtitle.addsub(video_title, video_path)

    processed_path = "./v2/processed/" + video_title + ".mp4"
    if os.path.exists(processed_path):
      return HTTPException(status_code=200, content={"message": "subtitle processed successfully"})
    else:
      HTTPException(status_code=404, detail="video file not found.")
  except Exception as e: 
    raise HTTPException(status_code=500, detail=str(e))

@app.get("/remove")
async def basic(video_path: str): # 동영상 -> srt파일 대본 -> 욕설 제거 -> 영상에 자막으로 삽입
  try:
    language = "korean"
    video_title = os.path.splitext(os.path.basename(video_path))[0]
    # 파일 형식 없는 이름 / video.title은 파일 형식 있는 이름
    get_script(video_title, video_path, language)

    processed_path = "./v2/processed/" + video_title + ".mp4"
    if os.path.exists(processed_path):
      return HTTPException(status_code=200, content={"message": "subtitle processed successfully"})
    else:
      HTTPException(status_code=404, detail="video file not found.")
  except Exception as e: 
    raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload") # 동영상 업로드
async def download_file(video_file: UploadFile = File(...)):
  try:
    # 영상을 저장할 경로 설정
    video_folder = "./v2/video"
    if not os.path.exists(video_folder):
      os.mkdir(video_folder)
    
    file_path = os.path.join(video_folder + '/' + video_file.filename)

    # 전달 받은 동영상 저장
    with open(file_path, "wb") as b:
      shutil.copyfileobj(video_file.file, b)
    
    print("-------title-------")
    print(f"{video_file.filename}")
    print("-------file_path-------")
    print(f"{file_path}")
    return JSONResponse(status_code = 200, content={"message": "video uploaded successfully", "title": video_file.filename, "file_path": file_path})
  except Exception as e:
    raise HTTPException(status_code = 500, detail=str(e))
  finally:
    video_file.file.close()

# @app.get("/video/{video_name}")
# async def get_video(video_name: str):
#   video_directory = "./v2/processed"

#   # 실제 파일 경로
#   video_path = video_directory / f"{video_name}.mp4"

#   # 파일이 존재하는지 확인
#   if not video_path.exists():
#     raise HTTPException(status_code=404, detail="Video not found")

#   # 파일이 존재하면 파일을 클라이언트에게 반환
#   return FileResponse(str(video_path))

if __name__ == "__main__": # 서버 실행
  import uvicorn
  uvicorn.run(app="main:app", host="YOUR_IP", port=5632, reload=True)


# 저장된 영상 가져와서 오디오 데이터 따로 저장
# 한글을 전달
# whisper 사용해서 대화 텍스트 뽑기
# 뽑힌 텍스트를 가지고 초단위로 연결하여 다른 txt 파일로 저장
# 그 텍스트에 알맞게 영상에 자막 삽입

# 오디오 데이터 저장
# 한글을 전달
# 텍스트 뽑고
# 다른 txt 파일로 저장
# 욕설 검열
# 자막으로 삽입

# 오디오 데이터 저장
# 영어를 전달
# whisper 사용해서 영어 텍스트 뽑기
# 뽑힌 텍스트를 가지고 초단위로 연결하여 다른 txt 파일로 저장
# 변한 텍스트에 알맞게 자막 삽입
