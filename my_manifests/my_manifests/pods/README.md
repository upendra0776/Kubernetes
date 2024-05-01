# Pods
Smallest deployable unit in Kubernetes
## Pod and Container Status
Pods have phases and conditions; containers have states. These status properties can and will be changed based on probe results.

### Pod Phases
Pod status object includes a phase field. This phase-field tells Kubernetes and us that wherein the execution cycle a pod is.

- Pending: Accepted by the cluster, containers are not set up yet.
- Running: At least one container is in a running, starting, or restarting state.
- Succeeded: All of the containers exited with a status code of zero; the pod will not be restarted.
- Failed: All containers have terminated and at least one container exited with a status code of non-zero.
- Unknown: The state of the pod can not be determined.

### Pod Conditions
As well as pod phases, there are pod conditions. These also give information about the state the pod is in.
- PodScheduled: A Node has been successfully selected to schedule the pod, and scheduling is completed.
- ContainersReady: All the containers are ready.
- Initialized: Init containers are started.
- Ready: The pod is able to serve requests; hence it needs to be included in the service and load balancers.

`We can view the pod conditions via kubectl describe pods <POD_NAME> command`


### Container States
The container has three simple states.

- Waiting: Required processes are running for a successful startup.
- Running: The container is executing.
- Terminated: Container started execution and finished by either success or failure.

`We can see the pod conditions and container states from a Pod object by issuing Kubernetes get pods <POD_NAME> -o yaml command`



