FROM python:3.11.4-alpine

COPY main.py /app/main.py
ENTRYPOINT ["python", "/app/main.py"]