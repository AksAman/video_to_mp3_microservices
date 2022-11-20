#!/bin/sh

if [ "$RABBITMQ_ENABLED" = "True" ]
then
    echo "Waiting for rabbitmq..."

    # while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do 
    #   sleep 1; 
    # done
    while ! nc -z $RABBITMQ_HOST $RABBITMQ_PORT; do
      sleep 0.1
    done

    echo "RabbitMQ started"
fi

python3 src/app.py
exec "$@"