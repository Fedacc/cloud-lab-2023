# this file will describe the output of the execution of the terraform scripts

output "target_resource_group_id" {
  value       = data.ibm_resource_group.resource_group.id
  description = "ID of the targeted resource group"
}

output "nlu_service_id" {
  value       = ibm_resource_instance.nlu_service.id
  description = "ID of nlu service created"
}

output "nlu_service_credentials_name" {
  value       = ibm_resource_key.nlu_resource_key.name
  description = "Name of nlu service credentials created"
}

output "nlu_service_credentials_apikey" {
  value       = ibm_resource_key.nlu_resource_key.credentials.apikey
  description = "Apikey of nlu service credentials"
  sensitive   = true
}

