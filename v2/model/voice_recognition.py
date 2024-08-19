import torch
from pydub import AudioSegment
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from transformers import WhisperForConditionalGeneration, WhisperProcessor, AutomaticSpeechRecognitionPipeline, pipeline

def seconds_to_hhmmss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

def load_audio(file_path):
    try:
        # 오디오 파일 로드
        audio = AudioSegment.from_file(file_path)
        return audio
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return None

def recognition(title, language):
  try:
    audiourl = "./v2/audio/" + title + ".mp3"

    # device = "cuda" if torch.cuda.is_available() else "cpu" # in nvidia gpu
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f'"{device}로 인공지능 처리를 시작합니다."')
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-medium" # 사용할 whisper 사이즈

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
      model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
      "automatic-speech-recognition",
      model=model,
      tokenizer=processor.tokenizer,
      feature_extractor=processor.feature_extractor,
      max_new_tokens=128,
      chunk_length_s=30,
      batch_size=16,
      return_timestamps=True,
      torch_dtype=torch_dtype,
      device=device,
    )

    result = pipe(audiourl, generate_kwargs={"language": language})
    print(result)
    return result["text"], result["chunks"]
  except Exception as e:
    print(f"ERROR: {str(e)}")
    return ""