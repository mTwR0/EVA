import subprocess

def install_spacy_model(model):
    subprocess.call(['python', '-m', 'spacy', 'download', model])


  install_spacy_model('en_core_web_sm')
