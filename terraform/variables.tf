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

variable "nlu_sdk_version" {
    type        = string
    description = "version to be used in the watson SDK for python for NLU"
    default     = "2022-04-07"
}

variable "cr_suffix" {
    type        = string
    description = "unique identifier to be appended to the container registry name"
}