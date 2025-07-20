from bark import generate_audio, preload_models
import base64
import torchaudio

preload_models()

def generate_audio(prompt: str):
    waveform = generate_audio(prompt, history_prompt=None)
    torchaudio.save("audio.wav", waveform, sample_rate=24000)
    with open("audio.wav", "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")
    return {"audio_base64": audio_b64}
