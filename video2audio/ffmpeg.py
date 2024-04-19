import ffmpeg
import subprocess
import os

url = "YOUR_FILE_LOCATION" # 나중에 서버에서 받은 url을 사용해야함.

if os.path.exists("YOUR_DIR/testnew.mp3"):
  os.remove("YOUR_DIR/testnew.mp3")
outp = f"YOUR_DIR/testnew.mp3" # DB에 POST해야함.

subprocess.run(["ffmpeg", "-i", url, outp])