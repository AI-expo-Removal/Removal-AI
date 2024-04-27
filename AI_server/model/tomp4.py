import os
import subprocess

def convert_to_mp4(input_folder):
  files = os.listdir(input_folder)
  output_folder = "../Removal-AI/AI_server/video/"

  os.makedirs(output_folder, exist_ok=True)
  for file in files:
    filename, ext = os.path.splitext(file)

    if ext.lower() in ['.mov', '.wav']:
      input_file = os.path.join(input_folder, file)
      output_file = os.path.join(output_folder, f"{filename}.mp4")
      subprocess.run(['ffmpeg', '-i', input_file, '-c:v', 'libx264', '-c:a', 'aac', output_file])