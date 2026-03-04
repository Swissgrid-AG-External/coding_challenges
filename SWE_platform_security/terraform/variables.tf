variable "resource_group_name" {
  default = "rg-data-collector"
}

variable "location" {
  default = "West Europe"
}

variable "api_key_secret_uri" {
  description = "Key Vault Secret URI for API_KEY app setting."
  type        = string
  nullable    = false
}

variable "api_url" {
  description = "Upstream API URL used by the function app."
  type        = string
  nullable    = false
}

variable "storage_account_name" {
  default = "acmedatacollector01"
}

variable "function_app_name" {
  default = "func-data-collector-prod"
}
