FROM python:3.11.0b5-alpine

COPY main.py /app/main.py
ENTRYPOINT ["python", "/app/main.py"]