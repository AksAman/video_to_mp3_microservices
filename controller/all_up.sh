#!/bin/bash

micro_svcs=("auth" "gateway" "adminer" "rabbit" "mongodb" "mongo-express")

# kubectl apply -f ../src/{deployment}/mainfests

for micro_svc in "${micro_svcs[@]}"
do
    kubectl apply -f ../src/$micro_svc/manifests
done
