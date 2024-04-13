import ffmpeg
import subprocess
import os

url = "YOUR_DIR/20240412_230315.mp4" # 나중에 서버에서 받은 url을 사용해야함.

if os.path.exists("YOUR_DIR/testnew.wav"):
  os.remove("YOUR_DIR/testnew.wav")
outp = f"YOUR_DIR/testnew.wav" # DB에 POST해야함.

subprocess.run(["ffmpeg", "-i", url, outp])