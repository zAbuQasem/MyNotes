## Question-24

#deployments

You have a project for your App Engine application that serves a development environment. The required testing has succeeded and you want to create a new project to serve as your production environment. What should you do?  

- ***A. Use gcloud to create the new project, and then deploy your application to the new project. Most Voted***
- B. Use gcloud to create the new project and to copy the deployed application to the new project.
- C. Create a Deployment Manager configuration file that copies the current App Engine deployment into a new project.
- D. Deploy your application again using gcloud and specify the project parameter with the new project name to create the new project.

---
## Question-26 

#iam

You need to set up permissions for a set of Compute Engine instances to enable them to write data into a particular Cloud Storage bucket. You want to follow  
Google-recommended practices. What should you do?  

- A. Create a service account with an access scope. Use the access scope 'https://www.googleapis.com/auth/devstorage.write_only'.
- B. Create a service account with an access scope. Use the access scope 'https://www.googleapis.com/auth/cloud-platform'.
- ***C. Create a service account and add it to the IAM role 'storage.objectCreator' for that bucket. Most Voted***
- D. Create a service account and add it to the IAM role 'storage.objectAdmin' for that bucket.

---
# Question-32

#monitoring

You need to monitor resources that are distributed over different projects in Google Cloud Platform. You want to consolidate reporting under the same Stackdriver  
Monitoring dashboard. What should you do?  

- A. Use Shared VPC to connect all projects, and link Stackdriver to one of the projects.
- B. For each project, create a Stackdriver account. In each project, create a service account for that project and grant it the role of Stackdriver Account Editor in all other projects.
- ***C. Configure a single Stackdriver account, and link all projects to the same account. Most Voted***
- D. Configure a single Stackdriver account for one of the projects. In Stackdriver, create a Group and add the other project names as criteria for that Group.
### Explanation:

1. **Single Stackdriver (Cloud Monitoring) Workspace**:
    - Google Cloud’s **Stackdriver Monitoring** (now called Cloud Monitoring) allows you to monitor resources across multiple projects by creating a **single Workspace**.
    - You can **link multiple projects** to the same Cloud Monitoring Workspace, enabling centralized monitoring and reporting.
2. **How It Works**:
    - Choose a primary project to host the **Workspace**.
    - Link the additional GCP projects (containing the distributed resources) to this Workspace.
    - All metrics, dashboards, and alerts can then be managed and viewed centrally.
3. **Benefits**:
    - A single Workspace provides a **consolidated view** of resources across projects.
    - It avoids creating unnecessary accounts or roles.
    - Simplifies monitoring setup and management.

### Why Not the Other Options?

- **A. Use Shared VPC and link Stackdriver to one of the projects**:
    - Shared VPC is for networking, not for consolidating monitoring data. Linking Stackdriver to a single project doesn’t automatically gather metrics across multiple projects.
- **B. Create a Stackdriver account per project and service accounts**:
    - Creating separate Stackdriver accounts is inefficient and unnecessarily complex. There’s no need to grant Stackdriver roles across all projects.
- **D. Create a Group and add project names as criteria**:
    - Stackdriver Groups help organize resources **within** a Workspace but do not consolidate monitoring data across projects. A single Workspace is still required to centralize metrics.

---

## Question #37

#deployments 

You created a Google Cloud Platform project with an App Engine application inside the project. You initially configured the application to be served from the us- central region. Now you want the application to be served from the asia-northeast1 region. What should you do?  

- A. Change the default region property setting in the existing GCP project to asia-northeast1.
- B. Change the region property setting in the existing App Engine application from us-central to asia-northeast1.
- C. Create a second App Engine application in the existing GCP project and specify asia-northeast1 as the region to serve your application.
- ***D. Create a new GCP project and create an App Engine application inside this new project. Specify asia-northeast1 as the region to serve your application.***
### Explanation:

1. **App Engine Region Selection**:
    - The region for an App Engine application is **immutable** and cannot be changed once the application is created.
    - You cannot move an App Engine app from one region (e.g., `us-central`) to another region (e.g., `asia-northeast1`).
2. **Recommended Action**:
    - To serve the application from a different region, you must **create a new App Engine application** in a new Google Cloud Platform project.
    - During creation, specify the desired region (`asia-northeast1`).
3. **Why a New Project?**:
    - A GCP project can have **only one App Engine application**.
    - Since the existing project already has an App Engine app in `us-central`, you cannot create a second one in the same project.

### Why Not the Other Options?

- **A. Change the default region property setting in the existing GCP project**:
    - The region of an App Engine application cannot be changed after creation.
- **B. Change the region property setting in the existing App Engine application**:
    - The App Engine region is immutable and cannot be updated.
- **C. Create a second App Engine application in the existing GCP project**:
    - A GCP project can contain **only one App Engine application**.

---
## Question-45

#deployments 

You recently deployed a new version of an application to App Engine and then discovered a bug in the release. You need to immediately revert to the prior version of the application. What should you do?  

- A. Run gcloud app restore.
- B. On the App Engine page of the GCP Console, select the application that needs to be reverted and click Revert.
- ***C. On the App Engine Versions page of the GCP Console, route 100% of the traffic to the previous version.***
- D. Deploy the original version as a separate application. Then go to App Engine settings and split traffic between applications so that the original version serves 100% of the requests.

Option A is wrong as gcloud app restore was used for backup and restore and has been deprecated.Option B is wrong as there is no application revert functionality available.Option D is wrong as App Engine maintains version and need not be redeployed.

---
## Question-46

#deployments 

You deployed an App Engine application using gcloud app deploy, but it did not deploy to the intended project. You want to find out why this happened and where the application deployed. What should you do?  

- A. Check the app.yaml file for your application and check project settings.
- B. Check the web-application.xml file for your application and check project settings.
- C. Go to Deployment Manager and review settings for deployment of applications.
- ***D. Go to Cloud Shell and run gcloud config list to review the Google Cloud configuration used for deployment.***]
### Explanation:

1. **`gcloud config list`**:
    - This command displays the current **Google Cloud SDK configuration**, including:
- **Active project**: The project where commands, like `gcloud app deploy`, are executed.
- Account and other configurations.
    - If the application was deployed to the wrong project, it’s likely because the active project setting was incorrect during deployment.
2. **Why This Happens**:
    - The `gcloud` CLI uses the **active project** in the configuration for deployments.
    - If no project is explicitly specified in the command (e.g., `--project` flag), the active project in the configuration is used.
3. **How to Resolve**:
	- Run the following to view your configuration:
```bash
gcloud config list
```

- Check the `project` field under the **[core]** section to confirm where the app was deployed.

- If needed, set the correct project:
```bash
gcloud config set project PROJECT_ID
```

### Why Not the Other Options?

- **A. Check the app.yaml file for your application and check project settings**:
	- The `app.yaml` file does not specify the project for deployment; the project comes from `gcloud` configuration or the `--project` flag.
- **B. Check the web-application.xml file for your application and check project settings**:
	- This file is not relevant to App Engine deployments.
- **C. Go to Deployment Manager and review settings for deployment**:
    - Deployment Manager is not used for deploying App Engine applications. `gcloud app deploy` is the correct command.

---

## Question-58

#deployments 

You are building an application that stores relational data from users. Users across the globe will use this application. Your CTO is concerned about the scaling requirements because the size of the user base is unknown. You need to implement a database solution that can scale with your user growth with minimum configuration changes. Which storage solution should you use?  

- A. Cloud SQL
- ***B. Cloud Spanner***
- C. Cloud Firestore
- D. Cloud Datastore

### Explanation:

1. **Global Scalability with Relational Data**:
    - **Cloud Spanner** is a fully managed, globally distributed, horizontally scalable **relational database**. It is designed to handle massive user growth with minimal configuration changes.
    - It supports strong consistency, SQL queries, and schemas, making it ideal for applications that require relational data storage.
2. **Reasons to Choose Cloud Spanner**:
    - **Scalability**: Scales seamlessly across regions and handles high throughput and low latency for users worldwide.
    - **Global Distribution**: Data is replicated across multiple regions to ensure availability and global access.
    - **Relational Database Features**: Full SQL capabilities with ACID transactions.
    - **Minimal Configuration Changes**: Automatically handles replication, sharding, and scaling without developer intervention.

---
### Why Not the Other Options?

- **A. Cloud SQL**:
    - While Cloud SQL is a managed relational database, it is not designed for global scaling. It is better suited for smaller, single-region use cases or moderate workloads.
- **C. Cloud Firestore**:
    - Cloud Firestore is a NoSQL document database and not designed for relational data. It is better suited for semi-structured or hierarchical data, not structured relational data.
- **D. Cloud Datastore**:
    - Cloud Datastore is also a NoSQL database and does not support relational schemas or SQL queries. It is suitable for structured or hierarchical data, not relational data.

---
## Question-59

#billing

You are the organization and billing administrator for your company. The engineering team has the Project Creator role on the organization. You do not want the engineering team to be able to link projects to the billing account. Only the finance team should be able to link a project to a billing account, but they should not be able to make any other changes to projects. What should you do?  

- ***A. Assign the finance team only the Billing Account User role on the billing account.***
- B. Assign the engineering team only the Billing Account User role on the billing account.
- C. Assign the finance team the Billing Account User role on the billing account and the Project Billing Manager role on the organization.
- D. Assign the engineering team the Billing Account User role on the billing account and the Project Billing Manager role on the organization.

### Explanation:

1. **Role Responsibilities**:
    - **Billing Account User**: This role allows users to link or unlink projects to/from the billing account. By assigning this role **only to the finance team**, you ensure that only the finance team can perform this action.
    - **Project Creator**: The engineering team can create projects, but without the **Billing Account User** or **Project Billing Manager** roles, they cannot link those projects to the billing account.
2. **Why This Works**:
    - By limiting the **Billing Account User** role to the finance team, you restrict the ability to link projects to the billing account.
    - The engineering team retains the ability to create projects (as they have the **Project Creator** role) but cannot link those projects to the billing account.

### Why Not the Other Options?

- **B. Assign the engineering team only the Billing Account User role on the billing account**:
    
    - This would allow the engineering team to link projects to the billing account, violating the requirement that only the finance team should have this ability.
- **C. Assign the finance team the Billing Account User role on the billing account and the Project Billing Manager role on the organization**:
    
    - The **Project Billing Manager** role on the organization is unnecessary. The **Billing Account User** role alone is sufficient to allow the finance team to link projects to the billing account.
- **D. Assign the engineering team the Billing Account User role on the billing account and the Project Billing Manager role on the organization**:
    
    - This would allow the engineering team to link projects to the billing account, which is explicitly against the requirements.
---
## Question-64

#deployments 

You want to deploy an application on Cloud Run that processes messages from a Cloud Pub/Sub topic. You want to follow Google-recommended practices. What should you do?  

- A. 1. Create a Cloud Function that uses a Cloud Pub/Sub trigger on that topic. 2. Call your application on Cloud Run from the Cloud Function for every message.
- B. 1. Grant the Pub/Sub Subscriber role to the service account used by Cloud Run. 2. Create a Cloud Pub/Sub subscription for that topic. 3. Make your application pull messages from that subscription.
- ***C. 1. Create a service account. 2. Give the Cloud Run Invoker role to that service account for your Cloud Run application. 3. Create a Cloud Pub/Sub subscription that uses that service account and uses your Cloud Run application as the push endpoint.***
- D. 1. Deploy your application on Cloud Run on GKE with the connectivity set to Internal. 2. Create a Cloud Pub/Sub subscription for that topic. 3. In the same Google Kubernetes Engine cluster as your application, deploy a container that takes the messages and sends them to your application.

### Explanation:

This approach aligns with **Google-recommended practices** for deploying applications on Cloud Run that process messages from a Cloud Pub/Sub topic.

1. **Service Account for Secure Communication**:
    - Create a dedicated service account to ensure secure communication between Cloud Pub/Sub and your Cloud Run service.
    - Grant the **Cloud Run Invoker role** to this service account, allowing Pub/Sub to invoke your Cloud Run service.
2. **Cloud Pub/Sub Push Subscription**:
    - Set up a Pub/Sub subscription for the topic and configure it to use your Cloud Run application's URL as the push endpoint. Pub/Sub will push messages to your Cloud Run service automatically.
3. **Efficient Processing with Push**:
    - Using a **push subscription** eliminates the need for your application to pull messages, reducing complexity and ensuring low latency message processing.


### Why Not the Other Options?

- **A. Use a Cloud Function with a Pub/Sub trigger to invoke Cloud Run**:
    - This introduces unnecessary complexity and latency. Pub/Sub can directly push messages to Cloud Run without requiring a Cloud Function as an intermediary.
- **B. Grant Pub/Sub Subscriber role and pull messages from the subscription**:
    - While pulling messages is possible, it is **not the recommended practice** for Cloud Run. Using a push subscription simplifies the setup and ensures immediate message delivery.
- **D. Use Cloud Run on GKE with an internal connectivity configuration**:
    - Deploying Cloud Run on GKE is overly complex and unnecessary for this use case. Standard Cloud Run with a push subscription is simpler, more scalable, and cost-effective.
---
## Question-66

#billing 

Your company has an existing GCP organization with hundreds of projects and a billing account. Your company recently acquired another company that also has hundreds of projects and its own billing account. You would like to consolidate all GCP costs of both GCP organizations onto a single invoice. You would like to consolidate all costs as of tomorrow. What should you do?  

- ***A. Link the acquired company's projects to your company's billing account.***
- B. Configure the acquired company's billing account and your company's billing account to export the billing data into the same BigQuery dataset.
- C. Migrate the acquired company's projects into your company's GCP organization. Link the migrated projects to your company's billing account.
- D. Create a new GCP organization and a new billing account. Migrate the acquired company's projects and your company's projects into the new GCP organization and link the projects to the new billing account.

To me, A looks correct. projects are linked to another organization as well in the acquired company so migrating would need google cloud support. we can not do ourselves. however, we can link other company projects to an existing billing account to generate total cost. https://medium.com/google-cloud/google-cloud-platform-cross-org-billing-41c5db8fefa6

---

## Question-68

#monitoring #billing 

For analysis purposes, you need to send all the logs from all of your Compute Engine instances to a BigQuery dataset called platform-logs. You have already installed the Cloud Logging agent on all the instances. You want to minimize cost. What should you do?  

- A. 1. Give the BigQuery Data Editor role on the platform-logs dataset to the service accounts used by your instances. 2. Update your instances' metadata to add the following value: logs-destination: bq://platform-logs.
- B. 1. In Cloud Logging, create a logs export with a Cloud Pub/Sub topic called logs as a sink. 2. Create a Cloud Function that is triggered by messages in the logs topic. 3. Configure that Cloud Function to drop logs that are not from Compute Engine and to insert Compute Engine logs in the platform-logs dataset.
- ***C. 1. In Cloud Logging, create a filter to view only Compute Engine logs. 2. Click Create Export. 3. Choose BigQuery as Sink Service, and the platform-logs dataset as Sink Destination.***
- D. 1. Create a Cloud Function that has the BigQuery User role on the platform-logs dataset. 2. Configure this Cloud Function to create a BigQuery Job that executes this query: INSERT INTO dataset.platform-logs (timestamp, log) SELECT timestamp, log FROM compute.logs WHERE timestamp > DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) 3. Use Cloud Scheduler to trigger this Cloud Function once a day.

### Explanation:

This approach aligns with **Google-recommended practices** and is the simplest and most cost-effective way to send Compute Engine logs to a BigQuery dataset.

1. **Filtering Logs**:
    
    - Use **Cloud Logging's export feature** to filter logs specific to Compute Engine instances. This ensures that only relevant logs are sent to BigQuery, minimizing unnecessary data processing and storage costs.
2. **BigQuery as a Sink**:
    
    - Select **BigQuery** as the sink destination and specify the `platform-logs` dataset. This automatically sends the filtered logs to the specified dataset for analysis.
3. **Cost Efficiency**:
    
    - By directly exporting filtered logs to BigQuery, you avoid additional costs associated with intermediary services like Cloud Pub/Sub or Cloud Functions.

### Why Not the Other Options?

- **A. Update instances' metadata to direct logs to BigQuery**:
    
    - There is no feature in GCP that allows logs to be sent to BigQuery by simply updating instance metadata. This option is not valid.
- **B. Use Cloud Pub/Sub and Cloud Functions**:
    
    - This adds unnecessary complexity and cost. Logs can be exported directly from Cloud Logging to BigQuery without needing Cloud Pub/Sub or a Cloud Function.
- **D. Use Cloud Functions and Cloud Scheduler**:
    
    - This approach is unnecessarily complicated and inefficient. Direct export from Cloud Logging to BigQuery is simpler and more cost-effective.
---
## Question-69

#deployments 

You are using Deployment Manager to create a Google Kubernetes Engine cluster. Using the same Deployment Manager deployment, you also want to create a  
DaemonSet in the kube-system namespace of the cluster. You want a solution that uses the fewest possible services. What should you do?  

- ***A. Add the cluster's API as a new Type Provider in Deployment Manager, and use the new type to create the DaemonSet.***
- B. Use the Deployment Manager Runtime Configurator to create a new Config resource that contains the DaemonSet definition.
- C. With Deployment Manager, create a Compute Engine instance with a startup script that uses kubectl to create the DaemonSet.
- D. In the cluster's definition in Deployment Manager, add a metadata that has kube-system as key and the DaemonSet manifest as value.
### Explanation:

1. **Type Provider in Deployment Manager**:
    - A **Type Provider** allows Deployment Manager to interact with additional APIs, such as the Kubernetes API.
    - By adding the Kubernetes API as a new Type Provider, Deployment Manager can manage Kubernetes resources (like DaemonSets) directly as part of the deployment.
2. **Fewest Possible Services**: 
    - This approach keeps the solution clean and integrates everything within Deployment Manager, avoiding the need for extra services or scripts.
    - It allows Deployment Manager to handle both the GKE cluster creation and the DaemonSet deployment. 
3. **How It Works**:
    - After defining the cluster creation in Deployment Manager, you define the DaemonSet as a resource using the custom Type Provider linked to the Kubernetes API.
    - Deployment Manager then creates the cluster and deploys the DaemonSet in the specified namespace.

### Example Configuration:

- **Create a Type Provider for Kubernetes API**
	- You need to configure the **Kubernetes API** as a custom **Type Provider** in Deployment Manager.
	- Create a file called `k8s-type-provider.yaml`:
```yml
name: kubernetes-type-provider
type: typeProvider
properties:
  descriptorUrl: https://$(ref.gke-cluster.endpoint)/swagger.json
  options:
    validationOptions:
      schemaValidation: IGNORE_WITH_WARNINGS
```
- **Define the Deployment Manager Configuration**
	- Create a configuration file `deployment.yaml` that defines both the GKE cluster and the DaemonSet.
```yml
resources:
- name: gke-cluster
  type: container.v1.cluster
  properties:
    zone: us-central1-a
    cluster:
      name: example-cluster
      initialClusterVersion: "1.30"
      nodePools:
      - name: default-pool
        initialNodeCount: 1
        config:
          machineType: n1-standard-1
          oauthScopes:
          - https://www.googleapis.com/auth/devstorage.read_only
          - https://www.googleapis.com/auth/logging.write
          - https://www.googleapis.com/auth/monitoring

- name: daemonset
  type: kubernetes-type-provider:apps/v1:namespaces/kube-system/DaemonSet
  properties:
    metadata:
      name: example-daemonset
      namespace: kube-system
    spec:
      selector:
        matchLabels:
          app: example-daemon
      template:
        metadata:
          labels:
            app: example-daemon
        spec:
          containers:
          - name: example-container
            image: nginx:1.17
            ports:
            - containerPort: 80s
```
- Deploy the configuration using Deployment Manager:
```bash
# Step 1: Deploy the Type Provider
gcloud deployment-manager deployments create k8s-type-provider \
    --config k8s-type-provider.yaml

# Step 2: Deploy the GKE cluster and DaemonSet
gcloud deployment-manager deployments create gke-deployment \
    --config deployment.yaml
```


### Why Not the Other Options?

- **B. Use the Deployment Manager Runtime Configurator**:
    - Runtime Configurator is not designed for creating Kubernetes resources like DaemonSets. It is primarily used for dynamic configurations and runtime variables.
- **C. Create a Compute Engine instance with a startup script**:
    - While this could work, it adds unnecessary complexity and introduces additional services (Compute Engine). It is not efficient or recommended.
- **D. Add metadata to the cluster definition in Deployment Manager**:
    - Metadata in a Deployment Manager cluster definition cannot be used to directly create Kubernetes resources like DaemonSets. This option is invalid.
---
