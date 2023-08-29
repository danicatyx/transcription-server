
# Setup

## Local kubernetes cluster

Prerequisites:
- Docker
- kubectl
- helm

Setting up the API:
```bash
minikube start
docker build -t whisperimage -f Dockerfile --build-arg REPLICATE_API_TOKEN=XXXXXXX .
minikube image load whisperimage
kubectl apply -f k8s/deployment.yml
kubectl apply -f k8s/service.yml
```

Verify everything is working properly:
```bash
minikube service flask-service --url
```

Setting up Prometheus and Grafana:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace prometheus
helm install prometheus prometheus-community/kube-prometheus-stack -n prometheus
```

Open Grafana:
```bash
# Get the Username
kubectl get secret -n prometheus prometheus-grafana -o=jsonpath='{.data.admin-user}' |base64 -d
# Get the Password
kubectl get secret -n prometheus prometheus-grafana -o=jsonpath='{.data.admin-password}' |base64 -d
# Expose the grafana service
minikube service prometheus-grafana -n prometheus   
```

Then log into Grafana and follow these steps to monitor the cluster:
- Add the Prometheus data source and specifiy the URL: http://prometheus-kube-prometheus-prometheus:9090 (which is the service IP inside the cluster)
- Add a new dashboard, import by using Grafana id 6417 or use the default dashboards for prometheus (in the data source settings)




# Run
## Port forward

You can forward the remote 80 port to your local 5555 port with the following command:
```bash
kubectl port-forward service/flask-service 5555:80
```

You can then access the flask app at http://localhost:5555/transcribe