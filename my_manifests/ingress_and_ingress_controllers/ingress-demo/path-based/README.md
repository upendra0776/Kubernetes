# Path Based Routing

## Deploy Nginx Ingress Controller
```
https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal
```

## URL Based for same example
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: url-based-rules
spec:
  rules:
  - host: hello.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: hello
            port:
              number: 80
  - host: greet.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: greet
            port:
              number: 80
  - host: details.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: details
            port:
              number: 80
```


