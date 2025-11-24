# Image Signing

Container image signing and verification techniques.

---

## Cosign

## Installation
```bash
sudo apt install golang jq (Maanul installation is preferred)
git clone https://github.com/sigstore/cosign
cd cosign
go install ./cmd/cosign@latest
$(go env GOPATH)/bin/cosign
```
## Usage
Cosign automatically uploads the signature to your container registry
```
cosign generate-key-pair
cosign sign --key cosign.key <IMAGE> # Good to use digest instead of tag
cosign verify --key cosign.pub <IMAGE>
```
- Sample Usage
```json
cosign verify --key cosign.pub  <Redacted-Image> | jq .
## Output
Verification for <REDACTED> --
The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - The signatures were verified against the specified public key
[
  {
    "critical": {
      "identity": {
        "docker-reference": "<REDACTED>"
      },
      "image": {
        "docker-manifest-digest": "sha256:65d54d3e1edae09e8e5112ac5bf80597921d9403af5a1e901a52f18ff8634833"
      },
      "type": "cosign container image signature"
    },
    "optional": null
  }
]
```
## Cluster-Integration
In this tutorial i will be using [**connaissuer**](https://github.com/sse-secure-systems/connaisseur)
## Setup
- **Clone Repository**
```bash
git clone https://github.com/sse-secure-systems/connaisseur.git
cd connaisseu/helm
```
- **Insert Public Key to Verfiy Signed Images**
```yml
## configure Connaisseur deployment
deployment:
  replicasCount: 3
  image: securesystemsengineering/connaisseur:v2.6.4
  imagePullPolicy: IfNotPresent
## imagePullSecrets contains an optional list of Kubernetes Secrets, in Connaisseur namespace,
## that are needed to access the registry containing Connaisseur image.
## imagePullSecrets:
## - name: "my-container-secret"
  failurePolicy: Fail  # use 'Ignore' to fail open if Connaisseur becomes unavailable
## Use 'reinvocationPolicy: IfNeeded' to be called again as part of the admission evaluation if the object
## being admitted is modified by other admission plugins after the initial webhook call
## Note that if Connaisseur is invoked a second time, the policy to be applied might change in between.
## Make sure, your Connaisseur policies are set up to handle multiple mutations of the image originally
## specified in the manifest, e.g. my.private.registry/image:1.0.0 and my.private.registry/image@sha256:<hash-of-1.0.0-image>
  reinvocationPolicy: Never
  resources:
    limits:
      cpu: 1000m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  nodeSelector: {}
  tolerations: []
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
        - podAffinityTerm:
            labelSelector:
              matchExpressions:
                - key: app.kubernetes.io/instance
                  operator: In
                  values:
                    - connaisseur
            topologyKey: kubernetes.io/hostname
          weight: 100
  #annotations:  # uncomment when using Kubernetes prior v1.19
## seccomp.security.alpha.kubernetes.io/pod: runtime/default  # uncomment when using Kubernetes prior v1.19
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - ALL
    privileged: false
    readOnlyRootFilesystem: true
    runAsNonRoot: true
    runAsUser: 10001  # remove when using openshift or OKD 4
    runAsGroup: 20001  # remove when using openshift or OKD 4
    seccompProfile:  # remove when using Kubernetes prior v1.19, openshift or OKD 4
      type: RuntimeDefault  # remove when using Kubernetes prior v1.19, openshift or OKD 4
## PodSecurityPolicy is deprecated as of Kubernetes v1.21, and will be removed in v1.25
  podSecurityPolicy:
    enabled: false
    name: ["connaisseur-psp"]  # list of PSPs to use, "connaisseur-psp" is the project-provided default
  envs: {}
## Extra config
  extraContainers: []
  extraVolumes: []
  extraVolumeMounts: []

## configure Connaisseur service
service:
  type: ClusterIP
  port: 443

### VALIDATORS ###
## validators are a set of configurations (types, public keys, authentication)
## that can be used for validating one or multiple images (or image signatures).
## they are tied to their respective image(s) via the image policy below. there
## are a few handy validators pre-configured.
validators:
## static validator that allows each image
  - name: allow
    type: static
    approve: true
## static validator that denies each image
  - name: deny
    type: static
    approve: false
## the `default` validator is used if no validator is specified in image policy
  - name: default
    type: notaryv1  # or other supported validator (e.g. "cosign")
    host: notary.docker.io # configure the notary server for notaryv1 or rekor url for cosign
    trust_roots:
## # the `default` key is used if no key is specified in image policy
    #- name: default
## key: |  # enter your public key below
## -----BEGIN PUBLIC KEY-----
## <add your public key here>
## -----END PUBLIC KEY-----
    #cert: |  # in case the trust data host is using a self-signed certificate
## -----BEGIN CERTIFICATE-----
## ...
## -----END CERTIFICATE-----
    #auth:  # credentials in case the trust data requires authentication
## # either (preferred solution)
## secret_name: mysecret  # reference a k8s secret in the form required by the validator type (check the docs)
## # or (only for notaryv1 validator)
## username: myuser
## password: mypass
## pre-configured nv1 validator for public notary from Docker Hub
  - name: Keys
    type: cosign
    trust_roots:
      - name: sitech-demo
## Public Key for my own signed images
        key: |
          -----BEGIN PUBLIC KEY-----
          MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEJCMQ+AM6xerm3mIzDcalpZi7wl12
          YQMny3BJ9weP7yPPXPyNzJMgEv+dPFS6nBYXYzM9vCXCxzWjc/W7r152hg==
          -----END PUBLIC KEY-----
## public key for official docker images (https://hub.docker.com/search?q=&type=image&image_filter=official)
## !if not needed feel free to remove the key!
      - name: docker-official
        key: |
          -----BEGIN PUBLIC KEY-----
          MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEOXYta5TgdCwXTCnLU09W5T4M4r9f
          QQrqJuADP6U7g5r9ICgPSmZuRHP/1AYUfOQW3baveKsT969EfELKj1lfCA==
          -----END PUBLIC KEY-----
## public key securesystemsengineering repo including Connaisseur images
## !this key is critical for Connaisseur!
      - name: securesystemsengineering-official
        key: |
          -----BEGIN PUBLIC KEY-----
          MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEsx28WV7BsQfnHF1kZmpdCTTLJaWe
          d0CA+JOi8H4REuBaWSZ5zPDe468WuOJ6f71E7WFg3CVEVYHuoZt2UYbN/Q==
          -----END PUBLIC KEY-----

policy:
  - pattern: "docker.io/<REPO>" # Accept wildcard \*
    validator: Keys
    with:
      trust_root: sitech-demo
  - pattern: "docker.io/library/*:*"
    validator: Keys
    with:
      trust_root: docker-official
  - pattern: "k8s.gcr.io/*:*"
    validator: allow
  - pattern: "docker.io/securesystemsengineering/*:*"
    validator: Keys
    with:
      trust_root: securesystemsengineering-official

detectionMode: false

namespacedValidation:
  enabled: false
  mode: ignore  # 'ignore' or 'validate'

automaticChildApproval:
  enabled: true

logLevel: INFO
```
- **Deploy connaisseur**
```bash
kubeclt create ns connaisseur
helm upgrade --install connaisseur --values values.yaml .  -n connaisseur
```
## Pulling-Images-securely
It's always advised to pull images by digest instead of tags.
```bash
docker pull <NameSpace>/<REPO>:<TAG>@<SHA256-Digest>
## OR
docker pull <NameSpace>/<REPO>@<SHA256-Digest>
```
- Getting digest from cli
```bash
sudo apt install -y golang
go install github.com/google/go-containerregistry/cmd/crane@latest

## Usage
crane digest <REPO>
```

## GitHub Action Integration
1. Create cosign secrets
```sh
#!/bin/bash
export REPO_OWNER="zAbuQasem"
export REPO_NAME="GitOps-K8s"
export GITHUB_TOKEN="TOKEN"
export COSIGN_PASSWORD="PASSWORD"

cosign generate-key-pair github://$REPO_OWNER/$REPO_NAME
```
2. Use the following pipeline
```yaml
name: Build-Push

on:
  push

jobs:
    build-image:
      runs-on: ubuntu-latest
  
      name: build-image
      steps:
        - uses: actions/checkout@v4.1.1

        - name: Install Cosign
          uses: sigstore/cosign-installer@v3.4.0
          with:
            cosign-release: 'v2.2.3'

        - name: Set up Docker Buildx
          uses: docker/setup-buildx-action@v3
  
        - name: Login to GitHub Container Registry
          uses: docker/login-action@v3
          with:
            username: ${{ secrets.DOCKERHUB_USERNAME }}
            password: ${{ secrets.DOCKERHUB_SECRET }}
              
        - name: Build and Push container images
          uses: docker/build-push-action@v5
          id: build-and-push
          with:
            platforms: linux/amd64
            push: true
            tags: zeyadabuqasem/django

        - name: Sign image
          env:
            TAGS: zeyadabuqasem/django
            COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
            COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
            DIGEST: ${{ steps.build-and-push.outputs.digest }}
          run: |
            images=""
            for tag in ${TAGS}; do
              images+="${tag}@${DIGEST} "
            done
            cosign sign --yes --key env://COSIGN_PRIVATE_KEY ${images}
```