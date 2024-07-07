                                                #   nu am GPU destul de bun . procesul de antrenare va fi facut pe cpu

import time
import torch
import transformers
import numpy as np
import pandas as pd
from tqdm import tqdm
from torch import cuda
from torch.utils.data import Dataset, DataLoader
from transformers import BlenderbotSmallTokenizer, BlenderbotSmallForConditionalGeneration, \
TrainingArguments, Trainer
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from langchain.chains import LLMChain
from transformers import AutoTokenizer ,pipeline,AutoModelForSeq2SeqLM
from transformers import Trainer

# training


print()
print(" The training process will be done on CPU .")
print()
device = 'cuda' if cuda.is_available() else 'cpu'
df=pd.read_csv(r'', encoding='latin1')
print(df.head())


class customDataset(Dataset):
    #clasa care determina tot ce are legatura cu setul de date pe care antrenezi
    def __init__(self,tokenizer,dataframe,dialogue_len,summary_len):
        self.tokenizer=tokenizer
        self.data=dataframe # data in sine 
        self.dialogue_len=dialogue_len # lungimea dialogului din date
        self.summary_len=summary_len # lungimea sumarizarii
        self.summary=self.data['responses']
 # folosesti mai tz coloana de sumarizare din date 
        self.dialogue=self.data['questions'] # ii atribui instantei curente coloana de dataframe de  dialog
    
    def __len__(self):
        return len(self.summary) # iti trb pt ca folosesti clasa mare de la torch --> lungimea liniilor de sumarry
    
    def __getitem__(self, index):
        # pytorch --> ia un sample din setul de date la index-ul specificat
        dialogue=str(self.dialogue[index])
        dialogue=' '.join(dialogue.split())
        
        summary=str(self.summary[index])
        summary=' '.join(summary.split())
        # pt tokenizare , da join la cuvinte din dialog si din summary
        # source, target --> tokenizate , padding pana la lungimea maxima si ii returneaza ca pytorch tensors (folositi pt encodare ,decodare si pt parameri model)
        source = self.tokenizer.batch_encode_plus([dialogue], max_length = self.dialogue_len, padding = 'max_length',\
                                                  return_tensors = 'pt', truncation = True)
        target = self.tokenizer.batch_encode_plus([summary], max_length = self.summary_len, padding = 'max_length',\
                                                  return_tensors = 'pt', truncation = True)
        
        source_ids = source['input_ids'].squeeze().to(dtype = torch.long)   # inputul tokenizat
        source_mask = source['attention_mask'].squeeze().to(dtype = torch.long) # attention mask = 1 unde e data , 0 udne e padding
        target_ids = target['input_ids'].squeeze().to(dtype = torch.long)       # pentru target-ul (sumarry) tokenizat




        # modelul trebuie sa prezica tokene bazate pe tokene input . compari ce a generat cu actualele secvente de tokene
        # 
        y_ids = target_ids[:-1].contiguous() # make y_ids contiguous 
        #   in training modelul primeste input_ids si va prezice ce e in y_ids
        lm_labels = target_ids[1:].clone().detach() # make fast copy
        #   outputul ideal de la model . outptul adevarat va fi comparat cu lm_labels
        #   din cate am inteles , modelul produce o distributie de probabilitate a vocabularului pt fiecare pozitite in secventa de target
        #   distrubutia asta e comparata cu lm_labels si diferenta e pierderea (loss)
        lm_labels[target_ids[1:] == tokenizer.pad_token_id] = -100  # poate self.tokenizer.pad_token_id ??
        #  nu folosete tokenele cu padding ( -100 e ignore_index in pytorch --> modelul nu e penalizat pt predictii la padding)
        
        # returneaza un dictionar dupa formatul necesar pt Trainer din transformers 
        return {
            'input_ids': source_ids, 
            'attention_mask': source_mask, 
            'decoder_input_ids': y_ids, # target-ul
            'labels': lm_labels
        }



model_id = "facebook/blenderbot_small-90M"
model_path=""

TRAIN_BATCH_SIZE = 8
VALID_BATCH_SIZE = 2 
TRAIN_EPOCHS = 5 # normal 10      
VAL_EPOCHS = 1 
LEARNING_RATE = 1e-4    # folosita uzual  0.0001
SEED = 42               # seed random pt repetare generat de torch 
MAX_LEN = 256
SUMMARY_LEN = 64

# generare SEED
torch.manual_seed(SEED) 
np.random.seed(SEED) 
torch.backends.cudnn.deterministic = True
print("SEED generat ...")
print()
tokenizer=BlenderbotSmallTokenizer.from_pretrained(r"")
#tokenizer=BlenderbotSmallTokenizer.from_pretrained(model_path)
df = df[['questions','responses']]
#print(df.head())
#df.summary = 'summarize: ' + df.summary 
#print(df.summary)

train_size = 0.8        # 80% training 20% validare
train_dataset = df.sample(frac=train_size,random_state = SEED)  # ia 80% din valori , folosesti alt SEED de fiecare data ca sa ia alte valori
val_dataset = df.drop(train_dataset.index).reset_index(drop = True) # datasetul de validare , generat prin scoterea setului de date de antrenare din tot setul de date
train_dataset = train_dataset.reset_index(drop = True) # curata datele si seteaza un nou index 1 --> 818 care nu deranjeaza procesul de antrenare
# nr de valori 
print(type(train_dataset))
print(train_dataset.head())

print("FULL Dataset: {}".format(df.shape))
print("---"*20)
print("TRAIN Dataset: {}".format(train_dataset.shape))
print("---"*20)
print("TEST Dataset: {}".format(val_dataset.shape))
print("---"*20)

# pregatim seturile de date

training_set = customDataset( tokenizer,train_dataset, MAX_LEN, SUMMARY_LEN)
val_set = customDataset( tokenizer,val_dataset, MAX_LEN, SUMMARY_LEN)
# (self,tokenizer,dataframe,dialogue_len,summary_len):
print()
print("Seturi de date pregatite...")
print()

# parametri : shuffle - true pentru amestecare la antrenare , false pentru validare . num_workers e pentru folosirea a mai multe CPU cores dar nu am 
train_params = {
    'batch_size': TRAIN_BATCH_SIZE,
    'shuffle': True,
    'num_workers': 0
    }

val_params = {
    'batch_size': VALID_BATCH_SIZE,
    'shuffle': False,
    'num_workers': 0
    }

# creem un dataloader de la pytorch cu parametrii de mai sus , pentru iterare

training_loader = DataLoader(training_set, **train_params)
val_loader = DataLoader(val_set, **val_params)

model=BlenderbotSmallForConditionalGeneration.from_pretrained(model_path)
model = model.to(device)


# o clasa de optimizator Adam folosind parametrii modelului --> ajusteaza rata de invatare in functie de istoric ,normalizeaza rata de invatare , 
optimizer = torch.optim.Adam(params =  model.parameters(), lr = LEARNING_RATE)

args = TrainingArguments(output_dir=r"",
                         seed=42,
                         num_train_epochs=10,
                         per_device_train_batch_size=8,  
                         # max batch size without OOM exception, because of the large max token length
                         per_device_eval_batch_size=8,
                         logging_steps=2500,
                         save_steps=0,
                        )

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=training_set,
    eval_dataset=val_set,
)
print()
print("Antrenam modelul...")
print()


trainer.train()





def validate(epoch, tokenizer, model, device, loader):
    model.eval()
    # pune modelul in modul de evaluare --> schimba niste chestii
    predictions = []
    actuals = []
    texts = []
    with torch.no_grad(): # dezactiveaza  gradient computation, deci nu mai updateaza parametrii modelului ( in directia in care minimizeaza pierderea)
        for _, data in tqdm(enumerate(loader, 0)):
            # tqdm = progress bar
            # itereaza pentru fiecare batch . datele din fiecre baatch sunt puse in data . folosim _ (conventie) pt ca nu avem nevoie de batch-ul in sine
            # ii pune un index pentru fiecare batch generat de DataLoader (pytorch) 
            y = data['decoder_input_ids'].to(device, dtype = torch.long) # input pt decoder
            ids = data['input_ids'].to(device, dtype = torch.long)      # input folosit pentru generare
            mask = data['attention_mask'].to(device, dtype = torch.long)

            generated_ids = model.generate(
                input_ids = ids,
                attention_mask = mask, 
                max_length = 100, 
                num_beams = 2,
                repetition_penalty = 2.5, 
                length_penalty = 1.0, 
                early_stopping = True
                )
            preds = [tokenizer.decode(g, skip_special_tokens = True, clean_up_tokenization_spaces = True)\
                     for g in generated_ids]
            target = [tokenizer.decode(t, skip_special_tokens = True, clean_up_tokenization_spaces = True)\
                      for t in y]
            text = [tokenizer.decode(i, skip_special_tokens = True, clean_up_tokenization_spaces = True)\
                      for i in ids]
            if _%2500==0:
                print(f'Completed {_}')# progres la fiecare 2500 iteratii

            predictions.extend(preds)
            actuals.extend(target)
            texts.extend(text)
    return predictions, actuals, texts

print()
print("Salvam modelul...")
print()

trainer.save_model(r"")

# data frame cu rezultatele validarii 
print()
print("Incepem validarea...")
print()

all_results = []
start_time = time.time()
for epoch in range(VAL_EPOCHS):
    predictions, actuals, text = validate(epoch, tokenizer, model, device, val_loader)
    epoch_results = pd.DataFrame({'Generated Text': predictions, 'Actual Text': actuals, 'Text': text})
    all_results.append(epoch_results)
    
print("Validation took " + str(time.time() - start_time) + " seconds")
final_df = pd.concat(all_results, axis=0, ignore_index=True)
final_df.to_csv(r'D:\EVA PROJECT\EVA_VENV\EVA\_datasets\incercare_antrenare\model_nou4_antrenat_bancar\validare.csv')
print(final_df)

