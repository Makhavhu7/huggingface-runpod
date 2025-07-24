FROM python:3.10-slim AS builder

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --prefer-binary \
    fastapi==0.115.0 \
    uvicorn==0.30.6 \
    torch==2.4.1+cpu --extra-index-url https://download.pytorch.org/whl/cpu \
    transformers==4.44.2 \
    diffusers==0.30.3 \
    pydantic==2.9.2

FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /app .

ENV HUGGINGFACE_TOKEN=""
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]