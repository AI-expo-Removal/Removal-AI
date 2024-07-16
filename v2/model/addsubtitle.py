# import moviepy.editor as mp
# from datetime import datetime
# import ffmpeg
# import sys
# import os
# import pysrt
# from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

# def time_to_seconds(time_obj):
#   return time_obj.hours * 3600 + time_obj.minutes * 60 + time_obj.seconds + time_obj.milliseconds / 1000

# def create_subtitle_clips(subtitles, font='../Removal-AI/AI_server/font/HY견고딕.TTF', color='white', debug = False):
#   subtitle_clips = []

#   for subtitle in subtitles:
#     start_time = time_to_seconds(subtitle.start)
#     end_time = time_to_seconds(subtitle.end)
#     duration = end_time - start_time

#     video_width = 1920
#     video_height = 1080

#     text_clip = TextClip(subtitle.text, fontsize = 60, font=font, color=color, bg_color = 'black',size=(video_width * 4/5, None), method='caption').set_start(start_time).set_duration(duration)
#     subtitle_x_position = 'center'
#     subtitle_y_position = video_height * (4 / 5)

#     text_position = (subtitle_x_position, subtitle_y_position)                    
#     subtitle_clips.append(text_clip.set_position(text_position))

#   return subtitle_clips

# def addsub(video_title, video_path):
#   srtfilename = "../Removal-AI/AI_server/video/output.srt"

#   begin, end= mp4filename.split(".mp4")
#   output_video_file = begin[:30] + 'outvid/'+ begin[30:] +'_subtitled'+".mp4"

#   video = VideoFileClip(mp4filename)
#   subtitles = pysrt.open(srtfilename)

#   subtitle_clips = create_subtitle_clips(subtitles)

#   final_video = CompositeVideoClip([video] + subtitle_clips)

#   final_video.write_videofile(output_video_file, codec='utf-8', audio_codec='aac')

#   return output_video_file # 로컬에 저장된 영상 경로 반환



# test
import subprocess

def addsub(video_title, video_path):
    output_video = "./v2/processed/" + video_title + "_subtitled.mp4"
    subtitle_file = "./v2/srt_script/temp.srt"
    # ffmpeg 명령어 생성
    cmd = ['ffmpeg', '-i', video_path, '-vf', f'subtitles={subtitle_file}', '-c:a', 'copy', output_video]
    
    # subprocess를 사용하여 명령어 실행
    subprocess.run(cmd, check=True)
