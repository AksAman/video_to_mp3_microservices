#!/bin/bash

micro_svcs=("rabbit" "mongodb" "mongo-express" "auth" "gateway" "adminer" "converter" "notification") 

# kubectl apply -f ../src/{deployment}/mainfests

for micro_svc in "${micro_svcs[@]}"
do
    kubectl delete -f ../src/$micro_svc/manifests
done
