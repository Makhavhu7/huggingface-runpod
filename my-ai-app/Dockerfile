FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.30.6 \
    torch==2.4.1 \
    transformers==4.44.2 \
    diffusers==0.30.3 \
    pydantic==2.9.2 \
    scipy==1.14.1 \
    opencv-python==4.10.0.84

ENV HUGGINGFACE_TOKEN="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"
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]