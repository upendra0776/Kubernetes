# Network Policies
[Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

In a Kubernetes cluster, by default, all pods are non-isolated, meaning all ingress and egress traffic is allowed. Once a network policy is applied and has a matching selector, the pod becomes isolated, meaning the pod will reject all traffic that is not permitted by the aggregate of the network policies applied. The order of the policies is not important; an aggregate of the policies is applied.

Kubernetes provides networking functionality by using network plugins. Unless you have a network plugin that can implement network policies, you will not be able to use the functionality. Please note that even if the API server accepts the network policy configuration, this doesn’t mean that it will be implemented unless a controller understands and implements the policy. Several network plugins support network policies and much more.

# Network Plugins
There are two types of network plugins:
- CNI
- Kubenet

CNI type plugins follow the Container Network Interface spec and are used by the community to create advanced featured plugins. On the other hand, Kubenet utilizes bridge and host-local CNI plugins and has basic features.

Several network plugins were developed from various organizations, including but not limited to Calico, Cilium, and Kube-Router. A complete list can be found in Cluster Networking documentation. These network plugins provide Network Policy implementation and more, such as advanced monitoring, L7 filtering, integration to cloud networks, etc.

While some network plugins use Netfilter/iptables in their underlying infrastructure, others use eBPF technology on the underlying data path. Netfilter/iptables is very mature and builtin into the kernel. On the other hand, eBPF allows you to change the functionality on the fly without kernel upgrade. Not being dependent on the kernel version has led some big players to use eBPF based network plugins on very large scales.

It is imperative to select the correct network plugin for your Kubernetes cluster(s). If you are using cloud providers for your Kubernetes setup (such as AWS, Azure, GCP), they might already have deployed a network plugin that supports network policies. Please check the cloud provider documentation for further details.


# Writing & Applying Network Policies
In a Kubernetes cluster, by default, all pods are non-isolated, meaning all ingress and egress traffic is allowed. Once a network policy is applied and has a matching selector, the pod becomes isolated, meaning the pod will reject all traffic that is not permitted by the aggregate of the network policies applied. The order of the policies is not important; an aggregate of the policies is applied.

## Network Policy Resource Fields
Fields to define when writing network policies:

### podSelector
  podSelector selects a group of pods using a LabelSelector. If empty, it would select all pods in the namespace, so beware when using it.

### policyTypes
  policyTypes lists the type of rules that network policy includes. Value can be ingress, egress, or both.

#### ingress
  ingress defines the rules that will be applied to the ingress traffic of the selected pod(s). If it is empty, it matches all the ingress traffic. If it is absent, it doesn’t affect ingress traffic.

#### egress
  egress defines the rules that will be applied to the egress traffic of the selected pod(s). If it is empty, it matches all the egress traffic. If it is absent, it doesn’t affect egress traffic.

### Egress Rules
An array of rules that would be applied to the traffic going out of the pod. It is defined with the following fields.

Fields:

- ports: an array of NetworkPolicyPort (port, endport, protocol)
- to: an array of NetworkPolicyPeer (ipBlock, namespaceSelector, podSelector)

## Ingress Rules
An array of rules that would be applied to the traffic coming into the pod. It is defined with the following fields.

Fields:

- from: an array of NetworkPolicyPeer (ipBlock, namespaceSelector, podSelector)
- ports: an array of NetworkPolicyPort (port, endport, protocol)

# Examples
As an example, I'm using MySQL DB and a Python application that checks the connection to this DB.
Alternatively you can also use nginx webserver as an example
```
kubectl run web --image=kunchalavikram/go-app-ms:latest -l app=web --port 80 --expose 
kubectl run test --rm -i -t --restart=Never --image=alpine -- wget -qO- --timeout=2 http://web/details

(or)

kubectl run web --image=nginx --port 80 --expose 
kubectl run test --rm -i -t --restart=Never --image=alpine -- wget -qO- --timeout=2 http://web

(or)

kubectl apply -f db-connection-test/mysql_deployment.yml
kubectl run test --image=kunchalavikram/db-connection-test:latest --env="DB_HOST=mysql" --env="DB_USER=root" --env="DB_PASSWORD=root" --rm -it --restart=Never     
```

## Setup Minikube with Calico CNI
A vanilla minikube installation (minikube start) does not support any NetworkPolicies, since the default CNI, Kindnet, does not support Network Policies, by design. So use CNI plugins like Calico
```
minikube start --driver=virtualbox --cni calico
```
## Setup Minikube with Weavenet
```
https://github.com/weaveworks/weave/issues/3124#issuecomment-397820940
```

## View your policy
```
https://orca.tufin.io/netpol/
https://editor.cilium.io/
https://cilium.io/blog/2021/02/10/network-policy-editor
```

## Delete/clean up all policies
```
kubectl delete networkpolicy --all
```

## Deny all traffic
Denies all incoming and outgoing traffic
```
kubectl apply -f denyall.yaml
kubectl run test --image=kunchalavikram/db-connection-test:latest --env="DB_HOST=mysql" --env="DB_USER=root" --env="DB_PASSWORD=root" --rm -it --restart=Never  
```
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
spec:
  podSelector: {} # If empty, it would select all pods in the namespace
  policyTypes:
  - Ingress
  - Egress
```

## Deny all ingress in a specific namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Ingress
```
or set ingress to empty array
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress-policy
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress: []
```

## Deny all egress in a specific namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: advanced-policy-demo
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Egress
```

## Deny all egress except for kube-system namespace
In the above case deny all egress traffic will make DNS resolution to fail as
pods cannot query core-dns through kube-dns. So allow egress to kube-dns namespace
so pods can reach kube-dns service on port 53
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-access
  namespace: advanced-policy-demo
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: kube-system
    ports:
    - protocol: UDP
      port: 53
```
This will allow the DNS resolution but still this pod cannot talk to other. We need to modify egress

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-access
spec:
  podSelector:
    matchLabels: {}
  policyTypes:
  - Egress
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: kube-system
    - podSelector:
        matchLabels:
          app: web
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 80
```

## Allow only ingress in a specific namespace or to a specific pod
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {}
  ingress:
  - {}
  policyTypes:
  - Ingress
```
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: access-nginx
spec:
  podSelector:
    matchLabels:
      app: web
  ingress:
    - from:
      - podSelector:
          matchLabels: {}
```

## Allow only egress in a specific namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-egress
spec:
  podSelector: {}
  egress:
  - {}
  policyTypes:
  - Egress
```

## Allow from a specific pod with pod labels
This is within the same namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: access-nginx
spec:
  policyTypes:
  - Ingress
  podSelector:
    matchLabels:
      app: web
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: "true"
```
```
kubectl run test -l access=true --rm -i -t --restart=Never --image=alpine -- wget -qO- --timeout=2 http://web/details
```
If you want from all namespaces; add namespace selector
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector:
    matchLabels:
      app: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: dev
      namespaceSelector: {}
```

## Allow Access to a Group of Pods from Another Namespace
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-debug
spec:
  podSelector:
    matchLabels:
      component: app
  ingress: 
  - from:
    - podSelector:
        matchLabels:
          component: debug
      namespaceSelector:
        matchLabels:
          space: monitoring
  policyTypes:
  - Ingress
```

## Allow from all resources in a namespace on a specific port
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-on-port
spec:
  podSelector:            
    matchLabels:
      app: web 
  ingress:
    - ports:
        - protocol: TCP
          port: 80
      from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: dev
          podSelector:
            matchLabels:
              app: test
```
```
kubectl run test -n dev -l app=test --rm -i -t --restart=Never --image=alpine -- wget -qO- --timeout=2 http://web.default/details
```

## Allow egress for specific pods to a specific port on a pod

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-egress-port
spec:
  policyTypes:
  - Egress
  podSelector:
    matchLabels:
      app: test
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: web
  - ports:
    - port: 80
      protocol: TCP
    - port: 53
      protocol: UDP
```

## Allow ingress traffic from specific pods in another namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: specific-allow
spec:
  podSelector:
    matchLabels:
      app: web
  ingress:
    - from:
      - namespaceSelector:    
          matchLabels:
            kubernetes.io/metadata.name: dev 
        podSelector:       
          matchLabels:
            app: test
```

## Allow ingress traffic from all pods in another namespace and selected pods in current namespace

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ns-selected
spec:
  podSelector:
    matchLabels:
      app: web
  ingress:
    - from:
      - namespaceSelector:     # chooses all pods in namespaces labelled with team=operations
          matchLabels:
            kubernetes.io/metadata.name: dev  
      - podSelector:           # chooses pods with type=monitoring
          matchLabels:
            app: test
```

## Demo Example
Create a network policy to allow Python application only to the mysql database service 3302 and wishlist service on 8080
Open all Ingress traffic.
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: python-np
spec:
  podSelector:
    matchLabels:
      app: web
  egress:
  - to:
      - podSelector:
          matchLabels:
            app: wishlist
    ports:
    - port: 8080
      protocol: TCP
  - to:
      - podSelector:
          matchLabels:
            app: mysql
    ports:
    - port: 3306
      protocol: TCP
  policyTypes:
  - Ingress
  - Egress
```