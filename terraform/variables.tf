# This file contains the declaration of the variables that need to be collected from the user

variable "ibmcloud_apikey" {
    type        = string
    description = "IBM Cloud apikey to provision resources"
}

variable "target_resource_group" {
    type        = string
    description = "Name of the resource group in which resources will be deployed"
    default     = "Default"
}