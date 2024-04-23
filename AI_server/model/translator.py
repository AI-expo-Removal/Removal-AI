from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def translate_to_korean(english_sentences):
    model_dir = "/Users/kdw/Documents/Projects/AI EXPO/Removal-AI/AI_server/results"
    max_token_length = 128

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    model.cpu()

    inputs = tokenizer(english_sentences, return_tensors="pt", padding=True, truncation=True, max_length=max_token_length)

    korean_outputs = model.generate(
        **inputs,
        max_length=max_token_length,
        num_beams=5,
    )

    translated_sentences = tokenizer.batch_decode(korean_outputs, skip_special_tokens=True)
    
    return translated_sentences