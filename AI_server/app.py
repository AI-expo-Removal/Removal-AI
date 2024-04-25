from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Video  # assuming the model is defined in models.py

app = FastAPI()

# 데이터베이스 연결 설정
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://3.36.127.22:3306/removal"  # 데이터베이스 URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/videos/{video_id}")
async def get_video_url(video_id: int):
    db = SessionLocal()
    video = db.query(Video).filter(Video.id == video_id).first()
    if video is None:
        return {"error": "Video not found"}
    return {"url": video.url}