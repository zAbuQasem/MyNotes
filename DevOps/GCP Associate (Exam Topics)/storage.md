#  General-Notes

- **Durability**: Google Cloud Storage offers high durability by redundantly storing data across multiple locations.
- **Scalability**: Designed to handle exabytes of data, ensuring seamless scaling as your data grows.
- **Cost Optimization**: Use lifecycle management to transition data to lower-cost storage classes as it ages.

---
#  Persistent-Disk

- **Description**: High-performance block storage for Compute Engine and Google Kubernetes Engine (GKE).
- **Key Features**:
    - **Standard Persistent Disk**: Cost-effective for sequential read/write operations.
    - **SSD Persistent Disk**: Optimized for high IOPS and low latency.
    - **Balanced Persistent Disk**: Combines performance and cost-effectiveness.
- **Snapshots**: Use incremental snapshots for backup and disaster recovery.
- **Encryption**: Data is encrypted by default, ensuring security.
- [Official Documentation](https://cloud.google.com/compute/docs/disks)

---

#  Filestore

- **Description**: Fully managed NFS file servers for applications requiring shared file storage.
- **Key Features**:
    - High performance for data-intensive workloads.
    - Easy integration with Compute Engine and GKE.
- **Use Cases**:
    - Content management systems (CMS).
    - Media rendering.
    - High-performance computing (HPC).
- [Official Documentation](https://cloud.google.com/filestore/docs)

---
#  Cloud-Storage

- **Description**: Object storage service for unstructured data.
- **Storage Classes**:
    - **Standard**: For frequently accessed data.
    - **Nearline**: Cost-effective for data accessed less than once a month.
    - **Coldline**: Suitable for disaster recovery and infrequent access.
    - **Archive**: Lowest-cost storage for long-term retention of rarely accessed data.
- **Key Features**:
    - Global accessibility with low latency.
    - Built-in security with encryption at rest and in transit.
    - Lifecycle management to optimize costs.
- **Use Cases**:
    - Backup and archival.
    - Content delivery.
    - Big data analytics.
- [Official Documentation](https://cloud.google.com/storage/docs)

---
#  Additional-Resources

- [Choosing a Storage Option](https://cloud.google.com/storage-options)
- [Storage Pricing Details](https://cloud.google.com/pricing/storage)