import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import io
import base64

app = FastAPI()

preload_models()

class GenerateRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_audio(req: GenerateRequest):
    try:
        audio_array = generate_audio(req.text)
        buffer = io.BytesIO()
        write_wav(buffer, SAMPLE_RATE, audio_array)
        audio_b64 = base64.b64encode(buffer.getvalue()).decode()
        return {"audio_b64": audio_b64}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)