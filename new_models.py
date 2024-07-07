
from transformers import AutoTokenizer ,AutoModelForSeq2SeqLM


tokenizer=r""
model_path=r''


model=AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer=AutoTokenizer.from_pretrained(tokenizer)


def generate_response(model, tokenizer, input_text,stage=None, intent=None, repetition_penalty=1.9, max_length=128):
    conversation = " ".join(" ") + " " + input_text

    inputs = tokenizer(conversation, return_tensors='pt')
    input_ids = inputs['input_ids'].to(model.device)
    outputs = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        repetition_penalty=repetition_penalty,
        num_beams=5,
        early_stopping=True
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

def generate_response(model, tokenizer, query, stage=None, intent=None):
    if stage and intent:
        input_text = f"{stage} {intent} {query}"
    else:
        input_text = query
    
    inputs = tokenizer(input_text, return_tensors="pt").to('cpu')
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


#response = generate_response(model, tokenizer, prompt, last_stage, global_category)

def generate_response1(model, tokenizer, input_text,stage=None, intent=None, repetition_penalty=1.9, max_length=128):
    conversation = " ".join(" ") + " " + input_text

    inputs = tokenizer(conversation, return_tensors='pt')
    input_ids = inputs['input_ids'].to(model.device)
    outputs = model.generate(
        input_ids=input_ids,
        max_length=max_length,
        repetition_penalty=repetition_penalty,
        num_beams=5,
        early_stopping=True
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response

conversation_history = []

while True:
    user_input = input("User: ")
    response = generate_response1(model, tokenizer, user_input)
    print("Bot:", response)

