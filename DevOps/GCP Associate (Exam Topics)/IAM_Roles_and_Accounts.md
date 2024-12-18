
## Key IAM Roles

### Compute Engine

- **Compute Admin**: Full control over Compute Engine resources.
```
roles/compute.admin
```

- **Compute Viewer**: Read-only access to Compute Engine resources.

```
roles/compute.viewer
```

- **Instance Admin**: Manage instances without access to sensitive data.

```
roles/compute.instanceAdmin.v1
```


### Storage

- **Storage Admin**: Full control over Cloud Storage resources.

```
roles/storage.admin
```

- **Storage Object Admin**: Manage objects in storage buckets.

```
roles/storage.objectAdmin
```

- **Storage Viewer**: Read-only access to storage buckets and objects.

```
roles/storage.viewer
```


### BigQuery

- **BigQuery Admin**: Full control over BigQuery resources.

```
roles/bigquery.admin
```

- **BigQuery Data Viewer**: View data and metadata.

```
roles/bigquery.dataViewer
```

- **BigQuery Job User**: Run queries and create jobs.

```
roles/bigquery.jobUser
```


### Networking

- **Network Admin**: Full control over networking resources.

```
roles/compute.networkAdmin
```

- **Security Admin**: Manage firewall rules and SSL certificates.

```
roles/compute.securityAdmin
```


## Common Service Accounts

### Compute Engine

- **Default Compute Engine Service Account**: Used by Compute Engine and GKE.

```
[PROJECT_NUMBER]-compute@developer.gserviceaccount.com
```


### Cloud SQL

- **Cloud SQL Service Account**: Manages Cloud SQL instances.

```
service-[PROJECT_NUMBER]@gcp-sa-cloud-sql.iam.gserviceaccount.com
```


### Cloud Storage

- **Storage Transfer Service Account**: Performs storage transfer operations.

```
service-[PROJECT_NUMBER]@gcp-sa-storage-transfer.iam.gserviceaccount.com
```


### Kubernetes Engine

- **GKE Service Account**: Manages Kubernetes clusters.

```
service-[PROJECT_NUMBER]@container-engine-robot.iam.gserviceaccount.com
```


---

## Best Practices

- Use the principle of **least privilege**: Assign roles with only the permissions necessary for the job.
- Regularly audit roles and service accounts to ensure compliance with security policies.
- Use **custom roles** when predefined roles don't meet specific needs.
- Enable **Cloud Audit Logs** to track changes and access.

---

## Additional Resources

- [IAM Documentation](https://cloud.google.com/iam/docs)
- [Service Accounts](https://cloud.google.com/iam/docs/service-accounts)