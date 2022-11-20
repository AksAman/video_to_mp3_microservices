#!/bin/sh

if [ "$RABBITMQ_ENABLED" = "True" ]
then
    echo "Waiting for rabbitmq..."

    while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
      sleep 0.1
    done

    echo "RabbitMQ started"
fi

python3 src/app.py
exec "$@"