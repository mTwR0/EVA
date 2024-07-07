from voice_generation import generate_audio
from functii import add_new_intent , find_best_match , get_answer_for_question  , get_intent , get_words , load_intents , load_knowledge_base , save_intents , save_knowledge_base
from SpeechRecog import parseCommand
import pygame 
EVA_AUDIO_OUTPUT_PATH=r"D:\EVA PROJECT\EVA\output.wav"
pygame.init()

#                                                       continua cu nltk sa generezi text dinamic --> vf in dinamic.docx

# ia input -->


def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")
    intents: dict = load_intents("intents.json")
    best_match = None  # Initialize best_match to None
    while True:
        user_input: str = input("You: ")
        #user_input=parseCommand()
        if user_input.lower() == "quit":
            break

        recognized_intent: str | None = get_intent(user_input, intents)


        # Prompt for the intent only if it doesn't exist
        if  recognized_intent == None:
            print("EVA: The intent is not recognized. What is the intent?")
            recognized_intent = input("Type the intent name: ")

            #acum adaugi inputul in intents.json


            if recognized_intent.lower() != "skip":
                if recognized_intent not in intents:
                    # Create a new intent with keywords
                    intents[recognized_intent] = [user_input]
                    save_intents("intents.json", intents)
                    print(f"EVA: Created a new intent: {recognized_intent}")
                else:
                    print(f"EVA: The intent '{recognized_intent}' already exists. ")
                    if user_input not in intents[recognized_intent]:

#aici trb sa adauge doar cuvintele care determina ca intentul e ce e --> how why what etc pt intrebari

                        print(f"EVA:  Added {user_input} to {recognized_intent} in intents.json .")
                        intents[recognized_intent].append(user_input)
                        save_intents("intents.json", intents)


        # Always look for a match in the knowledge base
        best_match = find_best_match(user_input, [q["prompt"] for q in knowledge_base[recognized_intent]])
                
                
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base, recognized_intent)
            
            
            #modified here 

            # generate_audio(answer, EVA_AUDIO_OUTPUT_PATH)
            # my_sound = pygame.mixer.Sound(EVA_AUDIO_OUTPUT_PATH)
            # my_sound.play()
            print(f"EVA: {answer}")


            
        else:
            print("EVA: I don't know the answer. Teach me?")
            new_answer = input("Type the answer or 'skip' to skip: ")
            if new_answer.lower() != "skip":
                if recognized_intent not in knowledge_base:
                    knowledge_base[recognized_intent] = []

                # Check if the prompt already exists in this intent
                prompt_exists = any(q["prompt"] == user_input for q in knowledge_base[recognized_intent])
                if not prompt_exists:
                    knowledge_base[recognized_intent].append({"prompt": user_input, "answer": new_answer})
                    save_knowledge_base("knowledge_base.json", knowledge_base)
                    print("EVA: I learned something new. Thank you.")

if __name__ == "__main__":
    chat_bot()
