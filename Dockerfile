FROM python:3.9-slim

WORKDIR /project

COPY * /project

RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "server_main:app", "--host", "0.0.0.0", "--port", "8000"]