## Question-24

#deployments

You have a project for your App Engine application that serves a development environment. The required testing has succeeded and you want to create a new project to serve as your production environment. What should you do?  

- ***A. Use gcloud to create the new project, and then deploy your application to the new project.
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


---
## Question-45

#deployments 

You recently deployed a new version of an application to App Engine and then discovered a bug in the release. You need to immediately revert to the prior version of the application. What should you do?  

- A. Run gcloud app restore.
- B. On the App Engine page of the GCP Console, select the application that needs to be reverted and click Revert.
- ***C. On the App Engine Versions page of the GCP Console, route 100% of the traffic to the previous version.***
- D. Deploy the original version as a separate application. Then go to App Engine settings and split traffic between applications so that the original version serves 100% of the requests.

Option A is wrong as gcloud app restore was used for backup and restore and has been deprecated.
Option B is wrong as there is no application revert functionality available.
Option D is wrong as App Engine maintains version and need not be redeployed.

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
## Question-70

#iam #deployments 

You are building an application that will run in your data center. The application will use Google Cloud Platform (GCP) services like AutoML. You created a service account that has appropriate access to AutoML. You need to enable authentication to the APIs from your on-premises environment. What should you do?  

- A. Use service account credentials in your on-premises application.
- ***B. Use gcloud to create a key file for the service account that has appropriate permissions.***
- C. Set up direct interconnect between your data center and Google Cloud Platform to enable authentication for your on-premises applications.
- D. Go to the IAM & admin console, grant a user account permissions similar to the service account permissions, and use this user account for authentication from your data center.

### Explanation:

To enable authentication to Google Cloud APIs, including AutoML, from an **on-premises environment**, the recommended approach is to use **service account key files**.

1. **Why Service Account Key Files?**
    
    - A service account is a secure identity used by applications to authenticate and interact with Google Cloud services.
    - You can generate a **key file** for the service account, which allows your on-premises application to securely authenticate with the required APIs.
2. **Steps to Generate and Use a Service Account Key File**:
    
    - Use the `gcloud` CLI to create a key file for the service account:

```bash
gcloud iam service-accounts keys create key-file.json \
    --iam-account=SERVICE_ACCOUNT_EMAIL
```

- Save the key file (`key-file.json`) securely and use it in your on-premises application to authenticate with Google Cloud services by setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key-file.json"
```
**Why This Is Recommended**:  
- Service accounts are the **standard approach** for authenticating non-interactive workloads.
- The key file provides the necessary credentials while keeping authentication secure and manageable.

### Why Not the Other Options?

- **A. Use service account credentials in your on-premises application**:
    
    - While this may seem correct, the term **"service account credentials"** is ambiguous. You must use a **service account key file**, which is explicitly addressed in Option B.
- **C. Set up direct interconnect**:
    
    - Direct Interconnect is a network connection solution and does not handle authentication. It is unnecessary for enabling authentication to APIs from on-premises environments.
- **D. Use a user account for authentication**:
    
    - This violates **Google-recommended best practices**, as user accounts are not meant for non-interactive authentication. Service accounts are the correct approach for applications.

---
## Question-71

#deployments #iam 

You are using Container Registry to centrally store your company's container images in a separate project. In another project, you want to create a Google  
Kubernetes Engine (GKE) cluster. You want to ensure that Kubernetes can download images from Container Registry. What should you do?  

- ***A. In the project where the images are stored, grant the Storage Object Viewer IAM role to the service account used by the Kubernetes nodes.***
- B. When you create the GKE cluster, choose the Allow full access to all Cloud APIs option under 'Access scopes'.
- C. Create a service account, and give it access to Cloud Storage. Create a P12 key for this service account and use it as an imagePullSecrets in Kubernetes.
- D. Configure the ACLs on each image in Cloud Storage to give read-only access to the default Compute Engine service account.

---

## Question-82

#deployments #network

Your VMs are running in a subnet that has a subnet mask of 255.255.255.240. The current subnet has no more free IP addresses and you require an additional  
10 IP addresses for new VMs. The existing and new VMs should all be able to reach each other without additional routes. What should you do?  

1. ***Use gcloud to expand the IP range of the current subnet.***
    
2. Delete the subnet, and recreate it using a wider range of IP addresses.
    
3. Create a new project. Use Shared VPC to share the current network with the new project.
    
4. Create a new subnet with the same starting IP but a wider range to overwrite the current subnet.

### Explanation:

1. **Subnet Expansion in Google Cloud**:
    
    - Google Cloud allows you to **expand the IP range of an existing subnet** without disrupting the current resources or requiring a new subnet.
    - Expanding the subnet's IP range ensures that the new and existing VMs remain in the same subnet and can communicate without additional routes.
2. **Command to Expand the Subnet**: Use the following command to expand the IP range:
```bash
gcloud compute networks subnets expand-ip-range SUBNET_NAME \
    --region=REGION \
    --prefix-length=NEW_PREFIX_LENGTH
```
- Replace `SUBNET_NAME` with the name of your current subnet.
    - Replace `REGION` with the region where your subnet resides.
    - Replace `NEW_PREFIX_LENGTH` with a smaller prefix length (e.g., `28` for a larger subnet).
- **Why Subnet Expansion Works**:
    
    - By expanding the IP range, the existing subnet is updated to include more IP addresses, ensuring all VMs (existing and new) can communicate within the same subnet.
    - This avoids the need to delete or recreate resources, minimizing disruption.


### Why Not the Other Options?

- **B. Delete the subnet, and recreate it using a wider range of IP addresses**:
    
    - Deleting the subnet would require you to reconfigure the existing VMs, causing downtime. Expanding the IP range is more efficient and non-disruptive.
- **C. Create a new project and use Shared VPC**:
    
    - Creating a new project and using Shared VPC adds unnecessary complexity. It also creates separate subnets, requiring additional routes for communication.
- **D. Create a new subnet with the same starting IP but a wider range**:
    
    - Google Cloud does not allow overlapping IP ranges for subnets in the same network. Creating a new subnet with the same starting IP would conflict with the existing subnet.
---
## Question-83

#iam 

Your organization uses G Suite for communication and collaboration. All users in your organization have a G Suite account. You want to grant some G Suite users access to your Cloud Platform project. What should you do?  

1. Enable Cloud Identity in the GCP Console for your domain.
    
2. Grant them the required IAM roles using their G Suite email address.
    
3. Create a CSV sheet with all users' email addresses. Use the gcloud command line tool to convert them into Google Cloud Platform accounts.
    
4. In the G Suite console, add the users to a special group called [[email protected]](https://www.secexams.com/cdn-cgi/l/email-protection). Rely on the default behavior of the Cloud Platform to grant users access if they are members of this group.
### Explanation:

1. **IAM and G Suite Integration**:
    - G Suite accounts (now known as Google Workspace) can be used directly as identities in Google Cloud Platform (GCP) for authentication and access management.
    - You can grant users access to GCP resources by assigning the appropriate IAM roles using their G Suite email addresses.
2. **How to Grant Access**:
    - In the GCP Console or via the `gcloud` CLI, add the user's G Suite email to the project and assign the required roles.
3. **Why This Works**:
	- G Suite accounts are natively supported in GCP, so no additional setup or configuration is required.
	- This method ensures that only the required users are granted access with the appropriate level of permissions.
### Why Not the Other Options?

- **A. Enable Cloud Identity in the GCP Console for your domain**:
    
    - Cloud Identity is used to manage users without G Suite accounts or for organizations without G Suite. Since your organization already uses G Suite, this is unnecessary.
- **C. Use a CSV sheet and convert users into GCP accounts**:
    
    - G Suite users do not need to be "converted" into GCP accounts. They are already recognized as valid identities in GCP.
- **D. Add users to a special G Suite group called `gcp-admins@your-domain.com`**:
    
    - While you can use groups to manage IAM roles, GCP does not automatically grant access to a group called `gcp-admins`. You must explicitly assign IAM roles to the group.
---
## Question-111

#iam 

Your management has asked an external auditor to review all the resources in a specific project. The security team has enabled the Organization Policy called  
Domain Restricted Sharing on the organization node by specifying only your Cloud Identity domain. You want the auditor to only be able to view, but not modify, the resources in that project. What should you do?  

1. Ask the auditor for their Google account, and give them the Viewer role on the project.
2. Ask the auditor for their Google account, and give them the Security Reviewer role on the project.
3. ***Create a temporary account for the auditor in Cloud Identity, and give that account the Viewer role on the project.***
4. Create a temporary account for the auditor in Cloud Identity, and give that account the Security Reviewer role on the project.
### Explanation:

1. **Domain Restricted Sharing Policy**:
    
    - The **Domain Restricted Sharing** policy restricts resource access to only users within your organization's **Cloud Identity domain**.
    - External auditors not in your domain cannot be granted access directly to the project without violating this policy.
2. **Solution: Temporary Cloud Identity Account**:
    
    - To comply with the policy, create a **temporary account** for the auditor within your Cloud Identity domain.
    - This allows the auditor to access resources without relaxing or violating the Domain Restricted Sharing policy.
3. **Viewer Role**:
    
    - Assign the **Viewer role** to the auditor’s temporary account. This role allows them to view (but not modify) all resources within the project, which matches the requirements.
### Why Not the Other Options?

- **A. Ask the auditor for their Google account and give them the Viewer role**:
    
    - Since the **Domain Restricted Sharing** policy is enabled, external accounts (outside your domain) cannot be granted access.
- **B. Ask the auditor for their Google account and give them the Security Reviewer role**:
    
    - Same issue as Option A: external accounts are blocked by the Domain Restricted Sharing policy.
- **D. Create a temporary Cloud Identity account and give the Security Reviewer role**:
    
    - The **Security Reviewer role** provides access to security-related resources (IAM policies, logs, etc.), but it does not meet the broader requirement of viewing **all resources**. The Viewer role is more appropriate here.
---

## Question-112

#iam 

You need to assign a Cloud Identity and Access Management (Cloud IAM) role to an external auditor. The auditor needs to have permissions to review your  
Google Cloud Platform (GCP) Audit Logs and also to review your Data Access logs. What should you do?  

1. Assign the auditor the IAM role roles/logging.privateLogViewer. Perform the export of logs to Cloud Storage. 
2. Assign the auditor the IAM role roles/logging.privateLogViewer. Direct the auditor to also review the logs for changes to Cloud IAM policy.
3. Assign the auditor's IAM user to a custom role that has logging.privateLogEntries.list permission. Perform the export of logs to Cloud Storag.
4. Assign the auditor's IAM user to a custom role that has logging.privateLogEntries.list permission. Direct the auditor to also review the logs for changes to Cloud IAM policy.

### Explanation:

1. **Role for Accessing Audit Logs**:
    
    - The `roles/logging.privateLogViewer` role provides access to **all audit logs**, including **Data Access logs**, which are private and require elevated permissions.
    - This role ensures the auditor can view **Admin Activity logs**, **System logs**, and **Data Access logs**, covering the required scope.
2. **Changes to Cloud IAM Policies**:
    
    - **Admin Activity logs** include changes to IAM policies, making them essential for security and compliance reviews.
    - By reviewing these logs, the auditor can verify changes made to IAM roles and permissions.
3. **Why No Need for Export**:
    
    - Direct access to logs via the `roles/logging.privateLogViewer` role eliminates the need to export logs to Cloud Storage or create custom roles.

### Why Not the Other Options?

- **A. Assign `roles/logging.privateLogViewer` and export logs to Cloud Storage**:
    
    - Exporting logs is unnecessary. The `roles/logging.privateLogViewer` role already allows the auditor to access the logs directly.
- **C. Create a custom role with `logging.privateLogEntries.list` and export logs**:
    
    - Creating a custom role is redundant when the predefined `roles/logging.privateLogViewer` role already provides the required permissions.
    - Exporting logs adds unnecessary complexity.
- **D. Create a custom role with `logging.privateLogEntries.list`**:
    
    - Similar to Option C, creating a custom role is unnecessary, and the predefined role (`roles/logging.privateLogViewer`) is sufficient for the auditor's needs.
---
## Question-116

#iam

You are configuring service accounts for an application that spans multiple projects. Virtual machines (VMs) running in the web-applications project need access to BigQuery datasets in crm-databases-proj. You want to follow Google-recommended practices to give access to the service account in the web-applications project. What should you do?  

1. Give project owner for web-applications appropriate roles to crm-databases-proj.
2. Give project owner role to crm-databases-proj and the web-applications project.
3. Give project owner role to crm-databases-proj and bigquery.dataViewer role to web-applications.
4. ***Give bigquery.dataViewer role to crm-databases-proj and appropriate roles to web-applications.***

### Explanation:

1. **Service Accounts for Cross-Project Access**:
    - When an application spans multiple projects, service accounts are used to securely grant specific permissions across projects.
    - The virtual machines (VMs) in the `web-applications` project need access to BigQuery datasets in the `crm-databases-proj`. This access should follow the **principle of least privilege**.
2. **Steps to Implement Cross-Project Access**:
    - **Grant the `bigquery.dataViewer` role**:
        - Assign the `bigquery.dataViewer` role in the **crm-databases-proj** project to the **service account used by the VMs in the web-applications project**.
3. **Why This Works**:
    - The `bigquery.dataViewer` role provides read access to BigQuery datasets, allowing the VMs to query the data without write permissions.
    - This approach aligns with Google-recommended practices by granting the minimum required permissions for the service account to function effectively.

### Why Not the Other Options?

- **1. Give project owner for `web-applications` appropriate roles to `crm-databases-proj`**:
    - The **Project Owner** role provides broad, unrestricted access and is excessive for this use case. This violates the principle of least privilege.
- **2. Give project owner role to both projects**:
    - Assigning the **Project Owner** role to both projects is highly insecure and unnecessary. It provides administrative permissions far beyond what's needed.
- **3. Give project owner role to `crm-databases-proj` and `bigquery.dataViewer` to `web-applications`**:
    - Granting the **Project Owner** role to `crm-databases-proj` is excessive and violates best practices. Only the necessary permissions should be granted.

---

## Question-118

#iam 

You need to create a custom IAM role for use with a GCP service. All permissions in the role must be suitable for production use. You also want to clearly share with your organization the status of the custom role. This will be the first version of the custom role. What should you do?  

1. ***Use permissions in your role that use the 'supported' support level for role permissions. Set the role stage to ALPHA while testing the role permissions.***
2. Use permissions in your role that use the 'supported' support level for role permissions. Set the role stage to BETA while testing the role permissions.
3. Use permissions in your role that use the 'testing' support level for role permissions. Set the role stage to ALPHA while testing the role permissions.
4. Use permissions in your role that use the 'testing' support level for role permissions. Set the role stage to BETA while testing the role permissions.

### Explanation:

1. **Support Levels for Permissions**:
    - **Supported**: Permissions that are production-ready and stable. These should be used when creating roles for production use.
    - **Testing**: Permissions that are not production-ready and could be removed or changed without notice. These should not be used in roles intended for production.
2. **Role Stage**:
    - **ALPHA**: Used to indicate that the role is in an early testing phase and not ready for general use.
    - **BETA**: Used to indicate that the role is more stable but still undergoing testing.
    - **GA (General Availability)**: Used to indicate that the role is ready for production use.
3. **Best Practices for Custom IAM Roles**:
    - Use **'supported' permissions** to ensure production readiness.
    - Set the **role stage to ALPHA** during initial testing so the organization knows it is not yet fully tested or ready for general use.

### Why Not the Other Options?

- **B. Use 'supported' permissions and set the stage to BETA**:
    - The BETA stage is intended for roles that are stable but still under testing. For the **first version** of a role, you should start with ALPHA to clearly indicate it's an initial version.
- **C and D. Use 'testing' permissions**:
    - Permissions with the 'testing' support level are not suitable for production use. These permissions are unstable and might be deprecated without notice, making them inappropriate for production roles.
---
## Question #119

#security #storage 

Your company has a large quantity of unstructured data in different file formats. You want to perform ETL transformations on the data. You need to make the data accessible on Google Cloud so it can be processed by a Dataflow job. What should you do?  

1. Upload the data to BigQuery using the bq command line tool.
2. ***Upload the data to Cloud Storage using the gsutil command line tool.***
3. Upload the data into Cloud SQL using the import function in the console.
4. Upload the data into Cloud Spanner using the import function in the console.

### Explanation:

1. **Why Cloud Storage?**
    
    - **Cloud Storage** is designed for storing unstructured data in various file formats, making it the ideal storage solution for your large dataset.
    - **Dataflow** can directly read data from Cloud Storage as input for ETL (Extract, Transform, Load) jobs, making the data processing pipeline seamless.

### Why Not the Other Options?

- **A. Upload the data to BigQuery using the bq command-line tool**:
    - BigQuery is designed for structured, tabular data (like CSV, JSON, or Avro). Uploading unstructured data to BigQuery is not suitable without first transforming it.
- **C. Upload the data into Cloud SQL using the import function**:
    - Cloud SQL is a relational database for structured data, not for storing large quantities of unstructured data in different file formats.
- **D. Upload the data into Cloud Spanner using the import function**:
    - Cloud Spanner is also a relational database for structured data with strong consistency. It is not designed for handling large quantities of unstructured files.
---
## Question-121

#depoyments 

Your managed instance group raised an alert stating that new instance creation has failed to create new instances. You need to maintain the number of running instances specified by the template to be able to process expected application traffic. What should you do?  

1. Create an instance template that contains valid syntax which will be used by the instance group. Delete any persistent disks with the same name as instance names.
2. Create an instance template that contains valid syntax that will be used by the instance group. Verify that the instance name and persistent disk name values are not the same in the template.
3. ***Verify that the instance template being used by the instance group contains valid syntax. Delete any persistent disks with the same name as instance names. Set the disks.autoDelete property to true in the instance template.***
4. Delete the current instance template and replace it with a new instance template. Verify that the instance name and persistent disk name values are not the same in the template. Set the disks.autoDelete property to true in the instance template.
### Explanation:

1. **Why Validate the Instance Template**:
    - The instance template must have valid syntax and proper configurations to ensure instances can be created successfully. Any issues in the template, such as improper configurations or naming conflicts, will cause instance creation to fail.
2. **Persistent Disk Conflicts**:
    - If a persistent disk with the same name as the instance already exists, the new instance cannot be created because instance names must be unique within a project. Deleting conflicting disks resolves this issue.
3. **Set `disks.autoDelete` to `true`**:
    - Enabling the `disks.autoDelete` property ensures that disks created with instances are automatically deleted when the instances are removed. This avoids conflicts with future instance creations.
4. **How This Solves the Problem**:
    - Verifying the template syntax ensures the configurations are correct.
    - Deleting conflicting persistent disks removes obstacles to instance creation.
    - Setting `disks.autoDelete` ensures that instances and their associated resources are cleaned up properly, preventing future issues.
### Why Not the Other Options?

- **A. Create a new instance template and delete conflicting disks**:
    - Creating a new instance template is unnecessary unless the current template is invalid. Verifying the existing template and fixing issues is more efficient.
- **B. Create a new template and verify naming conflicts**:
    - Similar to A, creating a new instance template is redundant unless the current one is invalid. Fixing the existing one is sufficient.
- **D. Replace the current template and enable `disks.autoDelete`**:
    - Replacing the current template is unnecessary unless it's invalid. Verifying and fixing the existing template is simpler and avoids extra work.

---
## Question -136

#depoyments 

Your company runs one batch process in an on-premises server that takes around 30 hours to complete. The task runs monthly, can be performed offline, and must be restarted if interrupted. You want to migrate this workload to the cloud while minimizing cost. What should you do?  

- A. Migrate the workload to a Compute Engine Preemptible VM.
- B. Migrate the workload to a Google Kubernetes Engine cluster with Preemptible nodes.
- ***C. Migrate the workload to a Compute Engine VM. Start and stop the instance as needed.***
- D. Create an Instance Template with Preemptible VMs On. Create a Managed Instance Group from the template and adjust Target CPU Utilization. Migrate the workload.

> Preeemptible VMs are not suitable for long-running tasks. They can be terminated at any time and are not suitable for tasks that take 30 hours to complete. Using a regular Compute Engine VM and starting/stopping it as needed is a more cost-effective and reliable approach for this scenario.

---
## Question-140

#monitoring 

You are asked to set up application performance monitoring on Google Cloud projects A, B, and C as a single pane of glass. You want to monitor CPU, memory, and disk. What should you do?  

- A. Enable API and then share charts from project A, B, and C.
- B. Enable API and then give the metrics.reader role to projects A, B, and C.
- C. Enable API and then use default dashboards to view all projects in sequence.
- ***D. Enable API, create a workspace under project A, and then add projects B and C.***

### Explanation:

1. **Cloud Monitoring Workspaces**:
    - **Cloud Monitoring (formerly Stackdriver)** allows you to create a **workspace** to monitor multiple projects in a single pane of glass.
    - A **workspace** is associated with one project (the "host project") and can include resources from multiple other projects.
2. **Steps**:
    - **Step 1**: Enable the Cloud Monitoring API in projects A, B, and C.
    - **Step 2**: Create a **Cloud Monitoring Workspace** in **project A**.
    - **Step 3**: Add **projects B and C** to the workspace:
        - Navigate to **Monitoring > Settings > Workspace** in the Google Cloud Console.
        - Add the additional projects to the workspace.
    - Once the workspace is set up, you can monitor metrics like **CPU, memory, and disk** for resources across all projects.
3. **Why This Is the Best Option**:
    - By creating a workspace and adding all projects, you can view metrics across all projects in a single pane of glass.
    - This approach ensures centralized monitoring without requiring additional tools or manual aggregation.
### Why Not the Other Options?

- **A. Enable API and then share charts from project A, B, and C**:
    - Sharing individual charts from multiple projects does not provide a unified view. It is inefficient and lacks the ability to correlate metrics across projects.
- **B. Enable API and then give the `metrics.reader` role to projects A, B, and C**:
    - Assigning the `metrics.reader` role alone does not aggregate monitoring data. You still need a workspace to view metrics centrally.
- **C. Enable API and then use default dashboards to view all projects in sequence**:
    - Default dashboards allow you to view metrics for each project individually, but they do not provide a consolidated view across multiple projects.
---
## Question-139

#storage 

The core business of your company is to rent out construction equipment at large scale. All the equipment that is being rented out has been equipped with multiple sensors that send event information every few seconds. These signals can vary from engine status, distance traveled, fuel level, and more. Customers are billed based on the consumption monitored by these sensors. You expect high throughput `" up to thousands of events per hour per device `" and need to retrieve consistent data based on the time of the event. Storing and retrieving individual signals should be atomic. What should you do?  

- A. Create a file in Cloud Storage per device and append new data to that file.
- B. Create a file in Cloud Filestore per device and append new data to that file.
- C. Ingest the data into Datastore. Store data in an entity group based on the device.
- ***D. Ingest the data into Cloud Bigtable. Create a row key based on the event timestamp.***

### Explanation:

1. **Why Cloud Bigtable?**
    - **Cloud Bigtable** is a fully managed NoSQL database optimized for high-throughput and low-latency workloads, making it ideal for IoT use cases like storing sensor data.
    - It can handle **thousands of events per second per device**, scaling horizontally to meet your needs.
    - **Time-based queries** are efficient when row keys are designed appropriately, such as incorporating a timestamp.
2. **Row Key Design**:
    - Using the event timestamp in the row key ensures:
        - Data is stored in **time order**, making range queries by time efficient.
        - Atomicity of operations (as Bigtable guarantees atomic reads/writes at the row level).
    - Example row key: `DEVICE_ID#TIMESTAMP`.
3. **Use Case Fit**:
    - The requirements include **high throughput**, **atomic operations**, and **time-based data retrieval**, all of which align with Cloud Bigtable's strengths.

### Why Not the Other Options?

- **A. Create a file in Cloud Storage per device and append new data to that file**:
    - Cloud Storage is designed for storing large, unstructured files, not for high-throughput, low-latency event data.
    - Appending data to files does not provide atomicity or efficient time-based querying.
- **B. Create a file in Cloud Filestore per device and append new data to that file**:
    - Cloud Filestore is a managed NFS file storage system. It is not optimized for high-throughput workloads or atomic operations for event data.
- **C. Ingest the data into Datastore and store data in an entity group**:
    - While Datastore supports transactions, it is not designed for high-throughput IoT workloads.
    - Datastore enforces strong consistency within an entity group but can become a bottleneck for thousands of events per second.
---
## Question-163

#deployments 

You have developed a containerized web application that will serve internal colleagues during business hours. You want to ensure that no costs are incurred outside of the hours the application is used. You have just created a new Google Cloud project and want to deploy the application. What should you do?  

- A. Deploy the container on Cloud Run for Anthos, and set the minimum number of instances to zero.
- ***B. Deploy the container on Cloud Run (fully managed), and set the minimum number of instances to zero.***
- C. Deploy the container on App Engine flexible environment with autoscaling, and set the value min_instances to zero in the app.yaml.
- D. Deploy the container on App Engine flexible environment with manual scaling, and set the value instances to zero in the app.yaml.

### Explanation:

1. **Why Cloud Run (fully managed)?**
    - **Cloud Run (fully managed)** is a serverless platform designed for running containerized applications. It scales down to **zero instances** when not in use, which ensures no costs are incurred outside of business hours.
    - This fits the use case of serving an internal application during business hours and avoiding costs during idle times.
2. **Setting Minimum Instances to Zero**:
    - By setting `min-instances=0`, Cloud Run ensures that no container instances are kept running when there is no traffic. This eliminates idle costs entirely.
    - Cloud Run automatically spins up instances when traffic arrives and scales down when traffic stops.
3. **Why Cloud Run Is Best for This Use Case**:
    - **Cost Efficiency**: Only incurs costs when the application is actively serving traffic.
    - **Simplicity**: Does not require manual intervention or complex configuration to scale down during non-business hours.
    - **Serverless**: You don’t have to manage infrastructure, and scaling is automatic.
### Why Not the Other Options?

- **A. Cloud Run for Anthos with minimum instances set to zero**:
    - **Cloud Run for Anthos** is designed for Kubernetes clusters. It requires managing a Kubernetes cluster, which incurs infrastructure costs even when no traffic is being served. This is not a cost-efficient choice for this use case.
- **C. App Engine flexible environment with autoscaling (min_instances=0)**:
    - App Engine flexible environment does not support `min_instances=0`. The minimum number of instances must be at least 1, which incurs costs even during idle times.
- **D. App Engine flexible environment with manual scaling (instances=0)**:
    - Setting `instances=0` in manual scaling is not supported. App Engine flexible always requires at least one running instance.
---
## Question-165

#iam 

You are running a data warehouse on BigQuery. A partner company is offering a recommendation engine based on the data in your data warehouse. The partner company is also running their application on Google Cloud. They manage the resources in their own project, but they need access to the BigQuery dataset in your project. You want to provide the partner company with access to the dataset. What should you do?  

- A. Create a Service Account in your own project, and grant this Service Account access to BigQuery in your project.
- B. Create a Service Account in your own project, and ask the partner to grant this Service Account access to BigQuery in their project.
- C. Ask the partner to create a Service Account in their project, and have them give the Service Account access to BigQuery in their project.
- ***D. Ask the partner to create a Service Account in their project, and grant their Service Account access to the BigQuery dataset in your project.***

### Why This Approach Works:
- **Cross-Project Resource Sharing**: Service accounts are the standard way to securely grant access to resources across projects in Google Cloud.
- **Least Privilege**: By granting access to the partner's Service Account, you limit access to only the necessary dataset and ensure that permissions are not broadly applied.
### Why Not the Other Options?

- **A. Create a Service Account in your project and grant it access**:
    - If the Service Account resides in your project, it cannot directly interact with the partner's project. The partner's application would not have access to the Service Account in your project.
- **B. Create a Service Account in your project and ask the partner to grant it access**:
    - This reverses the intended setup. The partner's application requires access to your BigQuery dataset, not vice versa.
- **C. Ask the partner to create a Service Account and give it access to BigQuery in their project**:
    - The dataset resides in **your project**, so granting access to BigQuery in the partner's project is irrelevant.
---
## Question-184

#storage 

You need to configure optimal data storage for files stored in Cloud Storage for minimal cost. The files are used in a mission-critical analytics pipeline that is used continually. The users are in Boston, MA (United States). What should you do?  

- A. Configure regional storage for the region closest to the users. Configure a Nearline storage class.
- ***B. Configure regional storage for the region closest to the users. Configure a Standard storage class.***
- C. Configure dual-regional storage for the dual region closest to the users. Configure a Nearline storage class.
- D. Configure dual-regional storage for the dual region closest to the users. Configure a Standard storage class.

### Explanation:

1. **Data Storage Class for Mission-Critical and Frequently Accessed Data**:
    
    - The **Standard storage class** is ideal for frequently accessed data because it offers the **lowest latency** and **highest availability**, making it optimal for mission-critical workloads like a continually used analytics pipeline.
    - Other storage classes (e.g., Nearline, Coldline) are designed for infrequent access and would incur higher retrieval costs for frequently accessed data.
2. **Regional Storage**:
    
    - **Regional storage** is appropriate because the users are located in a single location (Boston, MA). Storing data in the closest region (e.g., `us-east1`) minimizes latency while keeping costs lower compared to multi-regional or dual-regional storage.
    - Dual-region storage, while offering additional redundancy, incurs higher costs and is unnecessary if data access is localized and latency-sensitive.
3. **Cost Optimization**:
    
    - **Regional Standard storage** minimizes costs while meeting the requirements for frequent data access and mission-critical performance.
    - **Nearline storage** is cheaper for storage but has higher data retrieval costs, making it unsuitable for continual access.

### Why Not the Other Options?

- **A. Regional storage with Nearline class**:
    
    - Nearline storage is designed for data accessed less than once a month. Since the pipeline accesses data continually, retrieval costs would outweigh the lower storage costs.
- **C. Dual-regional storage with Nearline class**:
    
    - Dual-region storage is more expensive than regional storage and unnecessary for a single-user location. Additionally, Nearline is not suitable for frequent data access.
- **D. Dual-regional storage with Standard class**:
    
    - Dual-regional storage provides added redundancy and availability but is more expensive than regional storage. Since the users are in a single location, the additional redundancy is unnecessary.
---
## Question-187

#monitoring #depoyments 

You need to manage a Cloud Spanner instance for best query performance. Your instance in production runs in a single Google Cloud region. You need to improve performance in the shortest amount of time. You want to follow Google best practices for service configuration. What should you do?  

- A. Create an alert in Cloud Monitoring to alert when the percentage of high priority CPU utilization reaches 45%. If you exceed this threshold, add nodes to your instance.
- B. Create an alert in Cloud Monitoring to alert when the percentage of high priority CPU utilization reaches 45%. Use database query statistics to identify queries that result in high CPU usage, and then rewrite those queries to optimize their resource usage.
- ***C. Create an alert in Cloud Monitoring to alert when the percentage of high priority CPU utilization reaches 65%. If you exceed this threshold, add nodes to your instance.***
- D. Create an alert in Cloud Monitoring to alert when the percentage of high priority CPU utilization reaches 65%. Use database query statistics to identify queries that result in high CPU usage, and then rewrite those queries to optimize their resource usage.
### Explanation:

1. **High Priority CPU Utilization in Cloud Spanner**:
    - High-priority CPU utilization indicates the percentage of CPU resources consumed by read and write operations necessary for query execution and transaction processing.
    - Google recommends monitoring **high-priority CPU utilization** to ensure sufficient capacity for workloads and scaling Cloud Spanner instances when utilization reaches critical thresholds.
2. **Why 65%?**:
    - Google Cloud's **best practice** is to add nodes when high-priority CPU utilization exceeds **65%**. This ensures that there is enough capacity to handle spikes in workload without risking performance degradation.
    - Scaling based on a 65% threshold helps maintain query performance and reduces the risk of latency issues.
3. **Short-Term Performance Improvement**:
    - Adding nodes is the **fastest way** to improve query performance in the short term because it provides additional CPU and storage capacity to handle increased workloads.
### Why Not the Other Options?

- **A. Alert at 45% and add nodes**:
    - 45% is a conservative threshold, and adding nodes at this point is unnecessary and may result in over-provisioning, leading to higher costs without a significant performance benefit.
- **B. Alert at 45% and rewrite queries**
    - Optimizing queries is a long-term performance improvement strategy but does not immediately resolve performance issues. Additionally, 45% utilization is not a critical level.
- **D. Alert at 65% and rewrite queries**
    - While query optimization is beneficial for long-term performance and cost management, adding nodes is the quickest way to improve performance in the short term, as required by the scenario.
---
## Question-190
#depoyments 

You are assigned to maintain a Google Kubernetes Engine (GKE) cluster named 'dev' that was deployed on Google Cloud. You want to manage the GKE configuration using the command line interface (CLI). You have just downloaded and installed the Cloud SDK. You want to ensure that future CLI commands by default address this specific cluster What should you do?  

- ***A. Use the command gcloud config set container/cluster dev.***
- B. Use the command gcloud container clusters update dev.
- C. Create a file called gke.default in the ~/.gcloud folder that contains the cluster name.
- D. Create a file called defaults.json in the ~/.gcloud folder that contains the cluster name.

---
## Question-194

#iam 

You have been asked to set up the billing configuration for a new Google Cloud customer. Your customer wants to group resources that share common IAM policies. What should you do?  

- A. Use labels to group resources that share common IAM policies.
- ***B. Use folders to group resources that share common IAM policies.***
- C. Set up a proper billing account structure to group IAM policies.
- D. Set up a proper project naming structure to group IAM policies.

> "Folders are used to group resources that share common IAM policies" https://cloud.google.com/resource-manager/docs/creating-managing-folders

---
## Question-202

#iam #deployments 

You have an application that runs on Compute Engine VM instances in a custom Virtual Private Cloud (VPC). Your company’s security policies only allow the use of internal IP addresses on VM instances and do not let VM instances connect to the internet. You need to ensure that the application can access a file hosted in a Cloud Storage bucket within your project. What should you do?

- A. Enable Private Service Access on the Cloud Storage Bucket.
- B. Add storage.googleapis.com to the list of restricted services in a VPC Service Controls perimeter and add your project to the list of protected projects.
- ***C. Enable Private Google Access on the subnet within the custom VPC.***
- D. Deploy a Cloud NAT instance and route the traffic to the dedicated IP address of the Cloud Storage bucket.

> C is the correct Answer as Private Google Access allows you to the connect on the internal networks, A is incorrect becuause Cloud Storage bucket dont have such services to connect to Private Acesss`

---
## Question-203

#iam #deployments 

Your company completed the acquisition of a startup and is now merging the IT systems of both companies. The startup had a production Google Cloud project in their organization. You need to move this project into your organization and ensure that the project is billed to your organization. You want to accomplish this task with minimal effort. What should you do?

- ***A. Use the projects.move method to move the project to your organization. Update the billing account of the project to that of your organization.***
- B. Ensure that you have an Organization Administrator Identity and Access Management (IAM) role assigned to you in both organizations. Navigate to the Resource Manager in the startup’s Google Cloud organization, and drag the project to your company's organization.
- C. Create a Private Catalog for the Google Cloud Marketplace, and upload the resources of the startup's production project to the Catalog. Share the Catalog with your organization, and deploy the resources in your company’s project.
- D. Create an infrastructure-as-code template for all resources in the project by using Terraform, and deploy that template to a new project in your organization. Delete the project from the startup’s Google Cloud organization.
### Why Not the Other Options?

- **B. Drag the project in the Resource Manager**
    - There is no drag-and-drop functionality in the Google Cloud Console to move projects between organizations.
    - This option is invalid.
- **C. Use a Private Catalog**
    - The Private Catalog is not designed for migrating projects or resources. It is used for sharing pre-configured solutions within an organization.
- **D. Use Terraform to recreate resources in a new project**
    - Recreating the project and its resources using Terraform is time-consuming and error-prone.
    - This approach does not preserve the project ID or its existing resources, leading to significant effort and disruption.

---
## Question-206

#iam #network 

You have two subnets (subnet-a and subnet-b) in the default VPC. Your database servers are running in subnet-a. Your application servers and web servers are running in subnet-b. You want to configure a firewall rule that only allows database traffic from the application servers to the database servers. What should you do?

- ***A. • Create service accounts sa-app and sa-db.***  
    ***• Associate service account sa-app with the application servers and the service account sa-db with the database servers.***  
    ***• Create an ingress firewall rule to allow network traffic from source service account sa-app to target service account sa-db.***
- B. • Create network tags app-server and db-server.  
    • Add the app-server tag to the application servers and the db-server tag to the database servers.  
    • Create an egress firewall rule to allow network traffic from source network tag app-server to target network tag db-server.
- C. • Create a service account sa-app and a network tag db-server.  
    • Associate the service account sa-app with the application servers and the network tag db-server with the database servers.  
    • Create an ingress firewall rule to allow network traffic from source VPC IP addresses and target the subnet-a IP addresses.
- D. • Create a network tag app-server and service account sa-db.  
    • Add the tag to the application servers and associate the service account with the database servers.  
    • Create an egress firewall rule to allow network traffic from source network tag app-server to target service account sa-db.

> Both service accounts and network tags can be used for creating a Cloud Firewall rule. The prime word is "to allow network traffic from app server to database server" which is achievable by inbound/ingress rule and not egress rule. https://cloud.google.com/firewall/docs/firewalls#rule_assignment

--- 

## Question-222

#deployments 

You want to permanently delete a Pub/Sub topic managed by Config Connector in your Google Cloud project. What should you do?

- A. Use kubectl to create the label deleted-by-cnrm and to change its value to true for the topic resource.
- ***B. Use kubectl to delete the topic resource.***
- C. Use gcloud CLI to delete the topic.
- D. Use gcloud CLI to update the topic label managed-by-cnrm to false.

> If a resource is managed by the Config Connector, you can update/delete it through kubectl command. https://cloud.google.com/config-connector/docs/how-to/getting-started#before_you_begin

--- 
## Question-225

#depoyments 

Your managed instance group raised an alert stating that new instance creation has failed to create new instances. You need to solve the instance creation problem. What should you do?

- ***A. Create an instance template that contains valid syntax which will be used by the instance group. Delete any persistent disks with the same name as instance names.***
- B. Create an instance template that contains valid syntax that will be used by the instance group. Verify that the instance name and persistent disk name values are not the same in the template.
- C. Verify that the instance template being used by the instance group contains valid syntax. Delete any persistent disks with the same name as instance names. Set the disks.autoDelete property to true in the instance template.
- D. Delete the current instance template and replace it with a new instance template. Verify that the instance name and persistent disk name values are not the same in the template. Set the disks.autoDelete property to true in the instance template.
> instance templates are immutable so can not modify or update them. https://cloud.google.com/compute/docs/instance-templates#instance-templates

---
## Question-228

#deployments 

You have a batch workload that runs every night and uses a large number of virtual machines (VMs). It is fault-tolerant and can tolerate some of the VMs being terminated. The current cost of VMs is too high. What should you do?

- ***A. Run a test using simulated maintenance events. If the test is successful, use Spot N2 Standard VMs when running future jobs.***
- B. Run a test using simulated maintenance events. If the test is successful, use N2 Standard VMs when running future jobs.
- C. Run a test using a managed instance group. If the test is successful, use N2 Standard VMs in the managed instance group when running future jobs.
- D. Run a test using N1 standard VMs instead of N2. If the test is successful, use N1 Standard VMs when running future jobs.

### Explanation:

1. **Why Spot VMs?**
    - **Spot VMs** are the most cost-effective option for workloads that are fault-tolerant and can handle interruptions. They are priced **up to 91% cheaper** than regular on-demand VMs.
    - Since the batch workload is fault-tolerant and runs nightly, it can tolerate the possibility of Spot VMs being terminated, making them an ideal choice.
2. **Why Test with Simulated Maintenance Events?**
    - Testing with **simulated maintenance events** ensures that the workload can recover properly from VM interruptions or terminations.
    - If the test confirms the workload can tolerate interruptions, Spot VMs can be safely used.
3. **Why Use N2 Standard VMs?**
    - **N2 Standard VMs** offer better performance and flexibility compared to N1 Standard VMs. They are also cost-optimized for general-purpose workloads.
### Why Not the Other Options?

- **B. Use N2 Standard VMs**:
    - Regular N2 Standard VMs are not cost-effective for a fault-tolerant batch workload. Spot VMs are a much cheaper alternative.
- **C. Use a managed instance group (MIG) with N2 Standard VMs**:
    - While a MIG can help manage VMs, it does not address cost reduction. Regular N2 Standard VMs are still more expensive than Spot VMs.
- **D. Use N1 Standard VMs instead of N2**:
    - N1 Standard VMs are older and generally less cost-efficient than N2 Standard VMs. Additionally, Spot VMs provide much greater cost savings than switching from N2 to N1.
---
## Question-261

#iam 

You are in charge of provisioning access for all Google Cloud users in your organization. Your company recently acquired a startup company that has their own Google Cloud organization. You need to ensure that your Site Reliability Engineers (SREs) have the same project permissions in the startup company's organization as in your own organization. What should you do?

- A. In the Google Cloud console for your organization, select Create role from selection, and choose destination as the startup company's organization.
- B. In the Google Cloud console for the startup company, select Create role from selection and choose source as the startup company's Google Cloud organization.
- ***C. Use the gcloud iam roles copy command, and provide the Organization ID of the startup company's Google Cloud Organization as the destination.***
- D. Use the gcloud iam roles copy command, and provide the project IDs of all projects in the startup company's organization as the destination.
### Explanation:

1. **Cross-Organization Role Consistency**:
    - Since your SREs need the same permissions in the startup company’s Google Cloud Organization as in your organization, you must replicate the **custom roles** that define these permissions.
    - The `gcloud iam roles copy` command is designed to duplicate custom roles from one organization to another.
2. **Why Use `gcloud iam roles copy`?**
    - This command allows you to copy an existing custom role to another project or organization.
    - By specifying the **Organization ID** of the startup’s Google Cloud organization as the destination, you ensure the custom roles are applied at the organizational level, enabling consistency across all projects in the startup’s organization.
- **Command Syntax**:
```sh
gcloud iam roles copy SOURCE_ROLE_ID \
    --source-organization=SOURCE_ORGANIZATION_ID \
    --destination-organization=DESTINATION_ORGANIZATION_ID \
    --destination-role=DESTINATION_ROLE_ID
```
### Why Not the Other Options?

- **A. Create a role from selection in your organization and set the startup company as the destination**:
    - The Google Cloud Console does not have functionality to copy roles between organizations directly.
- **B. Create a role from selection in the startup’s organization**:
    - Similar to Option A, the Google Cloud Console cannot directly replicate roles across organizations.
- **D. Copy roles to individual projects in the startup’s organization**:
    - Copying roles to individual projects is unnecessarily repetitive and inefficient. It is better to copy roles at the organization level to ensure consistency across all projects.
---
