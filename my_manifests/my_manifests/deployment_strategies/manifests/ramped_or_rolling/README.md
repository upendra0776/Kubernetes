# Rolling Update Strategy

Here new version is immediately rolled out in rolling update fashion

### How to implement?

```
# Deploy V1
kubectl apply -f deployment-v1.yaml

# Deploy V2
kubectl apply -f app-v2.yaml --record

# Check rollout status and history
kubectl rollout status deploy <deployment-name>
kubectl rollout history deploy <deployment-name>
kubectl rollout undo deployment <deployment-name>
kubectl rollout undo deployment <deployment-name> --to-revision=2
kubectl set image deployment <deployment-name>  <container-name>=<new-image-name> --record
```
Other commands for deployments
```
$ kubectl scale deployment <deployment-name> --replicas=10 
$ kubectl edit deployment <deployment-name> 
kubectl set image deployment <deployment-name> nginx=nginx:1.16.1  
kubectl delete deployment <deployment-name>
kubectl create deployment <deployment-name> --image nginx --replicas=5 --port=80 --dry-run=client -o yaml > deployment.yaml
kubectl create -f <yaml> --record 
kubectl rollout status deployment <deployment-name>
kubectl rollout history deployment <deployment-name>  
kubectl set image deployment <deployment-name> nginx=nginx:1.14 --record (container name: new image)
kubectl scale deployment <deployment-name> --replicas=10
kubectl rollout undo deployment <deployment-name>
kubectl rollout undo deployment <deployment-name> --to-revision=2
kubectl rollout pause deployment <deployment-name>
kubectl apply -f <yaml> --record 
kubectl delete -f <yaml>.yml
```
