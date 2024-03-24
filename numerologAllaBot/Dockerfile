FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install virtualenv 
RUN python3 -m virtualenv /app/venv

RUN /app/venv/bin/pip install -r requirements.txt

COPY . .

CMD ["/app/venv/bin/python", "bot.py"]


EXPOSE 8000