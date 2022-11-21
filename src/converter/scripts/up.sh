# RUN FROM parent directory (./scripts/up.sh)

docker build -t peace2103/vmp3_converter_service:latest . || exit 1;
docker push peace2103/vmp3_converter_service:latest || exit 1;
kubectl apply -f ./manifests/ || exit 1;
kubectl rollout restart deployment converter || exit 1;