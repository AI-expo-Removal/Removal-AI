from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

def translate_to_korean(english_sentences):
    model_dir = "./results"
    max_token_length = 256

    n = 0
    for i in english_sentences:
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
        model.cpu()
        
        inputs = tokenizer(i['text'], return_tensors="pt", padding=True, truncation=True, max_length=max_token_length)

        korean_outputs = model.generate(
            **inputs,
            max_length=max_token_length,
            num_beams=5,
            )
        
        translated_sentences = tokenizer.batch_decode(korean_outputs, skip_special_tokens=True)
        english_sentences[n]['text'] = translated_sentences[0]
        n += 1

    return english_sentences

