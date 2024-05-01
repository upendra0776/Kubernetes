# Canary Deployment Strategy using deployments

### How to implement?
```
# Deploy both V1 & V2 by setting V1 to 5 replicas and V2 to 0 initially
kubectl apply -f canaries_using_deployments.yaml

# Gradually scale up V2 replicas and scale down V1 replicas
kubectl scale deploy flask-v1 --replicas=4
kubectl scale deploy flask-v2 --replicas=1
```