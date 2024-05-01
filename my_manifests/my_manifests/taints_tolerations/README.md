# Taints and Tolerations

## Taint
kubectl taint nodes minikube env=test:NoSchedule

## Tolerations
tolerations:
- key: env
  operator: "Equal"
  value: test
  effect: "NoSchedule"

## Retaint
kubectl taint nodes minikube env=stag:NoSchedule --overwrite

## Untain
kubectl taint nodes minikube env=test:NoSchedule-
