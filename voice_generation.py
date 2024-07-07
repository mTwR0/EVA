from TTS.utils.synthesizer import Synthesizer

def generate_audio(text, output_path):
    model_path = r"C:\Users\STAR\AppData\Local\tts\tts_models--en--ljspeech--tacotron2-DDC\model_file.pth"
    config_path = r"C:\Users\STAR\AppData\Local\tts\tts_models--en--ljspeech--tacotron2-DDC\config.json"
    voc_path = r"C:\Users\STAR\AppData\Local\tts\vocoder_models--en--ljspeech--hifigan_v2\model_file.pth"
    voc_config_path = r"C:\Users\STAR\AppData\Local\tts\vocoder_models--en--ljspeech--hifigan_v2\config.json"

    syn = Synthesizer(
        tts_checkpoint=model_path,
        tts_config_path=config_path,
        vocoder_checkpoint=voc_path,
        vocoder_config=voc_config_path,
    )

    outputs = syn.tts(text)
    syn.save_wav(outputs, path=output_path)

