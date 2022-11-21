# RUN FROM parent directory (./scripts/up.sh)

docker build -t peace2103/vmp3_notification_service:latest . || exit 1;
docker push peace2103/vmp3_notification_service:latest || exit 1;
kubectl apply -f ./manifests/ || exit 1;
kubectl rollout restart deployment notification || exit 1;