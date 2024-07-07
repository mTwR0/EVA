print()
print(" _____ _   _  ___  \n|  ___| | | |/ _ \\ \n| |__ | | | / /_\\ \\\n|  __|| | | |  _  |\n| |___\ \\_/ / | | |\n\\____/ \\___/\\_| |_|")
print()

from gtts import gTTS


def choose_category(user_utt):
    categories_list = []
    for category in user_utt:
        categories_list.append(category)
    print("Available categories:")
    for index, category in enumerate(categories_list, start=1):
        print(f"{index}. {category}")
    while True:
        try:
            choice = int(input("Choose a category (enter the corresponding number): "))
            if 1 <= choice <= len(categories_list):
                chosen_category = categories_list[choice - 1]
                return chosen_category
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def replace_diacritics(text):
    replacements = {
        'Ș': 'S', 'ș': 's',
        'Ț': 'T', 'ț': 't',
        'Ă': 'A', 'ă': 'a',
        'Â': 'A', 'â': 'a',
        'Î': 'I', 'î': 'i'
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text


import json


from difflib import get_close_matches 

def load_json(file_path:str) -> dict:
    with open(file_path,'r') as file:
        data: dict=json.load(file)
    return data

def save_json (file_path: str , data: dict):
    with open (file_path,'w') as file:
        json.dump(data,file,indent=2)

import spacy
nlp = spacy.load("en_core_web_sm")

from difflib import get_close_matches

def new_find_best_match(user_input):
    card_loss_keywords = [
        "loss", "lost", "wallet", "missing","missing.", "misplaced", "can't find",
        "last used", "yesterday", "last transaction", "convenience store",
        "gym", "bar", "bus", "online purchase","look for"
    ]
    update_phone_number_keywords = [
        "phone number",  "new phone", "phone", "number", "old phone", "old number"
    ]
    close_account_keywords = [
        "close", "account", "not using", "inactive", "acount","delete","remove"
    ]
    card_address_modification_keywords = [
        "address", "moved", "wrong address", "billing address",
        "new place", "old address", "adress"
    ]
    update_email_keywords = [
        "email", "old email", "new email", "mail"
    ]

    user_question_lower = user_input.lower()
    
    for word in user_question_lower.split():
        if any(word in keyword_list for keyword_list in [card_loss_keywords, update_phone_number_keywords, close_account_keywords, card_address_modification_keywords, update_email_keywords]):
            if word in card_loss_keywords:
                return "card_loss"
            elif word in update_phone_number_keywords:
                return "update_phone_number"
            elif word in close_account_keywords:
                return "close_account"
            elif word in card_address_modification_keywords:
                return "card_address_modification"
            elif word in update_email_keywords:
                return "update_email"
    return None

def find_best_match(user_question: str, questions: list[str]) -> str|None:
    card_loss_keywords = [
        "loss", "lost", "wallet", "missing", "misplaced", "can't find",
        "last used", "yesterday", "last transaction", "convenience store",
        "gym", "bar", "bus", "online purchase"
    ]
    update_phone_number_keywords = [
        "phone number",  "new phone","phone","number"
    ]
    close_account_keywords = [
        "close", "account", "not using",
        "inactive"
    ]
    card_address_modification_keywords = [
        "address", "moved", "wrong address", "billing address",
        "new place",
        "old address","adress"
    ]
    update_email_keywords = [
        "email", "old email", "new email","mail"
    ]
    
    user_question_lower = user_question.lower()

    for keyword_list in [card_loss_keywords, update_phone_number_keywords, close_account_keywords,
                         card_address_modification_keywords, update_email_keywords]:
        for keyword in keyword_list:
            if keyword in user_question_lower:
                matching_questions = [q for q in questions if keyword in q.lower()]
                if matching_questions:
                    return matching_questions[0]

    matches = get_close_matches(user_question, questions, n=1, cutoff=0.7)
    return matches[0] if matches else None


from datetime import datetime

now = datetime.today()
today_date = now.strftime('%d-%m-%Y_%H-%M')

from voice_generation import generate_audio
from SpeechRecog import parseCommand
import pygame 
import time
from transformers import AutoTokenizer ,AutoModelForSeq2SeqLM
from sistem_bancar import personal_info_check ,update_personal_info,generate_report,delete_user_file

model_id = "facebook/blenderbot_small-90M"
model_path=r'D:\EVA PROJECT\EVA_VENV\EVA\_datasets\incercare_antrenare\modificare csv din nou\subsets\final'
model_path_for_card_loss=r'D:\EVA PROJECT\EVA_VENV\EVA\_datasets\incercare_antrenare\modificare csv din nou\subsets\final_card_loss'
tokenizer=r"D:\EVA PROJECT\EVA_VENV\EVA\hugging_face\blenderbot_small-90M"
model=AutoModelForSeq2SeqLM.from_pretrained(model_path)
tokenizer=AutoTokenizer.from_pretrained(tokenizer)


out=r"D:\EVA PROJECT\EVA\outputs_lore"
EVA_AUDIO_OUTPUT_PATH=r"D:\EVA PROJECT\EVA_VENV\EVA\output.wav"
pygame.init()

responses=[]
questions=[]


def remove_spaces(text):
    cleaned_text = text.replace(" '", "'").replace("' ", "'")
    cleaned_text = cleaned_text.replace(" ,", ",").replace(", ", ",")
    cleaned_text = cleaned_text.replace(" .", ".")
    cleaned_text = cleaned_text.replace(" ?", "?")
    cleaned_text = cleaned_text.replace("  ", "")
    return cleaned_text

from mtranslate import translate as mtranslate_translate

def chat_bot_v2(lang):
    model_path=r'D:\EVA PROJECT\EVA_VENV\EVA\_datasets\incercare_antrenare\modificare csv din nou\subsets\final'
    tokenizer=r"D:\EVA PROJECT\EVA_VENV\EVA\hugging_face\blenderbot_small-90M"
    model=AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer=AutoTokenizer.from_pretrained(tokenizer)
    model_path_for_card_loss=r'D:\EVA PROJECT\EVA_VENV\EVA\_datasets\incercare_antrenare\modificare csv din nou\subsets\final_card_loss'

    user_utt: dict = load_json("user_utterance.json")
    sadpath=0
    best_match = None
    loop_nr=0
    zzz=0
    last_stage="Stage_1"
    if lang=='en':
        print("SYSTEM: If the bot can not help the user within 4 conversation turns , the program will be terminated. ")
    else :
        print("SYSTEM : Dacă robotul nu poate ajuta utilizatorul în 4 ture de conversație, programul va fi încheiat.")
    answered=0

    while True:
        if last_stage=='Stage_3':
            break
        if lang=='en':
            loop_nr+=1
            
            print("SYSTEM: You can choose to quit the program at any time by saying 'quit' . ")
            if loop_nr==1:
                print("SYSTEM: Your following input should describe the problem.  ")
            prompt=parseCommand("en-GB")
            questions.append(prompt)
            user_input=prompt.strip()
            if loop_nr>1 :
                solved=input("SYSTEM: Was the problem solved ? (y/n):")
                if solved=='y':
                    print("EVA: Thank you for using our services. Have a great day!")
                    user_utt[global_category]['Stage_3'].append(user_input)
                    save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json", user_utt)
                    if global_category=='card_loss':
                        report_input=input("SYSTEM : Do you want to generate a report for your missing card? (y/n) : ")
                        if report_input=='y':
                            print("SYSTEM : The system will now confirm your identity.")
                            input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                            if input11 =='y':
                                user_file = personal_info_check(global_category,lang)
                                if user_file:
                                    print("SYSTEM : Generating a report...")
                                    generate_report(user_file)
                                else:
                                    print("Personal info not confirmed.")
                                    sadpath=1   
                                    break

                    break
            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                break
            verificare = None
            okk=0
            for category in user_utt:
                if verificare is not None and okk==1:
                    break
                for stage in user_utt[category]:
                    if verificare is not None and okk==1:
                        break
                    for prompt in user_utt[category][stage]:
                        verificare = new_find_best_match(user_input)
                        if verificare == category:
                            okk=1
                            best_match = prompt
                            global_category = verificare
                            found_category = verificare
                            found_stage = stage
                            last_stage = stage
                            break
                    if verificare is not None and okk==1:
                        break

            if best_match==None:
                found_category=None
                found_stage=None

            if best_match != None:
                        
                print(f"SYSTEM: From the user input , the found category is '{global_category}' . The robot expects conversation about this category .")
            while True:
                if loop_nr==1 and found_stage!='Stage_1' and best_match is not None:
                    found_stage="Stage_1"
                    proper_start=input("EVA: I cannot recognise what you are asking of me . Is this a proper start to a conversation? (y/n): ")
                    if proper_start=='y':
                        print("EVA: Thank you . The introductory prompt will be added to the database.")
                        if found_category==None:                            
                            print("SYSTEM: Please select the category this input should be added to. ")
                            global_category = choose_category(user_utt)
                            print(f"You chose category '{global_category}'.")
                            
                        user_utt[global_category]["Stage_1"].append(user_input)
                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)

                        break
                    bad=1
                    if proper_start=='n':
                        while bad==1:
                            print("EVA: Please describe your problem. I am here to help.")
                            print("SYSTEM: The following exchange should describe the problem.  ")
                            prompt=parseCommand("en-GB")
                            questions.append(prompt)
                            user_input=prompt.strip()
                            for category in user_utt:
                                for stage in user_utt[category]:
                                    best_match = find_best_match(user_input, [utterance for utterance in user_utt[category][stage]])
                                    found_category=category
                                    found_stage=stage
                                    if best_match !=  None:
                                        global_category=found_category
                                        break
                            if found_stage!= 'Stage_1':
                                proper_start=input("EVA: I cannot recognise what you are asking of me . Is this a proper start to a conversation? (y/n): ")
                                if proper_start=='y':
                                    print("EVA: Thank you . The introductory prompt will be added to the database.")
                                    found_stage='Stage_1'
                                    bad=0

                                    if best_match==None:
                                        found_category=None
                                    if found_category==None:
                                        print("SYSTEM: Please select the category this input should be added to. ")
                                        global_category = choose_category(user_utt)
                                        print(f"You chose category '{global_category}'.")
                                        user_utt[global_category]["Stage_1"].append(user_input)
                                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
                                    break
                                else:
                                    bad=1
                            else:
                                bad=0
                                break
                else:
                    break

            if last_stage=='Stage_2':
                print("SYSTEM: In the following exchanges the problem should be resolved.  ")
            if loop_nr==4 and last_stage!='Stage_3' :
                found_stage='Stage_3'
                user_input=user_utt[global_category][found_stage][0]
                print("EVA: I am sorry I could not be of use to you. ")
                sadpath=1

            if found_stage=='Stage_3' and sadpath!=1:
                
                print("SYSTEM: The following exchange should be closing the conversation.  ")
                
            if (global_category=='card_loss' or found_category=='card_loss') and zzz==0:
                zzz=1
                model=AutoModelForSeq2SeqLM.from_pretrained(model_path_for_card_loss)

            response = generate_response(model, tokenizer, prompt, last_stage, global_category)
            answer=remove_spaces(response)

            if answered ==0 and found_stage=='Stage_1' and global_category=='card_address_modification' or global_category=='update_email' or global_category=='update_phone_number':
                answer=answer+' We will need to confirm the ownership of your account before proceeding.'
                generate_audio(answer, EVA_AUDIO_OUTPUT_PATH)
                my_sound = pygame.mixer.Sound(EVA_AUDIO_OUTPUT_PATH)
                my_sound.play()                
                print(f"EVA: {answer}")
                responses.append(answer)
                answered=1
                prompt=parseCommand("en-GB")
                questions.append(prompt)
                user_input=prompt.strip()   
                response = generate_response(model, tokenizer, prompt, last_stage, global_category)
                answer=remove_spaces(response)
                print(f"EVA: {answer}")
                generate_audio(answer, EVA_AUDIO_OUTPUT_PATH)
                my_sound = pygame.mixer.Sound(EVA_AUDIO_OUTPUT_PATH)
                my_sound.play()                
                responses.append(answer)
                print()
                print("SYSTEM : The system will now confirm you identity.")
                input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                print()
                if input11 =='y':
                    user_file = personal_info_check(global_category,lang=lang)
                    if user_file:
                        print("EVA: I will now update your personal info.")
                        update_personal_info(global_category, user_file)
                    else:
                        print("Personal info not confirmed.")
                        sadpath=1   
                        break

                else:
                    break
            if loop_nr>=2 and global_category=='close_account':
                print("SYSTEM : Initiating account closure process...")
                acc_close_input=input("SYSTEM : Do you want to close your account? (y/n) : ")
                if acc_close_input=='y':
                    print("SYSTEM : The system will now confirm your identity.")
                    input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                    if input11 =='y':
                        user_file = personal_info_check(global_category,lang)
                        if user_file:
                            print("SYSTEM : Closing your account...")
                            delete_user_file(user_file)
                            break

            if answered == 0:
                print(f"EVA: {answer}")
                responses.append(answer)
                generate_audio(answer, EVA_AUDIO_OUTPUT_PATH)
                my_sound = pygame.mixer.Sound(EVA_AUDIO_OUTPUT_PATH)
                my_sound.play()                
            if sadpath ==1:
                if global_category=='card_loss':
                    report_input=input("SYSTEM : Do you want to generate a report for your missing card? (y/n) : ")
                    if report_input=='y':
                        print("SYSTEM : The system will now confirm your identity.")
                        input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                        if input11 =='y':
                            user_file = personal_info_check(global_category,lang)
                            if user_file:
                                print("SYSTEM : Generating a report...")
                                generate_report(user_file)
                            else:
                                print("Personal info not confirmed.")
                                sadpath=1  
                                break
                break

            answered=0
            if last_stage=='Stage_1' or last_stage=='Stage_2' and loop_nr<4:
                last_stage='Stage_2' 
            if last_stage=='Stage_2' and loop_nr!=1:
                user_utt[global_category][last_stage].append(user_input)
                save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
        
        else:

            loop_nr+=1
            print("SYSTEM: Poti iesi din program oricand cu: 'quit' . ")
            if loop_nr==1:
                
                print("SYSTEM: Urmatorul tau input ar trebui sa descrie problema.  ")
            prompt=parseCommand("ro-RO")
            questions.append(prompt)
            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                break
            
            prompt = mtranslate_translate(prompt, 'en', 'auto')

            print("Textul tradus in engleza este:", prompt)
            user_input=prompt.strip()
            if loop_nr>1 :
                        
                solved=input("SYSTEM: Problema a fost rezolvata? (y/n):")
                
                if solved=='y':
                    print("EVA: Multumim ca ai folosit serviciile noastre!")
                    user_utt[global_category]['Stage_3'].append(user_input)
                    save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json", user_utt)
                    if global_category=='card_loss':
                        report_input=input("SYSTEM : Vrei sa generezi un raport pentru cardul tau pierdut? (y/n) : ")
                        if report_input=='y':
                            print("SYSTEM : Acum trebuie sa iti confirmi identitatea.")
                            input11=input("SYSTEM : Vrei sa continui ? (y/n) : ")
                            if input11 =='y':
                                user_file = personal_info_check(global_category,lang)
                                if user_file:
                                    print("SYSTEM : Generare raport...")
                                    generate_report(user_file)
                                else:
                                    print("Informatii neconfirmate.")
                                    sadpath=1   
                                    break

                    break

            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                break
            verificare = None
            okk=0
            for category in user_utt:
                if verificare is not None and okk==1:
                    break
                for stage in user_utt[category]:
                    if verificare is not None and okk==1:
                        break
                    for prompt in user_utt[category][stage]:
                        verificare = new_find_best_match(user_input)
                        if verificare == category:
                            okk=1
                            best_match = prompt
                            global_category = verificare
                            found_category = verificare
                            found_stage = stage
                            last_stage = stage
                            break
                    if verificare is not None and okk==1:
                        break
            if best_match==None:
                found_category=None
                found_stage=None

            if best_match != None:
                        
                print(f"SYSTEM: Categoria gasita este '{global_category}' . EVA se asteapta la conversatie despre acest subiect .")
            while True:
                if loop_nr==1 and found_stage!='Stage_1' and best_match is not None:
                    found_stage="Stage_1"
                    proper_start=input("EVA: Nu pot recunoaște ce îmi ceri. Este acesta un început potrivit pentru o conversație? (y/n): ")
                    if proper_start=='y':
                        print("EVA: Mulțumesc . Promptul introductiv va fi adăugat la baza de date.")
                        if found_category==None:
                            print("SYSTEM: Vă rugăm să selectați categoria la care ar trebui adăugată această intrare. ")
                            global_category = choose_category(user_utt)
                            print(f"Ai ales categoria '{global_category}'.")
                        user_utt[global_category]["Stage_1"].append(user_input)
                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
                        break
                    bad=1
                    if proper_start=='n':
                        while bad==1:
                            print("EVA: Te rog descrie problema.")                            
                            print("SYSTEM: Următorul schimb ar trebui să descrie problema.  ")
                            prompt=parseCommand("ro-RO")
                            questions.append(prompt)
                            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                                break
                            prompt = mtranslate_translate(prompt, 'en', 'auto')
                            print("Textul tradus in engleza este:", prompt)
                                        
                            for category in user_utt:
                                for stage in user_utt[category]:
                                    best_match = find_best_match(user_input, [utterance for utterance in user_utt[category][stage]])
                                    found_category=category
                                    found_stage=stage
                                    if best_match !=  None:
                                        global_category=found_category
                                        break
                            if found_stage!= 'Stage_1':
                                proper_start=input("EVA: Nu pot recunoaște ce îmi ceri. Este acesta un început potrivit pentru o conversație? (y/n): ")
                                if proper_start=='y':
                                    print("EVA: Mulțumesc . Promptul introductiv va fi adăugat la baza de date.")
                                    found_stage='Stage_1'
                                    bad=0

                                    if best_match==None:
                                        found_category=None
                                    if found_category==None:
                                        print("SYSTEM: Vă rugăm să selectați categoria la care ar trebui adăugată această intrare. ")
                                        global_category = choose_category(user_utt)
                                        print(f"Ai ales categoria '{global_category}'.")
                                        user_utt[global_category]["Stage_1"].append(user_input)
                                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
                                    break
                                else:
                                    bad=1
                            else:
                                bad=0
                                break

                else:
                    break
            if last_stage=='Stage_2':
                
                print("SYSTEM: În următoarele schimburi problema ar trebui rezolvată.  ")
            if loop_nr==4 and last_stage!='Stage_3' :
                found_stage='Stage_3'
                user_input=user_utt[global_category][found_stage][0]
                print("EVA: Nu am putut sa te ajut . Imi pare rau. ")
                sadpath=1

            if found_stage=='Stage_3' and sadpath!=1:
                
                print("SYSTEM: Următorul schimb ar trebui să închidă conversația.  ")
            

            if (global_category=='card_loss' or found_category=='card_loss') and zzz==0:
                zzz=1
                model=AutoModelForSeq2SeqLM.from_pretrained(model_path_for_card_loss)
            
            response = generate_response(model, tokenizer, prompt, last_stage, global_category)
            answer=remove_spaces(response)

            if answered ==0 and found_stage=='Stage_1' and global_category=='card_address_modification' or global_category=='update_email' or global_category=='update_phone_number':
                answer=answer+' We will need to confirm the ownership of your account before proceeding.'
                answer = mtranslate_translate(answer, 'ro', 'auto')
                print(f"EVA: {answer}")
                responses.append(answer)

                mytext = answer
                language = 'ro'
                myobj = gTTS(text=mytext, lang=language, slow=False)
                myobj.save(EVA_AUDIO_OUTPUT_PATH)
                my_sound = pygame.mixer.Sound(EVA_AUDIO_OUTPUT_PATH)
                my_sound.play()
                print(f"EVA: {mytext}")
                responses.append(mytext)
                while pygame.mixer.get_busy():
                    time.sleep(0.1)
                                
                answered=1

                prompt=parseCommand("ro-RO")
                questions.append(prompt)
                if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                    break
                
                prompt = mtranslate_translate(prompt, 'en', 'auto')

                print("Textul tradus in engleza este:", prompt)
                user_input=prompt.strip()
                response = generate_response(model, tokenizer, prompt, last_stage, global_category)
                answer=remove_spaces(response)
                answer=mtranslate_translate(answer, 'ro', 'auto')

                mytext = answer
                language = 'ro'
                myobj = gTTS(text=mytext, lang=language, slow=False)
                myobj.save(EVA_AUDIO_OUTPUT_PATH)
                my_sound = pygame.mixer.Sound(EVA_AUDIO_OUTPUT_PATH)
                my_sound.play()
                print(f"EVA: {mytext}")
                responses.append(mytext)
                while pygame.mixer.get_busy():
                    time.sleep(0.1)
                                 
                print(f"EVA: {answer}")
                responses.append(answer)
                print()
                print("SYSTEM : Sistemul vă va confirma acum identitatea.")
                input11=input("SYSTEM : Vrei sa continui ? (y/n) : ")
                print()
                if input11 =='y':
                    user_file = personal_info_check(global_category,lang)
                    if user_file:
                        print("EVA: Iti voi schimba informatiile.")
                        update_personal_info(global_category, user_file)
                    else:
                        print("Informatii neconfirmate.")
                        sadpath=1  
                        break

                else:
                    break
            if loop_nr>=2 and global_category=='close_account':
                print("SYSTEM : Inițierea procesului de închidere a contului...")
                acc_close_input=input("SYSTEM : Vrei sa iti inchizi contul? (y/n) : ")
                if acc_close_input=='y':
                    print("SYSTEM : Sistemul vă va confirma acum identitatea.")
                    input11=input("SYSTEM : Vrei sa continui ? (y/n) : ")
                    if input11 =='y':
                        user_file = personal_info_check(global_category,lang)
                        if user_file:
                            print("SYSTEM : Închiderea contului ...")
                            delete_user_file(user_file)
                            break

            if answered == 0:
                answer=mtranslate_translate(answer, 'ro', 'auto')

                mytext = answer
                language = 'ro'
                myobj = gTTS(text=mytext, lang=language, slow=False)
                myobj.save(EVA_AUDIO_OUTPUT_PATH)
                my_sound = pygame.mixer.Sound(EVA_AUDIO_OUTPUT_PATH)
                my_sound.play()
                print(f"EVA: {mytext}")
                responses.append(mytext)
                while pygame.mixer.get_busy():
                    time.sleep(0.1)

                print(f"EVA: {answer}")
                responses.append(answer)
            if sadpath ==1:
                if global_category=='card_loss':
                    report_input=input("SYSTEM : Doriți să generați un raport pentru cardul pierdut? (y/n) : ")
                    if report_input=='y':
                        print("SYSTEM : Sistemul vă va confirma acum identitatea.")
                        input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                        if input11 =='y':
                            user_file = personal_info_check(global_category,lang)
                            if user_file:
                                print("SYSTEM : Generand un raport...")
                                generate_report(user_file)
                            else:
                                print("Personal info not confirmed.")
                                sadpath=1   
                                break
                break

            answered=0
            if last_stage=='Stage_1' or last_stage=='Stage_2' and loop_nr<4:
                last_stage='Stage_2' 
            if last_stage=='Stage_2' and loop_nr!=1:
                user_utt[global_category][last_stage].append(user_input)
                save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
        



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



def chat_bot_text(lang):
    model_path=r'D:\EVA PROJECT\EVA_VENV\EVA\_datasets\incercare_antrenare\modificare csv din nou\subsets\final'
    tokenizer=r"D:\EVA PROJECT\EVA_VENV\EVA\hugging_face\blenderbot_small-90M"
    model=AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer=AutoTokenizer.from_pretrained(tokenizer)
    model_path_for_card_loss=r'D:\EVA PROJECT\EVA_VENV\EVA\_datasets\incercare_antrenare\modificare csv din nou\subsets\final_card_loss'

    user_utt: dict = load_json("user_utterance.json")
    sadpath=0
    best_match = None
    loop_nr=0
    last_stage="Stage_1"
    if lang=='en':
        print("SYSTEM: If the bot can not help the user within 4 conversation turns , the program will be terminated. ")
    else :
        print("SYSTEM : Dacă robotul nu poate ajuta utilizatorul în 4 ture de conversație, programul va fi încheiat.")
    answered=0
    zzz=0
    while True:
        if last_stage=='Stage_3':
            break
        if lang=='en':
            loop_nr+=1
            
            print("SYSTEM: You can choose to quit the program at any time by typing 'quit' . ")
            
            if loop_nr==1:
                
                print("SYSTEM: Your following input should describe the problem.  ")
                

            prompt=input("User: ")
            questions.append(prompt)
            user_input=prompt.strip()

            if loop_nr>1 :
                        
                solved=input("SYSTEM: Was the problem solved ? (y/n):")
                
                if solved=='y':
                    print("EVA: Thank you for using our services. Have a great day!")
                    user_utt[global_category]['Stage_3'].append(user_input)
                    save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json", user_utt)
                    if global_category=='card_loss':
                        report_input=input("SYSTEM : Do you want to generate a report for your missing card? (y/n) : ")
                        if report_input=='y':
                            print("SYSTEM : The system will now confirm your identity.")
                            input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                            if input11 =='y':
                                user_file = personal_info_check(global_category,lang)
                                if user_file:
                                    print("SYSTEM : Generating a report...")
                                    generate_report(user_file)
                                else:
                                    print("Personal info not confirmed.")
                                    sadpath=1 
                                    break

                    break

            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                break
            verificare = None
            okk=0
            for category in user_utt:
                if verificare is not None and okk==1:
                    break
                for stage in user_utt[category]:
                    if verificare is not None and okk==1:
                        break
                    for prompt in user_utt[category][stage]:
                        verificare = new_find_best_match(user_input)
                        if verificare == category:
                            okk=1
                            best_match = prompt
                            global_category = verificare
                            found_category = verificare
                            found_stage = stage
                            last_stage = stage
                            break
                    if verificare is not None and okk==1:
                        break

            if best_match==None:
                found_category=None
                found_stage=None

            if best_match != None: 
                print(f"SYSTEM: From the user input , the found category is '{global_category}' . The robot expects conversation about this category .")
            while True:
                if loop_nr==1 and found_stage!='Stage_1' and best_match is  None:
                    found_stage="Stage_1"
                    proper_start=input("EVA: I cannot recognise what you are asking of me . Is this a proper start to a conversation? (y/n): ")
                    if proper_start=='y':
                        print("EVA: Thank you . The introductory prompt will be added to the database.")
                        if found_category==None:
                            print("SYSTEM: Please select the category this input should be added to. ")
                            global_category = choose_category(user_utt)
                            print(f"You chose category '{global_category}'.")
                            
                        user_utt[global_category]["Stage_1"].append(user_input)
                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)

                        break
                    bad=1
                    if proper_start=='n':
                        while bad==1:
                            print("EVA: Please describe your problem. I am here to help.")
                            print("SYSTEM: The following exchange should describe the problem.  ")
                            prompt=input("User: ")
                            questions.append(prompt)
                            user_input=prompt.strip()                        
                            for category in user_utt:
                                for stage in user_utt[category]:
                                    best_match = find_best_match(user_input, [utterance for utterance in user_utt[category][stage]])
                                    found_category=category
                                    found_stage=stage
                                    if best_match !=  None:
                                        global_category=found_category
                                        break
                            if found_stage!= 'Stage_1':
                                proper_start=input("EVA: I cannot recognise what you are asking of me . Is this a proper start to a conversation? (y/n): ")
                                if proper_start=='y':
                                    print("EVA: Thank you . The introductory prompt will be added to the database.")
                                    found_stage='Stage_1'
                                    bad=0

                                    if best_match==None:
                                        found_category=None
                                    if found_category==None:
                                        print("SYSTEM: Please select the category this input should be added to. ")
                                        global_category = choose_category(user_utt)
                                        print(f"You chose category '{global_category}'.")
                                        user_utt[global_category]["Stage_1"].append(user_input)
                                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
                                    break
                                else:
                                    bad=1
                            else:
                                bad=0
                                break

                else:
                    break
            if last_stage=='Stage_2':
                
                print("SYSTEM: In the following exchanges the problem should be resolved.  ")
                
            if loop_nr==4 and last_stage!='Stage_3' :
                found_stage='Stage_3'
                user_input=user_utt[global_category][found_stage][0]
                print("EVA: I am sorry I could not be of use to you. ")
                sadpath=1

            if found_stage=='Stage_3' and sadpath!=1:
                
                print("SYSTEM: The following exchange should be closing the conversation.  ")

 
            if (global_category=='card_loss' or found_category=='card_loss') and zzz==0:
                zzz=1
                model=AutoModelForSeq2SeqLM.from_pretrained(model_path_for_card_loss)

            response = generate_response(model, tokenizer, user_input)
            answer=remove_spaces(response)

            if answered ==0 and found_stage=='Stage_1' and global_category=='card_address_modification' or global_category=='update_email' or global_category=='update_phone_number':
                answer=answer+' We will need to confirm the ownership of your account before proceeding.'
                print(f"EVA: {answer}")
                responses.append(answer)
                answered=1

                prompt=input("User: ")
                questions.append(prompt)
                user_input=prompt.strip()   
                response = generate_response(model, tokenizer, prompt, last_stage, global_category)
                answer=remove_spaces(response)
                print(f"EVA: {answer}")
                responses.append(answer)
                print()
                print("SYSTEM : The system will now confirm you identity.")
                input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                print()
                if input11 =='y':
                    user_file = personal_info_check(global_category,lang=lang)
                    if user_file:
                        print("EVA: I will now update your personal info.")
                        update_personal_info(global_category, user_file)
                    else:
                        print("Personal info not confirmed.")
                        sadpath=1  
                        break

                else:
                    break
            if loop_nr>=2 and global_category=='close_account':
                print("SYSTEM : Initiating account closure process...")
                acc_close_input=input("SYSTEM : Do you want to close your account? (y/n) : ")
                if acc_close_input=='y':
                    print("SYSTEM : The system will now confirm your identity.")
                    input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                    if input11 =='y':
                        user_file = personal_info_check(global_category,lang)
                        if user_file:
                            print("SYSTEM : Closing your account...")
                            delete_user_file(user_file)
                            break

            if answered == 0:
                print(f"EVA: {answer}")
                responses.append(answer)
            if sadpath ==1:
                if global_category=='card_loss':
                    report_input=input("SYSTEM : Do you want to generate a report for your missing card? (y/n) : ")
                    if report_input=='y':
                        print("SYSTEM : The system will now confirm your identity.")
                        input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                        if input11 =='y':
                            user_file = personal_info_check(global_category,lang)
                            if user_file:
                                print("SYSTEM : Generating a report...")
                                generate_report(user_file)
                            else:
                                print("Personal info not confirmed.")
                                sadpath=1  
                                break
                break

            answered=0
            if last_stage=='Stage_1' or last_stage=='Stage_2' and loop_nr<4:
                last_stage='Stage_2' 
            if last_stage=='Stage_2' and loop_nr!=1:
                user_utt[global_category][last_stage].append(user_input)
                save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
        else:
            loop_nr+=1
            
            print("SYSTEM: Poti iesi din program oricand cu: 'quit' . ")
            if loop_nr==1:
                
                print("SYSTEM: Urmatorul tau input ar trebui sa descrie problema.  ")
            prompt=input("Utilizator: ")
            questions.append(prompt)
            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                break
            
            prompt = mtranslate_translate(prompt, 'en', 'auto')

            print("Textul tradus in engleza este:", prompt)

            user_input=prompt.strip()
            if loop_nr>1 :
                        
                solved=input("SYSTEM: Problema a fost rezolvata? (y/n):")
                
                if solved=='y':
                    print("EVA: Multumim ca ai folosit serviciile noastre!")
                    user_utt[global_category]['Stage_3'].append(user_input)
                    save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json", user_utt)
                    if global_category=='card_loss':
                        report_input=input("SYSTEM : Vrei sa generezi un raport pentru cardul tau pierdut? (y/n) : ")
                        if report_input=='y':
                            print("SYSTEM : Acum trebuie sa iti confirmi identitatea.")
                            input11=input("SYSTEM : Vrei sa continui ? (y/n) : ")
                            if input11 =='y':
                                user_file = personal_info_check(global_category,lang)
                                if user_file:
                                    print("SYSTEM : Generare raport...")
                                    generate_report(user_file)
                                else:
                                    print("Informatii neconfirmate.")
                                    sadpath=1 
                                    break

                    break

            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                break
            verificare = None
            okk=0
            for category in user_utt:
                if verificare is not None and okk==1:
                    break
                for stage in user_utt[category]:
                    if verificare is not None and okk==1:
                        break
                    for prompt in user_utt[category][stage]:
                        verificare = new_find_best_match(user_input)
                        if verificare == category:
                            okk=1
                            best_match = prompt
                            global_category = verificare
                            found_category = verificare
                            found_stage = stage
                            last_stage = stage
                            break
                    if verificare is not None and okk==1:
                        break

            if best_match==None:
                found_category=None
                found_stage=None

            if best_match != None:
                        
                print(f"SYSTEM: Categoria gasita este '{global_category}' . EVA se asteapta la conversatie despre acest subiect .")
            while True:
                if loop_nr==1 and found_stage!='Stage_1' and best_match is not None:
                    found_stage="Stage_1"
                    proper_start=input("EVA: Nu pot recunoaște ce îmi ceri. Este acesta un început potrivit pentru o conversație? (y/n): ")
                    if proper_start=='y':
                        print("EVA: Mulțumesc . Promptul introductiv va fi adăugat la baza de date.")
                        if found_category==None:
                            
                            print("SYSTEM: Vă rugăm să selectați categoria la care ar trebui adăugată această intrare. ")
                            
                            global_category = choose_category(user_utt)
                            print(f"Ai ales categoria '{global_category}'.")
                            
                        user_utt[global_category]["Stage_1"].append(user_input)
                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)

                        break
                    bad=1
                    if proper_start=='n':
                        while bad==1:
                            print("EVA: Te rog descrie problema.")
                            print("SYSTEM: Următorul schimb ar trebui să descrie problema.  ")
                            prompt=input("Utilizator: ")
                            questions.append(prompt)
                            if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                                break
                            prompt = mtranslate_translate(prompt, 'en', 'auto')
                            print("Textul tradus in engleza este:", prompt)
                                        
                            for category in user_utt:
                                for stage in user_utt[category]:
                                    best_match = find_best_match(user_input, [utterance for utterance in user_utt[category][stage]])
                                    found_category=category
                                    found_stage=stage
                                    if best_match !=  None:
                                        global_category=found_category
                                        break
                            if found_stage!= 'Stage_1':
                                proper_start=input("EVA: Nu pot recunoaște ce îmi ceri. Este acesta un început potrivit pentru o conversație? (y/n): ")
                                if proper_start=='y':
                                    print("EVA: Mulțumesc . Promptul introductiv va fi adăugat la baza de date.")
                                    found_stage='Stage_1'
                                    bad=0

                                    if best_match==None:
                                        found_category=None
                                    if found_category==None:
                                        print("SYSTEM: Vă rugăm să selectați categoria la care ar trebui adăugată această intrare. ")
                                        global_category = choose_category(user_utt)
                                        print(f"Ai ales categoria '{global_category}'.")
                                        user_utt[global_category]["Stage_1"].append(user_input)
                                        save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
                                    break
                                else:
                                    bad=1
                            else:
                                bad=0
                                break

                else:
                    break

            if last_stage=='Stage_2':
                
                print("SYSTEM: În următoarele schimburi problema ar trebui rezolvată.  ")
                
            if loop_nr==4 and last_stage!='Stage_3' :
                found_stage='Stage_3'
                user_input=user_utt[global_category][found_stage][0]
                print("EVA: Nu am putut sa te ajut . Imi pare rau. ")
                sadpath=1

            if found_stage=='Stage_3' and sadpath!=1:
                
                print("SYSTEM: Următorul schimb ar trebui să închidă conversația.  ")

            if (global_category=='card_loss' or found_category=='card_loss') and zzz==0:
                zzz=1
                model=AutoModelForSeq2SeqLM.from_pretrained(model_path_for_card_loss)

            response = generate_response(model, tokenizer, user_input)
            answer=remove_spaces(response)

            if answered ==0 and found_stage=='Stage_1' and global_category=='card_address_modification' or global_category=='update_email' or global_category=='update_phone_number':
                answer=answer+' We will need to confirm the ownership of your account before proceeding.'
                answer = mtranslate_translate(answer, 'ro', 'auto')
                print(f"EVA: {answer}")
                responses.append(answer)
                answered=1

                prompt=input("Utilizator: ")
                questions.append(prompt)
                if prompt.lower() == "quit the program" or prompt.lower() == "iesire" or prompt.lower() == "iesire din program" or prompt.lower() == "exit" or prompt.lower() == "quit":
                    break
                
                prompt = mtranslate_translate(prompt, 'en', 'auto')

                print("Textul tradus in engleza este:", prompt)
                user_input=prompt.strip()
                response = generate_response(model, tokenizer, prompt, last_stage, global_category)
                answer=remove_spaces(response)
                answer=mtranslate_translate(answer, 'ro', 'auto')
                print(f"EVA: {answer}")
                responses.append(answer)
            
                print()
                print("SYSTEM : Sistemul vă va confirma acum identitatea.")
                input11=input("SYSTEM : Vrei sa continui ? (y/n) : ")
                print()
                if input11 =='y':
                    user_file = personal_info_check(global_category,lang)
                    if user_file:
                        print("EVA: Iti voi schimba informatiile.")
                        update_personal_info(global_category, user_file)
                    else:
                        print("Informatii neconfirmate.")
                        sadpath=1   
                        break

                else:
                    break
            if loop_nr>=2 and global_category=='close_account':
                print("SYSTEM : Inițierea procesului de închidere a contului...")
                acc_close_input=input("SYSTEM : Vrei sa iti inchizi contul? (y/n) : ")
                if acc_close_input=='y':
                    print("SYSTEM : Sistemul vă va confirma acum identitatea.")
                    input11=input("SYSTEM : Vrei sa continui ? (y/n) : ")
                    if input11 =='y':
                        user_file = personal_info_check(global_category,lang)
                        if user_file:
                            print("SYSTEM : Închiderea contului ...")
                            delete_user_file(user_file)
                            break
            if answered == 0:
                answer=mtranslate_translate(answer, 'ro', 'auto')
                print(f"EVA: {answer}")
                responses.append(answer)
            if sadpath ==1:
                if global_category=='card_loss':
                    report_input=input("SYSTEM : Doriți să generați un raport pentru cardul pierdut? (y/n) : ")
                    if report_input=='y':
                        print("SYSTEM : Sistemul vă va confirma acum identitatea.")
                        input11=input("SYSTEM : Do you want to continue ? (y/n) : ")
                        if input11 =='y':
                            user_file = personal_info_check(global_category,lang)
                            if user_file:
                                print("SYSTEM : Generand un raport...")
                                generate_report(user_file)
                            else:
                                print("Personal info not confirmed.")
                                sadpath=1  
                                break

                break

            answered=0
            if last_stage=='Stage_1' or last_stage=='Stage_2' and loop_nr<4:
                last_stage='Stage_2' 
            if last_stage=='Stage_2' and loop_nr!=1:
                user_utt[global_category][last_stage].append(user_input)
                save_json(r"D:\EVA PROJECT\EVA_VENV\EVA\user_utterance.json",user_utt)
        

from unidecode import unidecode
from sistem_bancar import banking


alegere_model=banking()
from sumarizare import summarize

if alegere_model==2:
        
    ok=1
    while ok==1:
        ro_en=input("EVA : Type the language you wish to use : ")
        if 'en' in ro_en.lower():
            ro_en='en'
            ok=0
            print("SYSTEM : The program will run in the english language mode.")
            my_sound = pygame.mixer.Sound(r"D:\EVA PROJECT\EVA_VENV\EVA\_mesaje_startup\engleza\en_voice_or_text.wav")
            my_sound.play()
            while pygame.mixer.get_busy():
                time.sleep(0.1)
            ok2=1
            while ok2==1:
                voice_text=input("EVA : Type 'voice' if you wish to use the voice mode , or 'text' if you wish to use the text mode : ")
                if 'vo' in voice_text.lower():
                    ok2=0
                    voice_text='voice'
                    print("SYSTEM : The program will run in voice mode.")
                    my_sound = pygame.mixer.Sound(r"D:\EVA PROJECT\EVA_VENV\EVA\_mesaje_startup\engleza\en_not_human.wav")
                    print("EVA : Greetings , I am EVA , a chatbot designed to assist you . Please keep in mind that I am not a real human .")                
                    my_sound.play()
                    while pygame.mixer.get_busy():
                        time.sleep(0.1)
                    chat_bot_v2(ro_en)
                elif 'tex' in voice_text.lower():
                    ok2=0
                    voice_text='text'
                    print("SYSTEM : The program will run in text mode .")
                    print("EVA : Greetings , I am EVA , a chatbot designed to assist you . Please keep in mind that I am not a real human .")
                    chat_bot_text(ro_en)
            else:
                ok2=1
        elif 'ro' in ro_en.lower():
            ro_en='ro'
            ok=0
            
            print("SYSTEM : Programul va rula in modul de limba romana.")
            
            my_sound = pygame.mixer.Sound(r"D:\EVA PROJECT\EVA_VENV\EVA\_mesaje_startup\romana\ro_voice_or_text.wav")
            my_sound.play()
            while pygame.mixer.get_busy():
                time.sleep(0.1)
            ok2=1
            while ok2==1:
                voice_text=input("EVA : Scrieti 'voice' pentru a utiliza modul de voce , sau 'text' pentru a utiliza modul de text : ")
                if 'vo' in voice_text.lower():
                    ok2=0
                    voice_text='voice'
                    print("SYSTEM : Programul va rula in modul de voce.")                   
                    print("EVA : Buna ziua , eu sunt EVA , un asistent virtual creat pentru a va ajuta . Va rog sa tineti minte ca nu sunt o persoana adevarata.")
                    my_sound = pygame.mixer.Sound(r"D:\EVA PROJECT\EVA_VENV\EVA\_mesaje_startup\romana\ro_not_human.wav")
                    my_sound.play()
                    while pygame.mixer.get_busy():
                        time.sleep(0.1)
                    chat_bot_v2(ro_en)                        
                elif 'tex' in voice_text.lower():
                    ok2=0
                    voice_text='text'
                    
                    print("SYSTEM : Programul va rula in modul de text.")
                    
                    print("EVA : Buna ziua , eu sunt EVA , un asistent virtual creat pentru a va ajuta . Va rog sa tineti minte ca nu sunt o persoana adevarata.")
                    chat_bot_text(ro_en)

            else:
                ok2=1
        else:
            ok=1
    today_date_for_filename = today_date.replace(":", "_")


    if voice_text == 'voice':
        with open(f"D:\\EVA PROJECT\\EVA_VENV\\EVA\\outputs_lore\\{ro_en}_testare_voice_conv_{today_date_for_filename}.txt", 'w') as f:
            f.write(f"Voice log {today_date}.")
            f.write('\nUser:\n')
            i = 1
            for question in questions:
                question = replace_diacritics(question)
                question = unidecode(question)  

                f.write(f"{i}. {question}\n")
                i += 1
            f.write('\nEVA:\n')
            i = 1
            for response in responses:
                response = replace_diacritics(response)
                response = unidecode(response)  
                f.write(f"{i}. {response}\n")
                i += 1

                
    else:
        with open(f"D:\\EVA PROJECT\\EVA_VENV\\EVA\\outputs_lore\\{ro_en}_testare_text_conv_{today_date_for_filename}.txt", 'w') as f:
            f.write(f"Text log {today_date}.")
            f.write('\nUser:\n')
            i = 1
            for question in questions:
                f.write(f"{i}. {question}\n")
                i += 1
            f.write('\nEVA:\n')
            i = 1
            for response in responses:
                response=unidecode(response)
                f.write(f"{i}. {response}\n")
                i += 1
elif alegere_model==1:
    summarize()