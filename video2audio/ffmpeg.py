import ffmpeg
import subprocess
import os

url = "/Volumes/KDW_X31/Projects/Removal/Datasets/6gijun.mp4" # 나중에 서버에서 받은 url을 사용해야함.

if os.path.exists("/Volumes/KDW_X31/Projects/Removal/Datasets/outputs/testnew.mp3"):
  os.remove("/Volumes/KDW_X31/Projects/Removal/Datasets/outputs/testnew.mp3")
outp = f"/Volumes/KDW_X31/Projects/Removal/Datasets/outputs/testnew.mp3" # DB에 POST해야함.

subprocess.run(["ffmpeg", "-i", url, outp])