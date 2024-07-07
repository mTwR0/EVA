from TTS.utils.synthesizer import Synthesizer

def generate_audio(text, output_path):
    model_path = r""
    config_path = r""
    voc_path = r""
    voc_config_path = r""

    syn = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        vocoder_checkpoint=voc_path,
        vocoder_config=voc_config_path,
    )

    outputs = syn.tts(text)
    syn.save_wav(outputs, path=output_path)

