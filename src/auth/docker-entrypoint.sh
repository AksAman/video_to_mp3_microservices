#!/bin/sh

if [ "$POSTGRES_SCHEMA" = "postgresql" ]
then
    echo "Waiting for postgres..."

    # while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do 
    #   sleep 1; 
    # done
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
    flask db upgrade  
fi

exec "$@"