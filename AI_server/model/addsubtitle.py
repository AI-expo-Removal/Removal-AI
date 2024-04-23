import moviepy.editor as mp
import os

def addsubtitle(url, timeline):
  video = mp.VideoFileClip(url)
  for i in timeline:
    starttime = i['timestamp'][0]
    endtime = i['timestamp'][1]
    subtitle = mp.TextClip(i['text'], fontsize=34, color='black')
    duration = endtime - starttime
    subtitle = subtitle.set_position(('center', 'bottom')).set_duration(duration)
    video_with_subtitle = mp.CompositeVideoClip([video, subtitle])
  if os.path.exists("../video/outvid/subtitlevid.mp4"):
    os.remove("../video/outvid/subtitlevid.mp4")
  video_with_subtitle.write_videofile("../video/outvid/subtitlevid.mp4")

addsubtitle("/Users/kdw/Documents/Projects/AI EXPO/Removal-AI/AI_server/video/20240412_230315.mp4", )