FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Requisitos de la aplicación (están en backend/requirements.txt)
COPY backend/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# Código de la aplicación (carpeta backend/app)
COPY backend/app ./app

EXPOSE 8080

CMD ["python", "-m", "app.main"]
