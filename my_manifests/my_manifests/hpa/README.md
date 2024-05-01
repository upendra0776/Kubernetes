# HorizontalPodAutoscaler 

https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/


## Install Metrics Server
https://github.com/kubernetes-sigs/metrics-server
```
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```
```
https://www.linuxsysadmins.com/service-unavailable-kubernetes-metrics/
```
Edit the deployment
```
kubectl edit deployments.apps -n kube-system metrics-server 
```
Add below to the container section
```
spec:
  containers:
  - args:
    - --kubelet-insecure-tls=true
    - --kubelet-preferred-address-types=InternalIP
```
Add this below dns policy or at the end of the container section
```
hostNetwork: true
```
Get metrics of nodes and pods
```
kubectl top nodes
kubectl top pods
```

## Create the HorizontalPodAutoscaler 
```
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
kubectl get hpa
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
kubectl get hpa php-apache --watch
kubectl top po -l run=php-apache
kubectl get deployment php-apache
```
Stop the load
```
kubectl get hpa php-apache --watch

