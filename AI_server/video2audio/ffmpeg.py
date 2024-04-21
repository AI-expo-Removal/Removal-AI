import ffmpeg
import subprocess
import os

def video_to_audio(url):
  if os.path.exists("YOUR_DIR/sund.mp3"):
    os.remove("YOUR_DIR/sund.mp3")
  outp = "YOUR_DIR/sund.mp3"
  subprocess.run(["ffmpeg", "-i", url, outp])