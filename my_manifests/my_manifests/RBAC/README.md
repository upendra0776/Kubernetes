# RBAC

## Links
```
https://kubernetes.io/docs/reference/access-authn-authz/authentication/
https://kubernetes.io/docs/reference/access-authn-authz/certificate-signing-requests/
https://www.openlogic.com/blog/granting-user-access-your-kubernetes-cluster
https://kubernetes.io/docs/reference/access-authn-authz/rbac/
https://www.openlogic.com/blog/granting-user-access-your-kubernetes-cluster
https://cloudhero.io/creating-users-for-your-kubernetes-cluster
```

## Generate certs
```
openssl genrsa -out vikram.key 2048
openssl req -new -key vikram.key -out vikram.csr 
(or)
openssl req -new -key vikram.key -out vikram.csr -subj "/CN=vikram"

cat vikram.csr | base64 | tr -d "\n"
```

```
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: vikram
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0NCk1JSUNtekNDQVlNQ0FRQXdWakVMTUFrR0ExVUVCaE1DUVZVeEV6QVJCZ05WQkFnTUNsTnZiV1V0VTNSaGRHVXgNCklUQWZCZ05WQkFvTUdFbHVkR1Z5Ym1WMElGZHBaR2RwZEhNZ1VIUjVJRXgwWkRFUE1BMEdBMVVFQXd3R2RtbHINCmNtRnRNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQW45UGFzZkxTZTBuN0dHZjgNCjdDbDRQVitWdmVHSm9STUMrNXFGOFk5Z2FxMnFmUWJnQUV6L2lvWlVWeDBDcHgyeUp5Sy8xLy9VNGl2bU9qb2wNCnhabndwd0ppQXpENW96cDhMeHRQOVNzQ1FMQW9GeCt5SzkrTGhrTTVhbEpzQk1ES2Rza3Q1cmo4OERNcTdlR2oNCjBLcm5rOUpnaloyNkxIRkl2a1hUWHk1ZmlxQmhSU0VmWXZNV01qSkFNaUVSdmxuU3pBUlN0T2tGWkRiWGtuZE8NCmdHNXN0MXY0WTVSUzJCWTZDb0xLL2ovb3NBWlk4Q0x5eXlkUnduMXBMend3ZWVZYitubHBzcGxCdldST05zWEgNCjJTdjkrTG1PdGZlT2pYZlM5eGxpdStPelByYTJYbVJXSUdJMTFJVFJkd3FCdnJZY1RIL0NyWmlwRHNHbm84UHkNCjZtR0tZd0lEQVFBQm9BQXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnRUJBRjYrZnhJeHNXc29jdWpSajU1OFNZQ0oNCk5jS3MwWGZyZXcxQWF4TldkOW8yenVtR2xvRlVWdFRnaGRITDBzMndFdzBoZzdSbURxbWhXQ0xvaUdjM0RSMmUNCmpLdjVyZXA0dHVQcm1HS1pGVENkZTk2S0V3VUJPT2FZdGZXUUdXd2pxWTF2anV4VUwzNEtjR2d6MFJkd3p6NnENClJHQ2tSRlE5V25SOUNiMEFnSDVNRkNWZ0FoTEUwMVBUOStwaGN0SW9BTHAvNll0M3FrTjhYbjUzTFJpZVdCbWcNCjgvWmpUTndLRFJnUzcwZ3RMNGN3dWk4V09LVFEya1NtbHdFQldPU3VPNTFxTXlVbm9ZOVI1bVZkZHZwUk4ySmUNCnQrUlE3NWtFRVIyWlliRHdqMmNKdE9sRXloZSt4OEhmUUN1N3N1Wjk1MWVDamtNaWVwQUltTFpkR2NReWtPbz0NCi0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQ0K
  signerName: kubernetes.io/kube-apiserver-client
  expirationSeconds: 86400  # one day
  usages:
  - client auth
EOF
```

```
kubectl get csr
kubectl certificate approve <certificate-signing-request-name>
kubectl certificate deny <certificate-signing-request-name>

kubectl get csr vikram -o jsonpath='{.status.certificate}'| base64 -d > vikram.crt

```

## Add to Kubeconfig
```
kubectl config set-credentials vikram --client-key=vikram.key --client-certificate=vikram.crt --embed-certs=true

kubectl config set-context vikram --cluster=minikube --user=vikram

kubectl config use-context vikram

kubectl get po
```

## Set Authorization using RBAC
```
kubectl config use-context minikube

kubectl create role developer --verb=create --verb=get --verb=list --verb=update --resource=pods

kubectl create rolebinding developer-binding-vikram --role=developer --user=vikram

kubectl config use-context vikram

kubectl get po
kubectl get svc

kubectl auth can-i list po
kubectl auth can-i list svc

kubectl config use-context minikube
kubectl auth can-i list po --as vikram
kubectl auth can-i list svc --as vikram
```


## Signing by CA
```

Get Signed by CA
openssl x509 -req -days 360 -in vikram.csr -CA ca.crt -CAkey ca.key -out vikram.crt


curl https://kubernetes:6443/api/v1/pods \
 --key admin.key
 --cert admin.crt
 --cacert ca.crt

kubectl get pods
    --server my - kube - playground : 6443
    --client-key admin.key
    --client-certificate admin.crt
    --certificate-authority ca.crt

kubectl get roles -A --no-headers | wc -1
```