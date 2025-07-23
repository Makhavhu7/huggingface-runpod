from transformers import AutoProcessor, BarkModel
import scipy.io.wavfile
import torch
import os

class AudioGenerator:
    def __init__(self):
        model_id = "suno/bark"
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.model = BarkModel.from_pretrained(model_id)
        self.model = self.model.to("cuda" if torch.cuda.is_available() else "cpu")

    def generate(self, prompt, output_path="output_audio.wav"):
        inputs = self.processor(prompt, return_tensors="pt")
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        audio_array = self.model.generate(**inputs)
        audio_array = audio_array.cpu().numpy().squeeze()
        scipy.io.wavfile.write(output_path, rate=24000, data=audio_array)
        return output_path

    def health_check(self):
        return self.model is not None