from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Video
from database import engineconn, SessionLocal, DB_URL
import httpx
import requests

app = FastAPI()

base_url = "http://3.36.127.22:8080"

backend_url = "http://your-backend-server-url"

def get_userid_from_token(token):
    # 토큰을 백엔드 서버에 전송하여 userid를 가져오는 요청
    response = requests.post(f"{backend_url}/verify_token", json={"token": token})
    if response.status_code == 200:
        return response.json()["userid"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Token verification failed")

# userid를 사용하여 videoid 목록을 가져오는 함수
def get_videoids_for_userid(userid):
    # userid를 백엔드 서버에 전송하여 videoid 목록을 가져오는 요청
    response = requests.get(f"{backend_url}/user/{userid}/videos")
    if response.status_code == 200:
        return response.json()["videoids"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to get videoids for user")

# videoid를 사용하여 videourl을 가져오는 함수
def get_videourl_for_videoid(videoid):
    # videoid를 백엔드 서버에 전송하여 videourl을 가져오는 요청
    response = requests.get(f"{backend_url}/video/{videoid}/url")
    if response.status_code == 200:
        return response.json()["videourl"]
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to get videourl for videoid")

# FastAPI 엔드포인트
@app.get("/videourl")
async def get_videourl(token: str):
    # 토큰을 사용하여 userid 가져오기
    userid = get_userid_from_token(token)
    
    # userid를 사용하여 videoid 목록 가져오기
    videoids = get_videoids_for_userid(userid)
    
    # videoid 목록 중 첫 번째 videoid를 사용하여 videourl 가져오기 (예시로 간단하게 하기 위해)
    first_videoid = videoids[0]
    videourl = get_videourl_for_videoid(first_videoid)
    
    return {"videourl": videourl}


@app.post("")

@app.get("")
async def request_token(baseurl):
    response = await request_token(baseurl)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return token
    else:
        print("토큰 요청 실패:", response.text)