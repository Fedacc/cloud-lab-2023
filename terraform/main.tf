# This is the terraform file with the instructions for the provisioning of the resources

# # create a resource group - NOT WORKING FOR TRIAL ACCOUNTS ON IBM CLOUD
# resource "ibm_resource_group" "resource_group" {
#   name = "cloud-lab"
# }

# access the information about an existing resource group
data "ibm_resource_group" "resource_group" {
  name = var.target_resource_group
}

# create a Natural Language Understanding Service
resource "ibm_resource_instance" "nlu_service"{
    location = "eu-de"
    service = "natural-language-understanding"
    plan = "free"
    name = "nlu-service"
    resource_group_id = data.ibm_resource_group.resource_group.id
}

# create a set of credentials for the nlu service
resource "ibm_resource_key" "nlu_resource_key" {
  name                 = "nlu_credentials_manager"
  role                 = "Manager"
  resource_instance_id = ibm_resource_instance.nlu_service.id

  timeouts {
    create = "5m"
    delete = "5m"
  }
}