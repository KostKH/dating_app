FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
RUN sed -i'.bak' 's/$/ contrib/' /etc/apt/sources.list
RUN apt-get update; apt-get install -y ttf-mscorefonts-installer fontconfig
COPY . .
CMD ["gunicorn", "dating_app.wsgi:application", "--workers", "2", "--bind", "0:8000"]
