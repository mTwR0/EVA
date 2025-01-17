# Basic Banking System with AI Integration


### Note : The project is for my college graduation paper . This was made to learn about AI , so you are welcome to use it however you wish , but it is overcomplicated for no apparent reason .



## Overview
![image](https://github.com/mTwR0/EVA/assets/147711036/90b81693-1751-4f85-9496-3b342dbe1d58)


This project involves the development of a basic banking system that simulates fundamental functionalities of a mobile banking application. Users can create accounts, authenticate, and manage their respective accounts. Upon authentication, users have the option to interact with one of two available AI implementations.

The conversational AI model is `blenderbot_small-90M` which can be found here : https://huggingface.co/facebook/blenderbot_small-90M

The summarization AI model is `MBZUAI/LaMini-Flan-T5-248M` which can be found here : https://huggingface.co/MBZUAI/LaMini-Flan-T5-248M

The voice model is `speechbrain/tts-tacotron2-ljspeech` which can be found here : https://huggingface.co/speechbrain/tts-tacotron2-ljspeech



### AI Implementations

#### 1. Conversational AI Model

The first AI implementation is a conversational model capable of interacting with users in both Romanian and English languages. This model supports voice and text-based interactions based on user preferences. Its primary role is to act as a virtual assistant, answering queries and providing support to users during their interactions with the banking system.


![image](https://github.com/mTwR0/EVA/assets/147711036/fcde401c-7c66-4c73-8864-f10f07e6734a)


If the user selects the option to chat with the EVA chatbot:
- The user is asked if they want to communicate by voice or text and in which language (Romanian or English).
- The user expresses their problem either in writing or verbally (in the case of voice communication, the input is transcribed into text)
- The system checks if the user's input matches one of a list of inputs stored `user_utterance.json`, ordered by categories and stages (eg "card_loss" with conversation stages).
- Based on this match, the category and stage of the conversation is identified:
  - Stage 1: Description of the initial problem (eg "I lost my card").
  - Stage 2: The detailed conversation about the problem (eg "I last used it 2 days ago").
  - Stage 3: The last exchange of lines between the user and the chatbot.
  - If the issue is not resolved after 4 interactions, this issue is considered unsolvable and the user input is replaced with a specific one to trigger a final response from the chatbot (eg "I want to speak to an employee responsible for personal data modifications.").
- Various checks are implemented to ensure a consistent conversation flow:
  - If the user starts with an input that is similar to those in Stage 2, they are prompted to enter an input from Stage 1.
  - If the opening questions do not match any category, the user is guided to enter an appropriate opening question.
Depending on the identified category, various operations are performed, such as changing the address, the system checking the ownership of the account, checking whether the user knows the information that was used to create the account. After verification, the user data in the text file is updated according to the user's requirements.

The model itself is used in `main_v2.py` .  

#### 2. Summarization AI Model


The second AI implementation is a summarization model designed to deliver concise and relevant information about various banking concepts. This model extracts key insights from documents or data sources, presenting them to users in a summarized and easily understandable format. 

If the user selects the document summary option:
- A list of text documents available on the computer containing information about banking concepts is displayed.
- The user selects a document.
- After a 2-4 minute wait, the system returns a document summary. The summarization model used is MBZUAI_LaMini-Flan-T5-248M, not additionally trained.

![image](https://github.com/mTwR0/EVA/assets/147711036/e767552e-98e1-4b30-b4a4-7babc9600e49)
![image](https://github.com/mTwR0/EVA/assets/147711036/45346c9b-2778-464b-83b6-4e4703f53e6a)

The function for this is written in `sumarizare.py`

### Training process

The training script is `schinbare_antrenare.py` . The other training script , `blenderbot_training.py` is done a bit differently and has worse results for my task . 

TLDR: I loop , one by one , through the excel documents and format them with  `ConversationDataset`  . For each of them I also split the data 80-20 , train for the specified epochs and calculate loss . After all this , model params are updated.

- Implementation of the Conversational Dataset:
- `ConversationDataset`:  handles and processes data from CSV files. Tokenizes data to prepare question and answer pairs for training.
  - Tokenization and Data Preprocessing:
  - Each question-answer pair is tokenized to be compatible with the model. Tokenization includes truncation and padding of sequences to ensure uniform sizes for training.
- Datasets for Training and Validation:
  - The data is split into a training set and a validation set using a proportion of 80% for training and 20% for validation. This separation ensures that the model is evaluated on unseen data to measure its overall performance.
- Configuration of Training Parameters:
  - I configured training parameters using `Seq2SeqTrainingArguments`, which includes settings for number of epochs, batch size, learning rate, model saving strategies and others. 
- Training the Model:
  - `Seq2SeqLM` model is trained using `Seq2SeqTrainer`. At each epoch, the model is trained on the training data set . After the dataset is finished, it is evaluated on the validation dataset to measure performance.
- Performance Evaluation:
  - After finishing each training data set, the model is evaluated on the validation data set to calculate the loss. This process helps to monitor and adjust the performance of the model during training.

### Used dataset
Dataset is question and answer pairs made by me . It is made specifically with this task in mind , and accounts for any operations I do in my code , and that are handled by the system .  
The data used to train the conversation model within the banking system is structured in a format that allows the model to learn to respond appropriately and coherently to various requests and questions from users.
The data used are the `.csv` files.

Data Structure:
- Columns of the Data Set:
  - responses: The model's predefined responses, corresponding to the user's questions and requests.
  - questions: User questions and requests, which must be interpreted and processed by the model to generate appropriate responses.
  - stage: The stage in which the conversation is, indicating whether the user is in the phase of describing the problem or in the actual interaction with the model.
  - intent: The user's intent, i.e. the category or topic discussed in the dialog.
The conversation stage and topic (intent) columns were not passed to the AI ​​model in the training process and exist only for visual delineation.
