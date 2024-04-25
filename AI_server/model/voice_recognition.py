import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import os
# accelerate 설치 필요

def seconds_to_hhmmss(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

def recognition():
  audiourl = "../Removal-AI/AI_server/video/output/sund.mp3"

  # device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu") # in mac silicon chip gpu
  device = "cuda" if torch.cuda.is_available() else "cpu" # in nvidia gpu
  # print(device)
  torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

  model_id = "openai/whisper-base" # 사용할 whisper 사이즈

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

  result = pipe(audiourl)
  return result["text"], result["chunks"]