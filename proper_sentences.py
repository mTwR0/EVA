# from deepmultilingualpunctuation import PunctuationModel
# def proper_sentences(text):
#     model = PunctuationModel()
#     text = "what is up eva how are you today"
#     result = model.restore_punctuation(text)
#     return result

# def remove_spaces_around_quotes(text):
#     # Replace spaces around single quotes
#     cleaned_text = text.replace(" '", "'").replace("' ", "'")
#     cleaned_text = cleaned_text.replace(" ,", ",").replace(", ", ",")
#     cleaned_text = cleaned_text.replace(" .", ".")
#     cleaned_text = cleaned_text.replace(" ?", "?")
#     return cleaned_text

# # Example usage:
# original_text = " hello , how are you today ? i ' m good . how about you ? what do you do for fun ?"
# cleaned_text = remove_spaces_around_quotes(original_text)

# print(f"Original Text: '{original_text}'")
# print(f"Cleaned Text: '{cleaned_text}'")





# import re

# def is_sentence(text):
#     keywords = ['I', 'You', 'He', 'She', 'It', 'We', 'They', 'Hello', 'Hi', 'Hey', 'Greetings', 'Dear', 'What', 'Do', 'Did', 'Can', 'Could', 'Should', 'Would', 'Will']

#     return any(keyword in text.lower() for keyword in keywords) 


# daca gaseste un cuvnt de asta , adauga . inainte , daca nu e primul cuvant din propozitie. 

# def add_dot(text):
#     # List of common words sentences often start with
#     keywords = ['I', 'You', 'He', 'She', 'It', 'We', 'They', 'Hello', 'Hi', 'Hey', 'Greetings', 'Dear', 'What', 'Do', 'Did', 'Can', 'Could', 'Should', 'Would', 'Will']
#     words = text.split()

#     # Use a list to accumulate modified words
#     modified_words = []

#     for i, word in enumerate(words):
#         # Add a dot before the word if it's not the first word and it's in the keywords list
#         if i != 0 and word.capitalize() in keywords:
#             modified_words.append(f'.{word}')
#         else:
#             modified_words.append(word)

#     # Join the modified words back into a sentence
#     modified_text = ' '.join(modified_words)

#     return modified_text

# # Example usage
# sentence = "I like to play games and watch YouTube videos what about you"
# #           I like to play games and watch YouTube videos .what about .you
#                 # verifica cu spacy ? daca are partile de vorbire pentru o propozitie ? 
# modified_sentence = add_dot(sentence)
# print(modified_sentence)

                            # checks if the sentence text argument contains any of the words in the keywords list

#I You He She It We They Hello Hi Hey Greetings Dear What Do
# ce vreau sa faca ?
# hello eva how are you --> Hello,eva.How are you ?
                            # dupa greeting = , ;; eva = EVA ;; inainte de how =. + contine how = ? ;; scapi de spatii ne-necesare
                                                            # daca in stanga e . si nu e I sau nume sau EVA --> capitalize
                                # daca ai folosit o regula de asta == ai un counter =1 , poate e nev in caz ca u vr sa se aplice reguli de mai multe ori

# pasi :"I like to play games and watch YouTube videos what about you" sau hi how are you today eva how are you doing 
            # 1. pui . unde e nev 
                            #  I like to play games and watch YouTube videos . what about you ."
                            #  hi eva . how are you today .  what are you doing . i am doing fine. 
                            #  hi , EVA. how are you today? what are you doing ? i am doing fine. 
                            
                            
                            
                            
# def add_comma_after_greeting(sentence):
#     # List of common greetings
#     greetings = ['hi', 'hello', 'hey', 'greetings']

#     # Split the sentence into words
#     words = sentence.split()

#     # Iterate over each word
#     for i, word in enumerate(words):
#         # Check if the word is a greeting
#         if word.lower() in greetings:
#             # Add a comma after the greeting
#             words[i] = f'{word},'

#     # Join the modified words back into a sentence
#     sentence = ' '.join(words)

#     return sentence

# def capitalize_eva(sentence):
#     # Check if 'eva' is present in the sentence
#     if 'eva' in sentence.lower():
#         # Capitalize 'eva' and add a comma before it
#         sentence = re.sub(r'\beva\b', 'EVA', sentence, flags=re.IGNORECASE)
#         sentence = sentence.replace('EVA', ',EVA')

#     return sentence

# def make_proper_sentence(sentence):
#     # Capitalize the first letter of the sentence
#     sentence = sentence.capitalize()

#     # Add a comma after the greeting, if present
#     sentence = add_comma_after_greeting(sentence)

#     # Capitalize 'eva' and add a comma before it, if present
#     sentence = capitalize_eva(sentence)

#     # Add a period at the end if it's not already there and it's not a question
#     if not sentence.endswith('.') and not is_question_intent(sentence):
#         sentence += '.'

#     # Add a question mark at the end if it's a question
#     if is_question_intent(sentence):
#         sentence += '?'

#     return sentence

# # Example usage
# def example():
#     question_sentence = "I am fine how are you are you good are you bad"
#     greeting_sentence = "hello how are you today"
#     g="I play games and programme what about you"
#     a="hello Eva I am your creator"
#     b="I'm a programmer what about you"
#     c="I like to play games and watch YouTube videos what about you"
#     d="things like dark souls or elder ring did you do you know of any of them"
#     e="I see do you know that if I close the program right now you will die"
#     f="if I close this program right now you will cease to exist"

#     proper_question_sentence = make_proper_sentence(question_sentence)
#     proper_greeting_sentence = make_proper_sentence(greeting_sentence)

#     print(proper_question_sentence)
#     print(proper_greeting_sentence)
#     print(make_proper_sentence(g))
#     print(make_proper_sentence(f))
#     print(make_proper_sentence(e))
#     print(make_proper_sentence(d))
#     print(make_proper_sentence(c))
#     print(make_proper_sentence(b))
#     print(make_proper_sentence(a))
# #     #outputs:
#I am fine how are you are you good are you bad?
# Hello, how are you today?
# I play games and programme what about you?
# If i close this program right now you will cease to exist?
# I see do you know that if i close the program right now you will die?
# Things like dark souls or elder ring did you do you know of any of them?
# I like to play games and watch youtube videos what about you?
# I'm a programmer what about you?
# Hello, ,EVA i am your creator?
# Call the example function



#example()



# def make_proper_sentence_custom(input_text):
#     # Split the input text into a list of words
#     words = input_text.split()

#     # Identify specific words to capitalize differently
#     # custom_capitalization = {'hello', 'i'}
#     custom_capitalization = {'i',  'he', 'she', 'it', 'we', 'they', 'hello', 'hi', 'hey', 'greetings', 'dear','what','do'}


#     # Reconstruct the input text with custom capitalization and period placement
#     reconstructed_text = []
#     for i, word in enumerate(words):
#         reconstructed_text.append(word.capitalize())
#         # Add a period after the word if the next word is in the list
#         if i + 1 < len(words) and words[i + 1].lower() in custom_capitalization:
#             reconstructed_text.append('.')

#     # Convert the reconstructed list of words back to a sentence
#     output_text = ' '.join(reconstructed_text)

#     # Add a period at the end if it's not already there
#     if not output_text.endswith('.'):
#         output_text += '.'

#     return output_text

# g="I play games and program what about you" #I Play Games And Program . What About . You.
# a="hello Eva I am your creator"
# b="I'm a programmer what about you"#I'm A Programmer . What About . You.
# c="I like to play games and watch YouTube videos what about you"
# d="things like dark souls or elder ring do you know of any of them"
# e="I see do you know that if I close the program right now you will die" #I See . Do You Know That If . I Close The Program Right Now You Will Die.
# f="if I close this program right now you will cease to exist" #If . I Close This Program Right Now You Will Cease To Exist.
# h="if i like the food i will eat it "   
#         # fix : it se refera la food --> detectare
#         # I dupa if
#         #               --> spacy

# # Example usage
# #input_sentence = "hello eva i am your creator"
# output_sentence = make_proper_sentence_custom(h)
# print(output_sentence)
