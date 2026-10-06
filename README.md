# KAOP product architect demo

This is a two-component Kubernetes scenario for the assignment. The API serves
`/work` on port 8080. The worker calls the API through a Kubernetes Service.
The initial Deployment deliberately points the worker to port 8081, a plausible
configuration error after a service change. The worker logs real connection
failures and exits after three failed requests, producing Kubernetes restart
events. A pull request can fix the URL to `http://demo-api:8080/work`.

## Local setup

```sh
minikube start --driver=docker
minikube image build -t kaop-demo-api:local -f Dockerfile.api .
minikube image build -t kaop-demo-worker:local -f Dockerfile.worker .
kubectl apply -f k8s/demo.yaml
kubectl -n kaop-demo rollout status deployment/demo-api
kubectl -n kaop-demo get pods
kubectl -n kaop-demo logs deployment/demo-worker --previous
kubectl -n kaop-demo get events --sort-by=.metadata.creationTimestamp
```

The bad URL is intentional for the incident. For the code review workflow,
open a pull request that changes `8081` to `8080` in `k8s/demo.yaml`. Verify
the KAOP reviewer posts a comment on that actual pull request. After the
incident investigation, apply the fix and confirm the worker stays healthy.

## What remains to configure

- Grafana Cloud metrics collection and a restart alert for `kaop-demo`.
- A KAOP Kubernetes investigation agent with read-only access to this namespace.
- A KAOP incident workflow triggered by the Grafana alert.
- A KAOP GitHub integration and pull request review workflow.

Record the actual alert, workflow run, agent finding, and pull request URL
before presenting. Do not substitute screenshots of configuration for evidence
that the workflows ran.
