# Blue-Green Deployment Strategy

### How to implement?
```
# Deploy V1
kubectl apply -f deployment-v1.yaml

# Deploy V2
kubectl apply -f deployment-v2.yaml

# Change selector in service to point to V2 version
kubectl patch service flask -p '{"spec":{"selector":{"version":"v2"}}}'

```