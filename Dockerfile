FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

ENV OPENAI_API_KEY="sk-ds-team-general-uRHEpM4v8JyZPznqvmSMT3BlbkFJPIMx3gi9v6BQOn58RbSN"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
