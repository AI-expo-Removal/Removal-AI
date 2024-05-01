# https://metamath1.github.io/blog/posts/gentle-t5-trans/gentle_t5_trans.html

import os
from datasets import load_dataset, Dataset, load_metric
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
import torch
import multiprocessing
import evaluate

en_ko = load_dataset("bongsoo/news_talk_en_ko")
en_ko.set_format(type="pandas")
df = en_ko["train"][:]

example = list(df.columns)
example_df = pd.DataFrame({col: [value] for col, value in zip(('en', 'ko'), example)})
df.columns = ('en', 'ko')
en_ko_df = pd.concat([example_df, df],).reset_index(drop=True)

dataset = Dataset.from_pandas(en_ko_df)

num_train = 1210000
num_valid = 80000
num_test = 10000

if os.path.exists("train.tsv"):
  print("------------------------------")
  print("train.tsv 존재")
  print("------------------------------")
else:
  en_ko_df_train = en_ko_df.iloc[:num_train]
  en_ko_df_train.to_csv("train.tsv", sep='\t', index=False)

if os.path.exists("valid.tsv"):
  print("------------------------------")
  print("valid.tsv 존재")
  print("------------------------------")
else:
  en_ko_df_valid = en_ko_df.iloc[num_train:num_train + num_valid]
  en_ko_df_valid.to_csv("valid.tsv", sep='\t', index=False)

if os.path.exists("test.tsv"):
  print("------------------------------")
  print("test.tsv 존재")
  print("------------------------------")
else:
  en_ko_df_test = en_ko_df.iloc[-num_test:]
  en_ko_df_test.to_csv("test.tsv", sep='\t', index=False)

datafiles = {"train": "train.tsv", "valid": "valid.tsv", "test": "test.tsv"}
dataset = load_dataset("csv", data_files=datafiles, delimiter="\t")

# device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = torch.device("mps") if torch.backends.mps.is_available() else torch.device("cpu") # in mac silicon chip gpu
print("------------------------------")
print(device)
print("------------------------------")
model_ckpt = "KETI-AIR/ke-t5-base"
max_token_length = 64

tokenizer = AutoTokenizer.from_pretrained("KETI-AIR/ke-t5-base")
dataset['train'][10]['en'], dataset['train'][10]['ko']
tokenized_sample_en = tokenizer(dataset['train'][10]['en'], 
                                max_length=max_token_length, 
                                padding=True, truncation=True)

tokenized_sample_ko = tokenizer(dataset['train'][10]['ko'],
                                max_length=max_token_length,
                                padding=True, truncation=True)

def convert_examples_to_features(examples):
    model_inputs = tokenizer(examples['en'],
                            text_target=examples['ko'], 
                            max_length=max_token_length, truncation=True)
    
    return model_inputs

NUM_CPU = multiprocessing.cpu_count()

tokenized_datasets = dataset.map(convert_examples_to_features, 
                                batched=True, 
                                remove_columns=dataset["train"].column_names,
                                num_proc=NUM_CPU) 

model = AutoModelForSeq2SeqLM.from_pretrained(model_ckpt).to(device)

encoder_inputs = tokenizer(
    ['Studies have been shown that owning a dog is good for you'],
    return_tensors="pt"
)['input_ids'].to(device)

decoder_targets = tokenizer(
    ['개를 키우는 것이 건강에 좋다는 연구 결과가 있습니다.'],
    return_tensors="pt"
)['input_ids'].to(device)

decoder_inputs = model._shift_right(decoder_targets)

outputs = model(input_ids=encoder_inputs, 
                decoder_input_ids=decoder_inputs, 
                labels=decoder_targets)

data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
batch = data_collator(
    [tokenized_datasets["train"][i] for i in range(1, 3)]
)

metric = evaluate.load("sacrebleu")
predictions = [
    "저는 딥러닝을 좋아해요.",
    "딥러닝 프레임워크가 잘 개발되었기 때문에 요즘은 누군가의 도움 없이 기계번역 시스템을 구축할 수 있다."
]

references = [
    ["저는 딥러닝을 좋아해요.", "나는 딥러닝을 사랑해요."],
    ["요즘은 딥러닝 프레임워크가 잘 발달되어 있기 때문에 누구의 도움 없이도 기계 번역 시스템을 구축할 수 있습니다.",
     "최근에는 딥러닝 프레임워크가 잘 개발되어 있기 때문에 다른 사람의 도움 없이도 기계 번역 시스템을 개발할 수 있습니다."]
]
print(metric.compute(predictions=predictions, references=references))

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    
    if isinstance(preds, tuple):
        preds = preds[0]
    
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    
    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    
    # Some simple post-processing
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [[label.strip()] for label in decoded_labels]
    
    result = metric.compute(predictions=decoded_preds, references=decoded_labels)
    result = {"bleu": result["score"]}
    
    return result

training_args = Seq2SeqTrainingArguments(
    output_dir="chkpt",
    learning_rate=0.0005,
    weight_decay=0.01,
    per_device_train_batch_size=64,
    per_device_eval_batch_size=128,
    num_train_epochs=1,
    save_steps=500,
    save_total_limit=2,
    evaluation_strategy="epoch",
    logging_strategy="no",
    predict_with_generate=True,
    fp16=False,
    gradient_accumulation_steps=2,
    report_to="none"
)

trainer = Seq2SeqTrainer(
    model,
    training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["valid"],
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

trainer.train()
trainer.save_model("./results")

model_dir = "./results"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

model.cpu();

input_text = [
    "Because deep learning frameworks are well developed, in these days, machine translation system can be built without anyone's help.",
    "This system was made by using HuggingFace's T5 model for a one day"
]

inputs = tokenizer(input_text, return_tensors="pt", 
                   padding=True, max_length=max_token_length)

koreans = model.generate(
    **inputs,
    max_length=max_token_length,
    num_beams=5,
)

test_dataloader = DataLoader(
    tokenized_datasets["test"], batch_size=32, collate_fn=data_collator
)

test_dataloader_iter = iter(test_dataloader)
test_batch = next(test_dataloader_iter)
test_input = { key: test_batch[key] for key in ('input_ids', 'attention_mask') }

koreans = model.generate(
    **test_input,
    max_length=max_token_length,
    num_beams=5,
)

labels =  np.where(test_batch.labels != -100, test_batch.labels, tokenizer.pad_token_id)
eng_sents = tokenizer.batch_decode(test_batch.input_ids, skip_special_tokens=True)[10:20]
references = tokenizer.batch_decode(labels, skip_special_tokens=True)[10:20]
preds = tokenizer.batch_decode( koreans, skip_special_tokens=True )[10:20]

for s in zip(eng_sents, references, preds):
    print('English   :', s[0])
    print('Reference :', s[1])
    print('Translated:', s[2])
    print('\n')