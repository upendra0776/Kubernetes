# Ephemeral Containers

### Links
```https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/
https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/#ephemeral-container
```

### Enable Ephermal Container feature gates
```Minikube: minikube start --feature-gates=EphemeralContainers=true```


### Demo - 01: Debugging with an ephemeral debug container
```
kubectl run ephemeral-demo --image=kunchalavikram/go-app-ms:latest --port=80 --restart=Never
kubectl debug -it ephemeral-demo --image=busybox:1.28 --target=ephemeral-demo
ps aux
curl localhost:80
curl localhost/details
curl localhost/health

kubectl debug -it ephemeral-demo --image=kunchalavikram/curl --target=ephemeral-demo

kubectl describe pod ephemeral-demo
kubectl delete pod ephemeral-demo

Alternative curl images: alpine/curl & curlimages/curl
```

### Demo - 02: Copying a Pod while adding a new container
```
kubectl run myapp --image=kunchalavikram/go-app-ms:latest --port=80 --restart=Never 
kubectl debug myapp -it --image=kunchalavikram/curl --share-processes --copy-to=myapp-debug
```