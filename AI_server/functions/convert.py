import ffmpeg

def convert_to_mp4(input_file):
    ffmpeg.input(input_file).output(input_file[:-4] + ".mp4").run()
