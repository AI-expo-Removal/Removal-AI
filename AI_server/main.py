from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from typing import List
import shutil
import os

app = FastAPI()

async def video_to_sound():

async def process_video(video_file: UploadFile) -> str:
    # 여기에 동영상 처리 로직을 구현하세요.
    # 예를 들어, 동영상을 저장하고 처리한 후 새로운 파일 경로를 반환할 수 있습니다.
    # 여기에서는 단순히 업로드된 파일 이름을 그대로 반환합니다.
    return video_file.filename

# 클라이언트에게 처리된 동영상을 제공하는 엔드포인트
@app.get("/video/{video_name}")
async def get_processed_video(video_name: str):
    # 여기에서는 단순히 파일이 존재하는지 확인하고 반환합니다.
    # 여러분이 원하는 추가 로직을 구현할 수 있습니다.
    video_path = os.path.join("processed_videos", video_name)
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    else:
        return {"error": "Video not found"}

if __name__ == "__main__":
    # 서버 실행
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)