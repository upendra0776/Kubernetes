# Kubernetes Deployment strategies
Official link: https://github.com/ContainerSolutions/k8s-deployment-strategies

In Kubernetes there are multiple ways to rollout a new version of an application to the cluster.

## Recreate Strategy
Terminate the old version and release the new one. Expect a downtime during the process.

## Ramped Strategy
Release a new version on a rolling update fashion, one after the other.
This strategy slowly replaces older instances one after the other with the newer instances.
You can also record the changes done to each version to make it easier to rollback.

Two parameters defines the whole rolling update strategy. The first
- Max surge: How many instances to add in addition of the current amount.
- Max unavailable: Number of instances those can be unavailable during the roll out.

## Blue/Green Strategy
Release a new version(Green) alongside the old version(Blue) and then switch traffic after testing the new version.

## Canary Strategy
Release a new version to a subset of users, then proceed to a full rollout. Usually done with percent
traffic split using Istio's CRDs or by managing with deployments/Ingress controllers that support
weighted routing.

## A/B Testing Strategy
Release a new version alongside the old version but redirect the traffic to new version only to a subset of users in a
precise way by using HTTP headers, cookies etc.  Usually done with service mesh tools like
Istio, Linkerd, Traefik, custom nginx/haproxy, etc.

## Shadow Strategy
Release a new version alongside the old version. Incoming traffic is mirrored to the new version and doesn't impact the response. Requires Istio specific CRDs.
