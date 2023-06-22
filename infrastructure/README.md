# Deploy Ditto Deploy to Cluster

Ditto-deploy requires cert-manager to pre-installed to issue a self-signing certificate.


<details><summary>Install Cert Manager if not installed
</summary>

## Install Cert-manager 

- Add helm repository
```
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

- Create a namespace for installing cert-manager
```commandline
kubectl create ns cert-manager
```

- Install Cert manager
```
helm install cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --set global.leaderElection.namespace=cert-manager \
    --set installCRDs=true \
    --set prometheus.enabled=false
```

</details>

## Deploy Ditto Deploy using Manifests

- Apply Resources
   ```commandline
    kubectl apply -f ns.yaml
    kubectl apply -f issuer.yaml
    kubectl apply -f service.yaml
   ```