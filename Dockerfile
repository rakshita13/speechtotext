FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV PYTHONUNBUFFERED=1

ENV OPENAI_API_KEY="sk-ds-team-general-uRHEpM4v8JyZPznqvmSMT3BlbkFJPIMx3gi9v6BQOn58RbSN"

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]