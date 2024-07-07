import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

def list_documents(directory):
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    return files

def choose_document(documents):
    choice = int(input("Enter the number of the document you want to learn about (or -1 to exit): ")) - 1
    print()
    if 0 <= choice < len(documents):
        return documents[choice]
    else:
        if choice == -1:
            return None
        return None

def clean_and_split_text(tokenizer, text, max_length):
    cleaned_text = text.strip().replace("\n", " ").replace("\t", " ").replace("  ", " ")
    tokens = tokenizer.encode(cleaned_text, add_special_tokens=False)
    chunks = []
    for i in range(0, len(tokens), max_length):
        chunk = tokens[i:i + max_length]
        if len(chunk) > max_length:
            chunk = chunk[:max_length]
        chunks.append(chunk)
    text_chunks = [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]
    
    return text_chunks

def summarize_document(filepath, model_dir, max_length=512):
    print()
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    chunks = clean_and_split_text(tokenizer, content, max_length)
    print(f"Number of chunks: {len(chunks)}")

    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)
        print(f"Length of current chunk (in tokens): {len(tokenizer.encode(chunk, add_special_tokens=False))}")
        summaries.append(summary[0]['summary_text'])

    combined_summary = ' '.join(summaries)
    return combined_summary

def summarize():
    print()
    directory = r''
    model_dir = r''
    
    while True:
        documents = list_documents(directory)
        print()
        if not documents:
            print("No documents found.")
            return
        print("Available documents:")
        for idx, doc in enumerate(documents):
            print(f"{idx + 1}. {doc}")
        
        chosen_document = choose_document(documents)
        if chosen_document is None:
            print()
            print("Exiting the summarization tool.")
            break
        
        filepath = os.path.join(directory, chosen_document)
        summary = summarize_document(filepath, model_dir)
        print("Summary:")
        print()
        print(summary)
        print()
