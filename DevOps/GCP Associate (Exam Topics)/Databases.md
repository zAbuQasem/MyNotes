# General-Notes

- Placeholder for general notes and tips. Expand as needed.

---

# Cloud-SQL

- **Point-in-Time Recovery**: Enabling binary logging in Cloud SQL allows point-in-time recovery, which is essential for relational data management in single geographic locations.
- **Cost-Effective for Small Datasets**: Compared to Cloud Spanner, Cloud SQL is more cost-effective for smaller datasets.
- **Supported Databases**: Cloud SQL supports MySQL, PostgreSQL, and SQL Server.
- **Automated Backups**: Easily schedule automated backups to ensure data recovery options.
- **High Availability**: Provides regional high-availability options with automatic failover.
- [Official Documentation](https://cloud.google.com/sql/docs/mysql/backup-recovery/restore#tips-pitr)

---

# Cloud-Spanner

- **Global Scalability**: Designed for globally distributed databases with low-latency access.
- **Strong Consistency**: Guarantees strong consistency across regions.
- **Horizontal Scalability**: Scales horizontally without manual sharding.
- **Use Cases**: Ideal for financial systems, inventory management, and large-scale transactional applications.
- **Integration**: Supports integrations with BigQuery for analytical workloads.
- [Official Documentation](https://cloud.google.com/spanner/docs)

---

# Cloud-Storage

- **Storage Classes**:
    - **Standard**: High-performance storage for frequently accessed data.
    - **Nearline**: Cost-effective for data accessed less than once a month.
    - **Coldline**: Ideal for disaster recovery and infrequently accessed data.
    - **Archive**: Lowest-cost option for long-term storage of rarely accessed data.
- **Security**: Provides encryption at rest and in transit.
- **Lifecycle Management**: Automate data retention policies to reduce costs.
- **Integration**: Integrates seamlessly with other Google Cloud services like BigQuery and Dataflow.
- [Official Documentation](https://cloud.google.com/storage/docs)

---

# BigQuery

- **On-Demand Pricing**: Charges are based on the number of bytes processed ("bytes read") by queries.
    - Applicable whether data is stored in BigQuery or in external sources like Cloud Storage, Drive, or Cloud Bigtable.
    - Usage-based pricing model without upfront commitments.
- **Flat-Rate Pricing**: Provides predictable monthly costs for query usage.
- **Serverless Data Warehouse**: Eliminates the need for infrastructure management.
- **Advanced Analytics**: Supports AI and ML workflows with built-in SQL functions.
- **Integration**: Works with Data Studio, Looker, and other visualization tools.
- [Official Documentation](https://cloud.google.com/bigquery/docs)

---

# Firestore

- **Flexible Database**: Cloud Firestore is a NoSQL document database.
- **Real-Time Updates**: Supports real-time synchronization for mobile and web apps.
- **Scalable**: Automatically scales to handle high-traffic applications.
- **Integration**: Works seamlessly with Firebase and Google Cloud services.
- **Use Cases**: Ideal for user profile management, real-time messaging, and gaming apps.
- [Official Documentation](https://cloud.google.com/firestore/docs)

---

# Cloud-Bigtable

- **Wide-Column Database**: Designed for low-latency and high-throughput workloads.
- **Scalable**: Handles petabyte-scale datasets with ease.
- **Use Cases**: Suitable for time-series data, IoT data, and financial data analysis.
- **Integration**: Integrates with BigQuery for analytics and Dataflow for ETL.
- [Official Documentation](https://cloud.google.com/bigtable/docs)

---

# Persistent-Disk

- **Block Storage**: Provides high-performance block storage for Compute Engine and GKE.
- **Types**:
    - **Standard Persistent Disk**: Cost-effective for sequential read/write operations.
    - **SSD Persistent Disk**: High-performance storage for IOPS-intensive applications.
    - **Balanced Persistent Disk**: Optimal balance of performance and cost.
- **Snapshot Support**: Allows incremental backups for disaster recovery.
- [Official Documentation](https://cloud.google.com/compute/docs/disks)

---

# Filestore

- **Managed File Storage**: Provides a fully managed NFS service.
- **High Performance**: Ideal for applications requiring shared file storage.
- **Use Cases**: Suitable for media rendering, HPC workloads, and CMS systems.
- [Official Documentation](https://cloud.google.com/filestore/docs)