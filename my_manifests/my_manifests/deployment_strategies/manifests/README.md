
# Kubernetes deployment strategies

 
> In Kubernetes there are multiple ways to rollout a new version of an application


## 1. Recreate Strategy

Terminate the old version and release the new one

## Ramped Strategy

Release a new version on a rolling update fashion, one after the other

The ramped deployment strategy consists of slowly rolling out a version of an

application by replacing instances one after the other until all the instances

are rolled out. It usually follows the following process: with a pool of version

A behind a load balancer, one instance of version B is deployed. When the

service is ready to accept traffic, the instance is added to the pool. Then, one

instance of version A is removed from the pool and shut down.

Depending on the system taking care of the ramped deployment, you can tweak the following parameters to increase the deployment time:
- Parallelism, max batch size: Number of concurrent instances to roll out.
- Max surge: How many instances to add in addition of the current amount.
- Max unavailable: Number of unavailable instances during the rolling update  procedure.

## Blue/Green

 Release a new version alongside the old version then switch traffic
 The blue/green deployment strategy differs from a ramped deployment, version B(green) is deployed alongside version A (blue) with exactly the same amount of
 instances. After testing that the new version meets all the requirements the
 traffic is switched from version A to version B at the load balancer level.

## Canary
Release a new version to a subset of users, then proceed to a full rollout

## A/B testing
Release a new version to a subset of users in a
precise way (HTTP headers, cookie, weight, etc.). This doesn’t come out of the
box with Kubernetes, it imply extra work to setup a smarter
loadbalancing system (Istio, Linkerd, Traeffik, custom nginx/haproxy, etc).

## Shadow
Release a new version alongside the old version. Incoming

traffic is mirrored to the new version and doesn't impact the

response.
