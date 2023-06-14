FROM python:3.11

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

COPY requirements.txt .

COPY . .

CMD ["python", "app.py"]
