import os
from moviepy.editor import VideoFileClip

def getaud(video_name, video_path):
  try:
    # 동영상 파일명에서 확장자를 제외한 부분 추출
    output_dir = "./v2/audio"

    # 동영상 파일 로드
    video_clip = VideoFileClip(video_path) # 여기에 어떤 형식으로 경로를 작성해야할까요???
    
    # 오디오 추출
    audio_clip = video_clip.audio
    
    # mp3 파일 경로 설정
    output_path = os.path.join(output_dir, f"{video_name}.mp3")
    
    # mp3 파일로 저장
    audio_clip.write_audiofile(output_path)
    
    # 필요 시 원본 파일 해제
    video_clip.close()
    
    print(f"오디오가 {output_path}에 성공적으로 추출되었습니다.")
  except Exception as e:
    print(f"오디오 추출 중 오류가 발생하였습니다: {str(e)}")