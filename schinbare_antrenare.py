import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
import numpy as np
import os

SEED = 42
DEVICE = 'cpu'
TRAINING_DIR = r''
LOGS_DIR = r''
OUTPUT_DIR = r''
REPETITION_PENALTY=1.2


class ConversationDataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_length=128):
        self.dataframe = dataframe
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        item = self.dataframe.iloc[idx]
        input_text = item['questions']
        target_text = item['responses']

        input_ids = self.tokenizer.encode(input_text, max_length=self.max_length, truncation=True, padding="max_length")
        target_ids = self.tokenizer.encode(target_text, max_length=self.max_length, truncation=True, padding="max_length")

        target_ids = [(tid if tid != self.tokenizer.pad_token_id else -100) for tid in target_ids]

        return {
            'input_ids': torch.tensor(input_ids),
            'labels': torch.tensor(target_ids)
        }

def set_seed(seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True

def train_on_subset(csv_path, model, tokenizer):
    df = pd.read_csv(csv_path, encoding='latin1')
    df = df[['questions', 'responses']]

    train_size = 0.8
    train_df = df.sample(frac=train_size, random_state=SEED)
    val_df = df.drop(train_df.index).reset_index(drop=True)
    train_df = train_df.reset_index(drop=True)

    train_dataset = ConversationDataset(train_df, tokenizer)
    val_dataset = ConversationDataset(val_df, tokenizer)

    training_args = Seq2SeqTrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=True,
        evaluation_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=4,
        weight_decay=0.01,
        logging_dir=LOGS_DIR,
        logging_first_step=True,
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="loss",
        greater_is_better=False,
        predict_with_generate=True
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer
    )

    trainer.train()
    eval_results = trainer.evaluate(eval_dataset=val_dataset)
    print("Evaluation results:", eval_results)
    
    return model


from transformers import AutoTokenizer ,AutoModelForSeq2SeqLM

def trainingProcess():
    set_seed(SEED)
    model=r""
    tokenizer=r""
    model=AutoModelForSeq2SeqLM.from_pretrained(model)
    tokenizer=AutoTokenizer.from_pretrained(tokenizer)

    subset_files = [os.path.join(TRAINING_DIR, f) for f in os.listdir(TRAINING_DIR) if f.endswith('.csv')]

    for csv_path in subset_files:
        print(f"Training on subset: {csv_path}")
        model = train_on_subset(csv_path, model, tokenizer)

    save_path = r''
    model.save_pretrained(save_path)

trainingProcess()
