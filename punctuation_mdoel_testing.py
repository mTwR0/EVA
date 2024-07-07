from deepmultilingualpunctuation import PunctuationModel

model = PunctuationModel()
text = "My name is Clara and I live in Berkeley California Ist das eine Frage Frau Müller"
result = model.restore_punctuation(text)
print(result)
