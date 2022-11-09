FROM python:latest

RUN pip install \
    psycopg2-binary \
    requests \
    fastapi \ 
    "uvicorn[standard]" 

EXPOSE 8000
EXPOSE 80

COPY src/ /app/

WORKDIR /app

CMD ["python3", "app.py"]
