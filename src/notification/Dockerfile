FROM python:3.10-slim-bullseye

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    netcat curl \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN ls -la /app

ENTRYPOINT [ "/app/scripts/docker-entrypoint.sh" ]
