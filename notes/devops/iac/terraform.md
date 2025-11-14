# Navigation
- [**HCL_Basics**](#hcl-basics)
- [**Initialization**](#initialization)
- [**Configuration_Files**](#configuration-files)
- [**Variables**](#variables)
	- [Default Syntax](#default-syntax)
	- [Variables_Usage](#variables-usage)
	- [Example](#example)
	- [Variables_Order](#variables-order)
	- [Resource_Attributes](#resource-attributes)
	- [Implicit_dependency](#implicit-dependency)
	- [Explicit_dependency](#explicit-dependency)
	- [Output](#output)
- [**Mutable_vs_Immutable**](#mutable-vs-immutable)
	- [LifeCycle_Rules](#lifecycle-rules)
- [**Datasource**](#datasource)
- [**Meta_Arguments**](#meta-arguments)
	- [Count](#count)
	- [For-Each](#for-each)
- [**Version-Constraints**](#version-constraints)
---
# Installation
- [Downloads link](https://developer.hashicorp.com/terraform/downloads)
```bash
wget https://releases.hashicorp.com/terraform/1.3.9/terraform_1.3.9_linux_amd64.zip
7z x terraform_1.3.9_linux_amd64.zip
mv terraform /usr/local/bin
# Enable auto-complete
terraform -install-autocomplete
```

# HCL_Basics
HashiCorp Configuration language
- **Basic resource block**
	- `resource`: Block Name
	- `local_file`: Resource type
	- `create_text_file`: Resource name
	- `filename`: local_file argument
	- `content`:  local_file argument
```bash
resource "local_file" "create-text-file" {
	filename="/home/zeyad/zeyad.txt"
	content="Hello World!"
}

resource "aws_s3_bucket" "data" {  
bucket = "webserver-bucket-org-2207"  
acl = "private"  
}

resource "aws_instance" "webserver" {  
ami = "ami-0c2f25c1f66a1ff4d"  
instance_type = "t2.micro"  
}
```
# Initialization
Initialize the backend, we use `init` to install the required plugins and `plan` to preview the changes that terraform plans to make to your infrastructure.
```bash
terraform init
terraform plan
# (Optional) if you are interested in forcing style convention
terafform fmt
```
Executes the actions proposed in terraform plan
```
terraform apply
```
To inspect a plan to ensure that the planned operations are expected
```bash
terrafrom show [-json]
```
To destroy the infrastructure
```
terraform destroy
```

# Configuration_Files
|**File Name**|**Purpose**|
|-|-|
|**`main.tf`**|Main configuration file containing resource definition|
|**`variables.tf`**|Contains variable definitions|
|**`outputs.tf`**|Contains output from resources|
|**`provider.tf`**|Contains provider definition|

# Variables
## Default Syntax
- **`variables.tf`**
```bash
variable "filename" {  
	default = "/root/pets.txt"  
}  
variable "content" {  
	default = "We love pets!"  
}  
variable "prefix" {  
	default = "Mrs"  
}  
variable "separator" {  
	default = "."  
}  
variable "length" {  
	default = "1"  
}
```
- **`main.tf`**
```bash
resource "local_file" "pet" {  
	filename = var.filename  
	content = var.content 
}  
resource "random_pet" "my-pet" {  
	prefix = var.prefix
	separator = var.separator 
	length = var.length
}
```

## Variables_Usage
1. [**variables.tf**](#default-syntax) (Must create)
2. Environment Variables
```bash
export TF_VAR_filename="/root/pets.txt"  
export TF_VAR_content="We love pets!"  
export TF_VAR_prefix="Mrs"  
export TF_VAR_separator="."  
export TF_VAR_length="2"
```
3. Terraform CLI
```bash
terraform apply -var "filename=/root/pets.txt" -var "content=We love  
Pets!" -var "prefix=Mrs" -var "separator=." -var "length=2"
```
4. Custom file
```bash
terrafrom -var-file custom.tfvars
```
> **Note:**
> `terraform.tfvars` , `terraform.tfvars.json`, `*.auto.tfvars`,`*.auto.tfvars.json` are automatically loaded.


## Example
Create a plan using `prod.tfvars`.
- **`main.tf`**
```bash
resource "local_file" "s3cret" {  
	filename = var.filename  
	sensitive_content = var.sensitive_content 
}  
```
-  **`variables.tf`**
```bash
variable "filename" {  
	default = "/root/secret.txt"
	type = string  
}  
variable "sensitive_content" {
	default = "Sup3rS3cureP@ssw0rd!"
	type = string
}
```
- **`prod.tfvars`**
```bash
filename = "/root/SuperSecret.txt"
sensitive_content = "VerySup3rS3cureP@ssw0rd!@!"
```
- **Run**
```
terrafrom init
terraform -var-file="prod.tfvars" [-compact-warnings]
terraform fmt
terraform apply
```
## Variables_Order
variables order of invocation
|**Order**|**Option**|
|-|-|
|1|Enironment variables|
|2|terraform.tfvars|
|3|\*.auto.tfvars (Alphabetical order)|
|4|`-var` or `-var-file` (CLI)|

## Resource_Attributes
### Implicit_dependency
If we want to use a resource that is created by another resource
```bash
resource "local_file" "pet" {  
	filename = var.filename  
	content = "My favourite pet is: ${random_pet.my-pet.id}" 
}  
resource "random_pet" "my-pet" {  
	prefix = var.prefix
	separator = var.separator 
	length = var.length
}
```
### Explicit_dependency
Used between dependencies that aren't visible to terraform
```shell
resource "local_file" "pet" {  
	filename = var.filename  
	content = "My favourite pet is ${random_pet.my-pet.id}"
	depends_on = [random_pet.my-pet]
}  
resource "random_pet" "my-pet" {  
	prefix = var.prefix
	separator = var.separator 
	length = var.length
}
```
## Output
```shell
resource "random_pet" "my-pet" {
	length = var.length
}

output "pet-name" {
	value = random_pet.my-pet.id
	description = "Record the value of pet ID generated by the random_pet resource"

}

resource "local_file" "welcome" {
	filename = "/root/message.txt"
	content = "Welcome to Kodekloud."

}

output "welcome_message" {
	value = local_file.welcome.content
}
```
- Invoke
```bash
terraform output
terraform output pet-name
terraform output welcome_message
```

# Terraform_commands
- **validate**: Check for syntax errors.
- **output**: Extract the value of an output variable from the state file.
- **fmt**: Format the syntax to match the style convention.
- **refresh**: Update the state file with new non-terraform changes (manual changes). This option is invoked by default when running `terrafrom plan`.
- **graph**: Print a `dot` formatted graph.

# Mutable_vs_Immutable
Mutable infrastructures allow for regular updates and modifications after the software has been deployed, whereas immutable infrastructures do not allow modifications once the software has been deployed.

## LifeCycle_Rules
```sh

resource "local_file" "welcome" {
	filename = "/root/message.txt"
	content = "Welcome to Kodekloud."

	lifecycle {
		#ignore_changes = []
		ignore_changes = all
}
}
```

# Datasource
- **`data`**: To read a file not managed by terraform.
```sh
resource "local_file" "welcome" {
	filename = "/root/message.txt"
	content = data.local_file.dog.content
}

data "local_file" "msg" {
	filename = "/root/WelcomeMsg.txt"
}
```

#  Meta_Arguments
## Count
Create multiple instances of a resource, however if an instance is removed or added; the whole resource will be recreated.
- **`main.tf`**
```
resource "local_file" "pet" {
	filename = var.filename[count.index]
	count = length(var.filename) 
}
```
- **`variables.tf`**
```
variable "filename" {  
	default = "["/root/horse.txt", "/root/meow.txt", "/root/cats.txt"] 
}
```
## For-Each
Only works with a `map` or `set`, and doesn't need to recreate the whole resource on any change
- **`main.tf`**
```
resource "local_file" "pet" {
	filename = each.value
	for_each = var.filename
	# for_each = toset(var.filename) -- use this if you don't want to change the type in "variables.tf" file 
}
```
- **`variables.tf`**
```
variable "filename" {
	type = set(string)
	default = "["/root/horse.txt", "/root/meow.txt", "/root/cats.txt"] 
}
```
# Version-Constraints
We can use comparison operators to specify versions
- Use a specific version of a provider
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.57.1"
    }
  }
}

provider "aws" {
  # Configuration options
}
```
- Do not use `4.57.1` version
```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "! 4.57.1"
    }
  }
}

provider "aws" {
  # Configuration options
}
```
- **More info**: [Version Constraints - Configuration Language | Terraform | HashiCorp Developer](https://developer.hashicorp.com/terraform/language/expressions/version-constraints)
