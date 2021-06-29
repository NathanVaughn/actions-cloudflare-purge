FROM python:3.9-alpine

COPY main.py /app/main.py
ENTRYPOINT ["python", "/app/main.py"]