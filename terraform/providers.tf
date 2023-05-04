# This file contains the information about the required PROVIDERS

terraform {
  required_providers {
    ibm = {
      source  = "IBM-Cloud/ibm"
      version = ">= 1.12.0"
    }
  }
}

provider "ibm" {
  region           = "eu-de"
  ibmcloud_api_key = var.ibmcloud_apikey
}