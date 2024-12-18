#  General-Commands

- **Authenticate to GCP**:

  ```bash
gcloud auth login
  ```

- **Set Default Project**:

  ```bash
gcloud config set project [PROJECT_ID]
  ```

- **List All Configurations**:

  ```bash
gcloud config list
  ```

---
#  Compute-Engine

- **Create a VM Instance**:

```bash
gcloud compute instances create [INSTANCE_NAME] \
    --zone=[ZONE] --machine-type=[MACHINE_TYPE] \
    --image-family=[IMAGE_FAMILY] --image-project=[IMAGE_PROJECT]
```

- **List VM Instances**:

  ```bash
gcloud compute instances list
  ```

- **Delete a VM Instance**:

  ```bash
gcloud compute instances delete [INSTANCE_NAME] --zone=[ZONE]
  ```

---
#  Cloud-Storage

- **Create a Storage Bucket**:

  ```bash
gcloud storage buckets create [BUCKET_NAME] --location=[LOCATION]
  ```

- **List Buckets**:

  ```bash
gcloud storage buckets list
  ```

- **Upload a File**:

  ```bash
gcloud storage cp [LOCAL_FILE_PATH] gs://[BUCKET_NAME]
  ```

- **Delete a Bucket**:

  ```bash
gcloud storage buckets delete [BUCKET_NAME]
  ```

---
#  Cloud-SQL

- **Create a SQL Instance**:

  ```bash
gcloud sql instances create [INSTANCE_NAME] --tier=[TIER] --region=[REGION]
  ```

- **List SQL Instances**:

  ```bash
gcloud sql instances list
  ```

- **Delete a SQL Instance**:

  ```bash
gcloud sql instances delete [INSTANCE_NAME]
  ```

---
#  IAM

- **Add IAM Policy Binding**:

  ```bash
gcloud projects add-iam-policy-binding [PROJECT_ID] \
    --member=[MEMBER] --role=[ROLE]
  ```

- **List IAM Policies**:

  ```bash
gcloud projects get-iam-policy [PROJECT_ID]
  ```

---
#  Networking

- **Create a VPC Network**:

  ```bash
gcloud compute networks create [NETWORK_NAME] --subnet-mode=[MODE]
  ```

- **List VPC Networks**:

  ```bash
gcloud compute networks list
 ```

---

#  Monitoring-and-Logging

- **View Logs**:

  ```bash
gcloud logging read "logName=[LOG_NAME]"
  ```

- **List Log Sinks**:

  ```bash
gcloud logging sinks list
  ```

---
#  Kubernetes-Engine

- **Create a GKE Cluster**:

  ```bash
gcloud container clusters create [CLUSTER_NAME] --zone=[ZONE]
  ```

- **Get Credentials for a Cluster**:

  ```bash
gcloud container clusters get-credentials [CLUSTER_NAME] --zone=[ZONE]
  ```

- **List GKE Clusters**:

  ```bash
gcloud container clusters list
  ```

---
#  Additional Resources

- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference)