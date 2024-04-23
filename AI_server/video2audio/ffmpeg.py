import ffmpeg
import subprocess
import os

def video_to_audio(url):
  if os.path.exists("../video/output/sund.mp3"):
    os.remove("../video/output/sund.mp3")
  outp = "../video/output/sund.mp3"
  subprocess.run(["ffmpeg", "-i", url, outp])

video_to_audio("/Users/kdw/Documents/Projects/AI EXPO/Removal-AI/AI_server/video/Becane.mp4")