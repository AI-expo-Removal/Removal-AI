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





dat_location = open(os.path.join("YOUR_DIR", "test.wav"), "rb")
vd = dat_location.read()
print(vd)
sam = vd
i_f = processor(sam["array"], sampling_rate = sample["sampling_rate"], return_tensors = "pt").input_features

pre_ids = model.generate(i_f)
transc = processor.batch_decode(pre_ids, skip_special_tokens=False)
print(transc)