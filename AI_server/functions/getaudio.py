from moviepy.editor import VideoFileClip, AudioFileClip

def getaud(videourl):
  mp4_file = videourl
  mp3_file = "./video/output/sond.mp3"

  video_clip = VideoFileClip(mp4_file)

  audio_clip = video_clip.audio

  audio_clip.write_audiofile(mp3_file)

  audio_clip.close()
  video_clip.close()
