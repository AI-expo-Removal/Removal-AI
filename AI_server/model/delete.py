import os

def delete_all_files(directory):
    try:
        # 디렉터리 안의 모든 파일 목록 가져오기
        files = os.listdir(directory)
        
        # 디렉터리 안의 모든 파일에 대해 반복
        for file in files:
            # 파일의 절대 경로 생성
            file_path = os.path.join(directory, file)
            
            # 파일 삭제
            os.remove(file_path)
            print(f"{file} 삭제됨")
    except Exception as e:
        print(f"에러 발생: {e}")

def delete_all_mp4_files(directory):
    try:
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if file.lower().endswith('.mp4'):
                os.remove(file_path)
                print(f"{file} 삭제됨")
    except Exception as e:
        print(f"에러 발생: {e}")