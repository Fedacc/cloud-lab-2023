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


# create a kubernetes cluster
resource "ibm_container_cluster" "free_cluster" {
  name              = "cloud-lab-cluster"
  resource_group_id = data.ibm_resource_group.resource_group.id
  datacenter        = "mil01"
  machine_type      = "free"
  hardware          = "shared"
  wait_till         = "OneWorkerNodeReady"
  labels = {
    "test" = "lab-pool"
  }

}


# set up the container registry - create a container registry namespace
resource "ibm_cr_namespace" "cr_namespace" {
  name              = "cloud-lab-${var.cr_suffix}"
  resource_group_id = data.ibm_resource_group.resource_group.id
}

# interact with the kubernetes cluster - example: create a secret

# collect cluster configuration info for access
data "ibm_container_cluster_config" "cluster_config" {
  cluster_name_id = ibm_container_cluster.free_cluster.id
  admin           = true
}

# collect all the namespaces names in the kubernetes cluster
data "kubernetes_all_namespaces" "allns" {}

# TASK: create a configmap and secret for the microservice SEARCH-NLU
#
# CONFIGMAP VALUES:
# - NLU_BASEURL=string
# - NLU_VERSION=string
#
# SECRET VALUES:
# - NLU_APIKEY=string

resource "kubernetes_secret" "search_nlu_secret" {
  type = "Opaque"
  metadata {
    name      = "search-nlu-secret"
    namespace = "default"
  }

  data = {
    NLU_APIKEY = ibm_resource_key.nlu_resource_key.credentials.apikey
  }

}

resource "kubernetes_config_map" "search_nlu_configmap" {
  metadata {
    name = "search-nlu-configmap"
  }

  data = {
    NLU_BASEURL = ibm_resource_key.nlu_resource_key.credentials.url
    NLU_VERSION = var.nlu_sdk_version
  }

}