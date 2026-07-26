FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY Backend/requirements.txt /app/Backend/requirements.txt
RUN pip install --no-cache-dir -r /app/Backend/requirements.txt

# Copy only Backend and Frontend for lightweight production serving
COPY Backend /app/Backend
COPY Frontend /app/Frontend

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "Backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
