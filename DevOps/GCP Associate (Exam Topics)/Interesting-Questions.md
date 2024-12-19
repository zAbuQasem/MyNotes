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

---
### Why Not the Other Options?

- **B. Assign the engineering team only the Billing Account User role on the billing account**:
    
    - This would allow the engineering team to link projects to the billing account, violating the requirement that only the finance team should have this ability.
- **C. Assign the finance team the Billing Account User role on the billing account and the Project Billing Manager role on the organization**:
    
    - The **Project Billing Manager** role on the organization is unnecessary. The **Billing Account User** role alone is sufficient to allow the finance team to link projects to the billing account.
- **D. Assign the engineering team the Billing Account User role on the billing account and the Project Billing Manager role on the organization**:
    
    - This would allow the engineering team to link projects to the billing account, which is explicitly against the requirements.
---
