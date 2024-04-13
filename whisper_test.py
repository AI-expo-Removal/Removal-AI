# # large-v3
# import torch
# import librosa
# import soundfile as sf
# from scipy.io import wavfile
# from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
# from datasets import load_dataset

# device = "cuda:0" if torch.cuda.is_available() else "cpu"
# torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# model_id = "openai/whisper-large-v3"

# model = AutoModelForSpeechSeq2Seq.from_pretrained(
#     model_id, torch_dtype=torch_dtype
# )
# model.to(device)

# processor = AutoProcessor.from_pretrained(model_id)

# pipe = pipeline(
#     "automatic-speech-recognition",
#     model=model,
#     tokenizer=processor.tokenizer,
#     feature_extractor=processor.feature_extractor,
#     max_new_tokens=128,
#     chunk_length_s=30,
#     batch_size=16,
#     return_timestamps=True,
#     torch_dtype=torch_dtype,
#     device=device,
# )

# # file_lo = 'content/test.wav'
# # dat = wavfile.read(file_lo)
# # print(dat)
# audio_file_path = '/Volumes/KDW_X31/Projects/Removal/Datasets/test.wav'  # 수정 필요한 오디오 파일 경로

# # 오디오 파일을 직접 로드하여 파이프라인에 전달하여 텍스트로 변환
# audio, sr = librosa.load(audio_file_path, sr=None)
# text = pipe(audio, language="ko-KR")
# print(text)

# dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
# sample = dataset[0]["audio"]

# result = pipe(sample, language="en-US")
# print(result["text"])






import os

# tiny
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language="ko", task="transcribe")

# load dummy dataset and read audio files
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
sample = ds[0]["audio"]
input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features 

#dsa = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean")
#print(dsa)

# generate token ids
predicted_ids = model.generate(input_features)
# decode token ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)

print(transcription)

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription)





dat_location = open(os.path.join("/Volumes/KDW_X31/Projects/Removal/Datasets", "test.wav"), "rb")
vd = dat_location.read()
print(vd)
sam = vd
i_f = processor(sam["array"], sampling_rate = sample["sampling_rate"], return_tensors = "pt").input_features

pre_ids = model.generate(i_f)
transc = processor.batch_decode(pre_ids, skip_special_tokens=False)
print(transc)