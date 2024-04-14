# https://metamath1.github.io/blog/posts/gentle-t5-trans/gentle_t5_trans.html

from datasets import load_dataset, Dataset, load_metric
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
from transformers import Seq2SeqTrainingArguments, Seq2SeqTrainer
import pandas as pd
import numpy as np
import torch
import multiprocessing

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

en_ko_df_train = en_ko_df.iloc[:num_train]
en_ko_df_valid = en_ko_df.iloc[num_train:num_train + num_valid]
en_ko_df_test = en_ko_df.iloc[-num_test:]
en_ko_df_train.to_csv("train.tsv", sep='\t', index=False)
en_ko_df_valid.to_csv("valid.tsv", sep='\t', index=False)
en_ko_df_test.to_csv("test.tsv", sep='\t', index=False)

datafiles = {"train": "train.tsv", "valid": "valid.tsv", "test": "test.tsv"}
dataset = load_dataset("csv", data_files=datafiles, delimiter="\t")

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_ckpt = "KETI-AIR/ke-t5-base"
max_token_length = 64

