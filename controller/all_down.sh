#!/bin/bash

statefulsets=("db" "rabbitmq" "vmp3-mongo")
for set in "${statefulsets[@]}"
do
    kubectl delete statefulset $set
    # kubectl scale statefulset $set --replicas=0
done


services=("auth" "db" "gateway" "adminer" "rabbitmq" "vmp3-mongo" "mongo-express")
for service in "${services[@]}"
do
    kubectl delete service $service
done


deployments=("auth" "gateway" "adminer" "mongo-express" "converter")

for deployment in "${deployments[@]}"
do
    # kubectl scale deployment $deployment --replicas=0
    kubectl delete deployment $deployment
done





