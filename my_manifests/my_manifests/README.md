# Kubectl Commands

### Basic Commands
```
kubectl --help
kubectl version
kubectl version --short
kubectl version -o yaml 
kubectl cluster-info
kubectl get componentstatuses  # Get status of k8s components
kubectl get nodes -o wide # Also supports output formatting in YAML &JSON 
kubectl api-resources
kubectl api-versions
kubectl explain <object>.<option> 
kubectl explain pod
kubectl explain pod.apiVersion
kubectl explain pod.spec
kubectl api-resources --namespaced=true     
kubectl api-resources --namespaced=false     # All non-namespaced resources
kubectl api-resources -o name                # All resources with simple output (just the resource name)
kubectl api-resources -o wide                # All resources with expanded output
kubectl api-resources --verbs=list,get       # All resources that support the "list" and "get" request verbs
```