import moviepy.editor as mp
from moviepy.video.VideoClip import ColorClip
from datetime import datetime
import ffmpeg
from moviepy.video.tools.subtitles import SubtitlesClip
import pysrt
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

def generate_srt_from_list(subtitles):
  file_path = "./video/output.srt"
  with open(file_path, 'w', encoding='utf-8') as f:
    count = 1
    for subtitle in subtitles:
      start_time = subtitle['timestamp'][0]
      end_time = subtitle['timestamp'][1]
      text = subtitle['text']
      f.write(str(count) + '\n')
      f.write("{:02d}:{:02d}:{:02d},{:03d}".format(int(start_time // 3600), int((start_time % 3600) // 60), int(start_time % 60), int((start_time % 1) * 1000)) + ' --> ' +
              "{:02d}:{:02d}:{:02d},{:03d}".format(int(end_time // 3600), int((end_time % 3600) // 60), int(end_time % 60), int((end_time % 1) * 1000)) + '\n')
      f.write(text + '\n\n')
      count += 1

def time_to_seconds(time_obj):
  return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

def add_subtitles(video_path, subtitles_path, output_path):
    # 동영상 클립 로드
    video = VideoFileClip(video_path)
    
    # 자막 클립 생성
    def generator(txt):
        """자막 스타일을 여기서 지정합니다."""
        return TextClip(txt, font='NanumGothic', fontsize=30, color='white')

    subtitles = SubtitlesClip(subtitles_path, generator)

    # 동영상 높이의 4/5 위치 계산
    video_height = video.size[1]
    subtitles_position = ('center', video_height * 6 / 7 - 30 / 2)  # 40은 자막의 폰트 크기입니다.

    # 자막을 동영상에 오버레이하고, 계산된 위치에 배치
    final = CompositeVideoClip([video, subtitles.set_position(subtitles_position)])
    
    # 결과 동영상 파일 저장
    final.write_videofile(output_path, codec='libx264', fps=24)

    # # 자막 파일 로드
    # subtitles = []
    # with open(subtitles_path, 'r', encoding='utf-8') as f:
    #     lines = f.readlines()
    #     for i in range(0, len(lines), 4):
    #         start_time, end_time = lines[i+1].strip().replace(',', '.').split(' --> ')
    #         text = lines[i+2].strip()
    #         subtitles.append(((start_time, end_time), text))
    # # 동영상 파일 로드
    # video = VideoFileClip(video_path)
    
    # # 자막 삽입
    # subtitle_clips = []
    # for subtitle_info in subtitles:
    #     start_time, end_time = subtitle_info[0]
    #     text = subtitle_info[1]
    #     start_time_sec = video.parse_time(start_time)
    #     end_time_sec = video.parse_time(end_time)
    #     duration = end_time_sec - start_time_sec
    #     text_clip = TextClip(text, fontsize=font_size, font=font, color=font_color, stroke_color=stroke_color, stroke_width=stroke_width)
    #     text_clip = text_clip.set_position(('center', 'bottom')).set_start(start_time_sec).set_duration(duration)
    #     subtitle_clips.append(text_clip)
    
    # video_with_subtitles = CompositeVideoClip([video, *subtitle_clips])
    
    # # 결과 동영상 저장
    # video_with_subtitles.write_videofile(output_path, codec="libx264", temp_audiofile="temp-audio.m4a", remove_temp=True, audio_codec="aac")


def addsub(tl, url):
  generate_srt_from_list(tl)
  srtfilename = "../AI_server/video/output.srt"
  mp4filename = url[:-4] + ".mp4"
  li = mp4filename.split("/")
  output_video_file = './video/outvid/' + li[-1][:-4] + '_subtitled'+".mp4"
  add_subtitles(url, srtfilename, output_video_file)

  return output_video_file # 로컬에 저장된 영상 경로 반환
