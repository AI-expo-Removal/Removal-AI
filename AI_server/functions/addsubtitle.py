import moviepy.editor as mp
from datetime import datetime
import ffmpeg
from moviepy.video.tools.subtitles import SubtitlesClip
import pysrt
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

def add_subtitles(video_path, subtitles_path, output_path, font="Arial", font_size=24, font_color='white', stroke_color='black', stroke_width=5):
    # 자막 파일 로드
    subtitles = SubtitlesClip(subtitles_path)
    
    # 동영상 파일 로드
    video = VideoFileClip(video_path)
    
    # 자막 삽입
    subtitle_clips = []
    for subtitle in subtitles:
        text_clip = TextClip(subtitle[0], fontsize=font_size, font=font, color=font_color, stroke_color=stroke_color, stroke_width=stroke_width)
        subtitle_clips.append(text_clip.set_position(('center', 'bottom')).set_duration(subtitle.duration))
    
    video_with_subtitles = CompositeVideoClip([video.set_duration(subtitles.duration), *subtitle_clips])
    
    # 결과 동영상 저장
    video_with_subtitles.write_videofile(output_path, codec="libx264", temp_audiofile="temp-audio.m4a", remove_temp=True, audio_codec="aac")

def addsub(tl, url):
  generate_srt_from_list(tl)
  srtfilename = "../AI_server/video/output.srt"
  mp4filename = url[:-4] + ".mp4"
  print(mp4filename)
  li = mp4filename.split("/")
  output_video_file = './video/outvid/' + li[-1][:-4] + '_subtitled'+".mp4"

  add_subtitles(url, srtfilename, output_video_file)

  return output_video_file # 로컬에 저장된 영상 경로 반환

# print(addsub([{'timestamp': (0.0, 4.0), 'text': ' 꼼꼼 얼어붙은 한강 위로 고양이가 걸어다니입니다.'}, {'timestamp': (4.0, 9.0), 'text': ' 꼼꼼 얼어붙은 고양이가 한강 위로 걸어다니입니다.'}, {'timestamp': (9.0, 13.0), 'text': ' 꼼꼼 얼어붙은 한강 위로 고양이다.'}, {'timestamp': (13.0, 18.0), 'text': ' 꼼꼼 얼어붙은 한강이가 걸어다니입니다.'}, {'timestamp': (18.0, 23.0), 'text': ' 아, 님미나더러 가긴 하여 우리 흉안이는 하나 또 버렁꼼.'}, {'timestamp': (23.0, 26.0), 'text': ' 꼼꼼.'}], "/Users/kdw/Documents/Projects/AI EXPO/Removal-AI/AI_server/video/uploadedvid/ggongcat.mp4"))