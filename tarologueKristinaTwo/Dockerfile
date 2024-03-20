FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install virtualenv 
RUN python3 -m virtualenv /app/venv

RUN /app/venv/bin/pip install -r requirements.txt

COPY . .

EXPOSE 8000