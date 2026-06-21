# Gebruik een lichte Python basis-image


FROM python:3.9-slim

# Omdat we PySpark gebruiken, hebben we Java nodig in de container
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean

# Stel de werkmap in
WORKDIR /app

# Kopieer de benodigdheden en installeer deze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de source code en eventuele modellen
COPY src/ /app/src/

# Open poort 8000 voor de API
EXPOSE 8000

# Start de FastAPI server wanneer de container start
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]