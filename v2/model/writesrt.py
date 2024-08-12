import os

def format_srt_time(seconds):
  milliseconds = int((seconds - int(seconds)) * 1000)
  hours = int(seconds // 3600)
  minutes = int((seconds % 3600) // 60)
  seconds = int(seconds % 60)
  return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def create_srt_from_list(subtitles):
  srt_file = "./v2/srt_script/temp.srt"

  if os.path.exists(srt_file):
    print(f"Warning: File '{srt_file}' already exists and will be overwritten.")

  with open(srt_file, 'w', encoding='utf-8') as f:
    for idx, subtitle in enumerate(subtitles, start=1):
      start_time = subtitle['timestamp'][0]
      end_time = subtitle['timestamp'][1]
      text = subtitle['text']

      # Convert seconds to SRT format time (hours:minutes:seconds,milliseconds)
      start_srt = format_srt_time(start_time)
      end_srt = format_srt_time(end_time)

      # Write subtitle index
      f.write(f"{idx}\n")

      # Write time format --> (e.g., 00:00:00,000 --> 00:00:02,000)
      f.write(f"{start_srt} --> {end_srt}\n")

      # Write subtitle text
      f.write(f"{text}\n\n")