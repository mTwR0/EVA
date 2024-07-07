
import json 
from difflib import get_close_matches #try to match best response 

import spacy
nlp = spacy.load("en_core_web_sm")



def load_intents(file_path:str) -> dict:
    with open(file_path,'r') as file:
        data: dict=json.load(file)
    return data

def save_intents (file_path: str , data: dict):
    with open (file_path,'w') as file:
        json.dump(data,file,indent=2)

def load_knowledge_base (file_path:str) -> dict:
    with open(file_path,'r') as file:
        data: dict=json.load(file)
    return data




def save_knowledge_base (file_path: str , data: dict):
    with open (file_path,'w') as file:
        json.dump(data,file,indent=2)



def find_best_match(user_question:str  ,  questions:list[str]  )->str|None:
    matches:list=get_close_matches(user_question,questions,n=1,cutoff=0.6)
#                                                         top 1 answer , accuracy
    return matches[0] if matches else None



# ca sa vezi ce tag sa returneze raspunsul trb sa afli intentia utilizator--> greeting/goodbye si faci functie care ia asta ca parametru
def get_answer_for_question(question: str, knowledge_base: dict, intent: str) -> str | None:
    if intent not in knowledge_base:
        knowledge_base[intent] = []  # Create the intent as an empty list

    for q in knowledge_base[intent]:
        if q["prompt"] == question:
            return q["answer"]



        



def get_intent(user_input, intents):
    
    user_input = user_input.lower()
    doc = nlp(user_input)
    tokens = [token.text.lower() for token in doc]

    for intent, keywords in intents.items():
        for keyword in keywords:
            keyword_tokens = keyword.split()  # Split multi-word keywords into tokens
            if all(token in tokens for token in keyword_tokens):
                return intent
    return None


def add_new_intent(intents, intent_name, keywords):
    if intent_name not in intents:
        intents[intent_name] = keywords  # Create a new intent with keywords

def get_words(user_input):

    user_input=user_input.lower()
    doc=nlp(user_input)
    tokens=[token.text.lower() for token in doc]
    return tokens

#print(get_words("hello , my name is radu")) #--> ['hello', ',', 'my', 'name', 'is', 'radu']


