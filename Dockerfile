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

CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
