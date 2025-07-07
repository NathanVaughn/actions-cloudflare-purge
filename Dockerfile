FROM python:3.13.5-alpine

COPY main.py /app/main.py
ENTRYPOINT ["python", "/app/main.py"]