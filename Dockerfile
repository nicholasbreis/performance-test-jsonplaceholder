FROM python:3.11-slim

WORKDIR /app

RUN pip install locust --no-cache-dir

COPY locustfile.py .

# Cria pasta de resultados dentro do container
RUN mkdir -p /app/results

ENTRYPOINT ["locust", "-f", "locustfile.py"]
