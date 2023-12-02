# Use a base image
FROM python:3.9

# Install zlib1g from a specific repository with a newer version
RUN echo "deb http://deb.debian.org/debian buster main" > /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y zlib1g=1:1.2.11.dfsg-1

WORKDIR /opt/backend

RUN python3 -m pip install virtualenv 
RUN python3 -m virtualenv /opt/backend/venv

COPY ./pyproject.toml ./poetry.lock* /opt/backend/

RUN /opt/backend/venv/bin/pip install poetry

RUN /opt/backend/venv/bin/poetry config virtualenvs.create false
RUN /opt/backend/venv/bin/poetry install --no-dev --no-root

COPY . /opt/backend

CMD ["/opt/backend/venv/bin/poetry", "run", "fastapi-app"]

EXPOSE 8000
