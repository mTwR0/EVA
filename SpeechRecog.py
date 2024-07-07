import speech_recognition as sr



def parseCommand(lang):
    listener = sr.Recognizer()
    if lang=='en-GB':
        print("Listening for a command...")

        with sr.Microphone() as source:
            listener.pause_threshold=2
            input_speech=listener.listen(source)

        try:
            print("Recognizing speech...")
            query=listener.recognize_google(input_speech,language=lang)
            print(f"said text is : {query}")
        except Exception as exception:
            print("I did not quite catch that.")
            print(exception)
            return 'None'
    else:
        print("Ascultand o comanda...")

        with sr.Microphone() as source:
            listener.pause_threshold=2
            input_speech=listener.listen(source)

        try:
            print("Transcriere voce in text ...")
            query=listener.recognize_google(input_speech,language=lang)
            print(f"Textul spus este : {query}")
        except Exception as exception:
            print("Nu am inteles ce ai spus.")
            print(exception)
            return 'None'

            
    return query


