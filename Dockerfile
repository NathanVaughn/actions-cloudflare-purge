FROM python:3.10.7-alpine

COPY main.py /app/main.py
ENTRYPOINT ["python", "/app/main.py"]