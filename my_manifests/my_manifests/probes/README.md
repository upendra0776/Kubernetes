https://nayak-saabyasachi.medium.com/kubernetes-probes-5f4c3f7d900a

# Liveness, Readiness and Startup Probes

A probe is a diagnostic performed periodically by the kubelet on a container. To perform a diagnostic, the kubelet either executes code within the container, or makes a network request
## Why Probes are needed
Kubernetes provides probes -health checks- to monitor and act on the state or condition of the pods, to make sure only healthy pods serve traffic.

Kubelet is the responsible component for running the health checks, updating the API Server with the relevant information.

The [kubelet](https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/)  uses liveness probes to know when to restart a container. For example, liveness probes could catch a deadlock, where an application is running, but unable to make progress. Restarting a container in such a state can help to make the application more available despite bugs.

The kubelet uses readiness probes to know when a container is ready to start accepting traffic. A Pod is considered ready when all of its containers are ready. One use of this signal is to control which Pods are used as backends for Services. When a Pod is not ready, it is removed from Service load balancers.

The kubelet uses startup probes to know when a container application has started. If such a probe is configured, it disables liveness and readiness checks until it succeeds, making sure those probes don't interfere with the application startup. This can be used to adopt liveness checks on slow starting containers, avoiding them getting killed by the kubelet before they are up and running.

## Probe Handlers
There are three available handlers that can cover almost any scenario.

### Exec Action(exec)
ExecAction executes a command inside the container; this also is a gateway feature that can handle anything since we can run any executable; this might be a script running several curl requests to determine the status or an executable that connects to an external dependency. Make sure that the executable does not create zombie processes.

Executes a specified command inside the container. The diagnostic is considered successful if the command exits with a status code of 0.
### TCP Socket Action(tcpSocket)
Performs a TCP check against the Pod's IP address on a specified port. The diagnostic is considered successful if the port is open. If the remote system (the container) closes the connection immediately after it opens, this counts as healthy.
TCPSocketAction Connects to a defined port to check if the port is open, mostly used for endpoints that are not talking HTTP.HTTP Get Action
### HTTP Get Action(httpGet)
Performs an HTTP GET request against the Pod's IP address on a specified port and path. The diagnostic is considered successful if the response has a status code greater than or equal to 200 and less than 400.

## Common Probe Parameters
Each type of probe has common configurable fields:

- initialDelaySeconds: Seconds after the container started and before probes start. (default: 0)
- periodSeconds: Frequency of the pod. (default: 10)
- timeoutSeconds: Timeout for the expected response. (default: 1)
- successThreshold: How many success results received to transition from failure to a healthy state. (default: 1)
- failureThreshold: How many failed results received to transition from healthy to failure state. (default: 3)
As you can see, we can configure probes in detail. For successful probe configuration, we need to analyze the requirements and dependencies of our application/microservice.

## Probes Explained

### Startup Probes
Indicates whether the application within the container is started. All other probes are disabled if a startup probe is provided, until it succeeds. If the startup probe fails, the kubelet kills the container, and the container is subjected to its restart policy. If a container does not provide a startup probe, the default state is Success.

If your process requires time to get ready, reading a file, parsing a large configuration, preparing some data, and so on, you should use Startup Probes. If the probe fails, the threshold is exceeded, it will be restarted so the operation can start over. You need to adjust initialDelaySeconds and periodSeconds accordingly to make sure the process has sufficient time to complete. Otherwise, you can find your pod in a loop of restarts.

### Readiness Probes
Indicates whether the container is ready to respond to requests. If the readiness probe fails, the endpoints controller removes the Pod's IP address from the endpoints of all Services that match the Pod. The default state of readiness before the initial delay is Failure. If a container does not provide a readiness probe, the default state is Success.

If you want to control the traffic sent to the pod, you ought to use readiness probes. Readiness Probes modify Pod Conditions: Ready to change whether the pod should be included in the service and load-balancers. When the probe succeeds enough times (threshold), it means that the pod can receive traffic, and it should be included in the service and load-balancers. If your process has the ability to take itself out of the service for maintenance, reading a large amount of data to be used for the service, etc., again, you ought to use readiness probes. So that pod can signal to kublet via readiness probe that it wants out of the service for a while.

### Liveness Probes
Indicates whether the container is running. If the liveness probe fails, the kubelet kills the container, and the container is subjected to its restart policy. If a container does not provide a liveness probe, the default state is Success.

If your container cannot crash by itself when there is an unexpected error occur, then use liveness probes. Using liveness probes can overcome some of the bugs the process might have. Kublet restarts the pod once the Liveness Probe fails.

If your process can handle these errors by exiting, you don’t need to use liveness probes; however, it is advantageous to accommodate unknown bugs until they are fixed.

Many applications running for long periods of time eventually transition to broken states, and cannot recover except by being restarted. Kubernetes provides liveness probes to detect and remedy such situations.

