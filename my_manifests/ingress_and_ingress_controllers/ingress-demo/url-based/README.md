# URL Based Routing

## Install Traefik Helm chart
```
https://doc.traefik.io/traefik/getting-started/install-traefik/#use-the-helm-chart
https://doc.traefik.io/traefik/v1.7/user-guide/kubernetes/
https://github.com/containous/traefik/tree/v1.7/examples/k8s
```

## Install via Helm chart

```
helm repo add traefik https://helm.traefik.io/traefik
helm repo update
helm install traefik traefik/traefik
```

```
kubectl port-forward $(kubectl get pods --selector "app.kubernetes.io/name=traefik" --output=name) 9000:9000
http://127.0.0.1:9000/dashboard/#/
``