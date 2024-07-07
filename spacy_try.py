import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

def has_valid_sentence_structure(text):
    # Process the text using spaCy
    doc = nlp(text)
    for token in doc:
        print(token.text , token.pos_,token.dep_)
    print()
    # Minimum required number of verbs for a valid sentence
    min_verbs = 1
    #min_adp=1

    # Count the number of verbs in the document
    verbs = [token.text for token in doc if token.pos_ == "VERB"]

    # Check if the sentence has enough verbs
    return len(verbs) >= min_verbs

# Example usage
input_text = "how are you today"
result = has_valid_sentence_structure(input_text)

if result:
    print("The input has a valid sentence structure.")
else:
    print("The input does not have a valid sentence structure.")
