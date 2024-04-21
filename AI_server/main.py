from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from typing import List
from video2audio import ffmpeg
from model import voice_recognition, translate_T5
import shutil
import os

app = FastAPI()

async def video_to_sound(url):
    return ffmpeg.video_to_audio(url)

async def process_video(video_file: UploadFile) -> str:
    return voice_recognition.recognition()

# async def trans():
#    translate_T5. # 미완성

# 클라이언트에게 처리된 동영상을 제공하는 엔드포인트
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
    uvicorn.run(app, host="127.0.0.1", port=8000)