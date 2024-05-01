import moviepy.editor as mp
from datetime import datetime
import ffmpeg
import sys
import os
import pysrt
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def seconds_to_srt_time_format(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d},000"

def generate_srt_file(subtitles):
    file_path = "./video/output.srt"
    with open(file_path, 'w+', encoding='utf-8') as srt_file:
        count = 1
        for subtitle in subtitles:
            start_time = int(subtitle['timestamp'][0] * 1000)
            end_time = int(subtitle['timestamp'][1] * 1000)
            text = subtitle['text']

            srt_file.write(f"{count}\n")
            srt_file.write(f"{seconds_to_srt_time_format(start_time)} --> {seconds_to_srt_time_format(end_time)}\n")
            srt_file.write(f"{text}\n\n")
            count += 1

def time_to_seconds(time_obj):
  return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

def create_subtitle_clips(subtitles, font='../AI_server/font/HY견고딕.TTF', color='white', debug = False):
  subtitle_clips = []

  for subtitle in subtitles:
    start_time = time_to_seconds(subtitle.start)
    end_time = time_to_seconds(subtitle.end)
    duration = end_time - start_time

    video_width = 1920
    video_height = 1080

    text_clip = TextClip(subtitle.text, fontsize = 60, font=font, color=color, bg_color = 'black',size=(video_width * 4/5, None), method='caption').set_start(start_time).set_duration(duration)
    subtitle_x_position = 'center'
    subtitle_y_position = video_height * (4 / 5)

    text_position = (subtitle_x_position, subtitle_y_position)                    
    subtitle_clips.append(text_clip.set_position(text_position))

  return subtitle_clips

def addsub(tl, url):
  generate_srt_file(tl)
  srtfilename = "../AI_server/video/output.srt"
  mp4filename = url[:-4] + ".mp4"
  print(mp4filename)
  li = mp4filename.split("/")
  output_video_file = './video/outvid/' + li[-1][:-4] + '_subtitled'+".mp4"

  video = VideoFileClip(mp4filename)
  subtitles = pysrt.open(srtfilename)

  subtitle_clips = create_subtitle_clips(subtitles)

  final_video = CompositeVideoClip([video] + subtitle_clips)

  final_video.write_videofile(output_video_file, codec='libx264', audio_codec='aac')

  return output_video_file # 로컬에 저장된 영상 경로 반환

print(addsub([{'timestamp': (0.0, 2.0), 'text': ' 시트라도 되냐?'}, {'timestamp': (2.0, 4.5), 'text': ' 야 재민아, 발음 좀만 제대로 해봐'}, {'timestamp': (4.5, 6.0), 'text': ' 알죠. 그래, 뜨거워요'}, {'timestamp': (6.0, 8.0), 'text': ' 안녕하세요. 갑자기 뭐?'}, {'timestamp': (8.0, 9.0), 'text': ' 지금 뭘 듣고 있죠?'}, {'timestamp': (9.0, 11.0), 'text': ' 저희 음료이네라는 보고 있습니다'}, {'timestamp': (11.0, 13.0), 'text': ' 음료이네라는 어디가 쳐들어온'}, {'timestamp': (13.0, 14.0), 'text': ' 그거죠?'}, {'timestamp': (14.0, 15.0), 'text': ' 나 빨리 쇼그러워'}, {'timestamp': (15.0, 17.0), 'text': ' 일부는 아니라 왜예요? 왜?'}, {'timestamp': (17.0, 19.0), 'text': ' 빨리 빨리 빨리 빨리'}, {'timestamp': (19.0, 20.0), 'text': ' 저한테'}, {'timestamp': (20.0, 22.0), 'text': ' 야 나 계속도 좀 갑자기'}, {'timestamp': (22.0, 25.0), 'text': ' 나 퀘스에 형, 너 계속도 삼아주기 해. 계속. 나 캣스 해. 네.'}, {'timestamp': (25.0, 26.0), 'text': ' 잘.'}, {'timestamp': (26.0, 27.0), 'text': ' 네.'}, {'timestamp': (27.0, 28.0), 'text': ' 저는 잘 모르겠습니다.'}, {'timestamp': (28.0, 29.0), 'text': ' 네.'}, {'timestamp': (29.0, 30.0), 'text': ' 저기 도완입니다.'}, {'timestamp': (30.0, 31.0), 'text': ' 네, 알겠습니다.'}], "./video/uploadedvid/jamin.mp4"))